"""An AWS Python Pulumi program"""

import json
import pulumi
import pulumi_aws as aws
import os
import zipfile


# Domain names
frontend_domain = "todo.weecplanet.de"
backend_domain = "todo-api.weecplanet.de"

# Get Mongodb connection string
mongo_db_secret = aws.secretsmanager.Secret.get("mongodb_url", id="arn:aws:secretsmanager:eu-west-1:503530077116:secret:dev/mongo/db-fVny03")
mongo_db_secret_version = aws.secretsmanager.get_secret_version(secret_id=mongo_db_secret.id)
# mongo_db_secret_version.apply(lambda version: print(version.secret_string))
parsed_secret = json.loads(mongo_db_secret_version.secret_string)

mongo_db_connection_url = parsed_secret['MONGODB_URL']


# Create provider in us-eas-1
us_east_1 = aws.Provider("awsUsEast", region="us-east-1")
# Get zone id
zone = aws.route53.get_zone(name="weecplanet.de.")

# Create Cognito User poll for authentication
todo_user_pool = aws.cognito.UserPool("user-pool", name="todo-user-pool")

todo_user_pool_domain = aws.cognito.UserPoolDomain("main",
    domain="lp-auth",
    user_pool_id=todo_user_pool.id)
## Create a Cognito Resource Server
resource_server = aws.cognito.ResourceServer('todo-api',
    identifier=f'https://{backend_domain}',
    name='todo backend api resource',
    user_pool_id=todo_user_pool.id,
    scopes=[
    aws.cognito.ResourceServerScopeArgs(
        scope_description="Read access",
        scope_name="todos.read",
    ),
    aws.cognito.ResourceServerScopeArgs(
        scope_description="Write access",
        scope_name="todos.write",
    )
    ]
)

## Create a Cognito User Pool Client (Application)
user_pool_client = aws.cognito.UserPoolClient('todo-client-app',
    name='todo-user-pool-client',
    user_pool_id=todo_user_pool.id,
    generate_secret=False,
    callback_urls=[f"https://{frontend_domain}"],
    logout_urls=[f"https://{frontend_domain}"],
    allowed_oauth_flows_user_pool_client=True,
    explicit_auth_flows=["ALLOW_USER_SRP_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
    allowed_oauth_flows=[
        "code",
    ],
    allowed_oauth_scopes=[
        "email",
        "openid",
        "phone",
        f"https://{backend_domain}/todos.read",
        f"https://{backend_domain}/todos.write"
    ],
    access_token_validity=60,
    id_token_validity=60,
    refresh_token_validity=1440,
    token_validity_units={
        'accessToken': 'minutes',
        'idToken': 'minutes',
        'refreshToken': 'minutes'
    },
    supported_identity_providers=["COGNITO"],
     opts=pulumi.ResourceOptions(depends_on=[resource_server]),
)


# Create lambda function for backend
role = aws.iam.Role("todo-backend-dev-lambda-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": { "Service": "lambda.amazonaws.com" },
            "Action": "sts:AssumeRole"
        }]
    })
)

policy = aws.iam.RolePolicy("todo-backend-dev-lambda-policy",
    role=role.id,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["logs:*", "cloudwatch:*"],
            "Resource": "*",
            "Effect": "Allow",
        }],
    }))
# for an example handler.
todo_backend_lambda = aws.lambda_.Function("todo-backend-dev",
    package_type="Image",
    image_uri="503530077116.dkr.ecr.eu-west-1.amazonaws.com/today/backend:latest",
    timeout=300,
    role=role.arn,
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "MONGODB_URL": mongo_db_connection_url,
        },
    ),
    opts=pulumi.ResourceOptions(depends_on=[policy]),
)

# Create API gateway for Backend
api = aws.apigateway.RestApi("todo-backend-dev",
    description="This is my API for demonstration purposes",
    endpoint_configuration={
        "types": "REGIONAL",
    },
)

## Create a resource to map the end-point.
resource = aws.apigateway.Resource("external-facing",
    rest_api=api.id,
    parent_id=api.root_resource_id,
    path_part="{proxy+}")  # This is the path part. For example, in 'domain.com/my-path', it's 'my-path'.


integration = aws.apigateway.Integration("todo-backend-integration",
    rest_api=api.id,
    resource_id=resource.id,
    http_method="ANY",  # 'ANY' integrates all HTTP methods or you can specify 'GET', 'POST', etc.
    type="AWS_PROXY",  # Use AWS_PROXY integration for a Lambda proxy setup
    integration_http_method="POST",
    uri=todo_backend_lambda.invoke_arn)

# Difine Cognito Authorizer
authorizer = aws.apigateway.Authorizer('authorizer',
    rest_api=api.id,
    name='cognito-authorizer',
    type='COGNITO_USER_POOLS',
    provider_arns=[todo_user_pool.arn])
## Define the method response.
method = aws.apigateway.Method("todo-external-method",
    rest_api=api.id,
    resource_id=resource.id,
    http_method='ANY',
    authorization="COGNITO_USER_POOLS",
    authorizer_id=authorizer.id,
    authorization_scopes=[
        f"https://{backend_domain}/todos.read",
        f"https://{backend_domain}/todos.write"
    ]
    # Choose the type of authorization you want for this method
)

# Create /internal resource that will only allow aws services to connect
# internal_resource = aws.apigateway.Resource("internal-facing",
#     rest_api=api.id,
#     parent_id=api.root_resource_id,
#     path_part="internal")

# # Path in the lambda integration for triggers
# triggers_resource = aws.apigateway.Resource("triggers",
#     rest_api=api.id,
#     parent_id=internal_resource.id,
#     path_part="triggers")

# triggers_method = aws.apigateway.Method("triggers-method",
#     rest_api=api.id,
#     resource_id=triggers_resource.id,
#     http_method='POST',
#     authorization="NONE",
#     # Choose the type of authorization you want for this method
# )

## Deploy the API by creating a deployment resource.
deployment = aws.apigateway.Deployment("todo-api-deployment",
    rest_api=api.id,
    stage_name="dev",
    opts=pulumi.ResourceOptions(depends_on=[integration, method])
    )  # The stage name for the deployment

# Create custom domain
backend_certificate = aws.acm.Certificate("todo-backend-certificate",
    domain_name=backend_domain,
    validation_method="DNS",
    #  opts=pulumi.ResourceOptions(provider=us_east_1)
)

backend_cert_validation_records = aws.route53.Record("backendCertValidationRecord",
    name=backend_certificate.domain_validation_options[0].resource_record_name,
    zone_id=zone.zone_id,
    type=backend_certificate.domain_validation_options[0].resource_record_type,
    records=[backend_certificate.domain_validation_options[0].resource_record_value],
    ttl=300,
    # opts=pulumi.ResourceOptions(provider=us_east_1)
)

# Wait for the certificate to be validated
backend_cert_validation = aws.acm.CertificateValidation("backendCertificateValidation",
    certificate_arn=backend_certificate.arn,
    validation_record_fqdns=[backend_cert_validation_records.fqdn],
    # opts=pulumi.ResourceOptions(provider=us_east_1)
)


api_gateway_custom_domain = aws.apigateway.DomainName("apiGatewayCustomDomain",
    regional_certificate_arn=backend_cert_validation.certificate_arn,
    endpoint_configuration={
        "types": "REGIONAL",
    },
    domain_name=backend_domain
    )

api_gateway_custom_domain_record = aws.route53.Record("apiGatewayCustomDomainRecord",
    name=api_gateway_custom_domain.domain_name,
    type=aws.route53.RecordType.A,
    zone_id=zone.zone_id,
    aliases=[{
        "evaluate_target_health": False,
        "name": api_gateway_custom_domain.regional_domain_name,
        "zone_id": api_gateway_custom_domain.regional_zone_id,
    }])

# Create custom domain and api gateway mappings
api_gateway_custom_domain_mapping = aws.apigateway.BasePathMapping("mapApiGatewayCustomDomain",
    domain_name=api_gateway_custom_domain.domain_name,
    rest_api=api.id,
    stage_name="dev")

# ## Link the deployment to the REST API.
# stage = aws.apigateway.Stage("todo-stage",
#     rest_api=api.id,
#     deployment=deployment.id,
#     stage_name="v1"
#     )

# Create Lambda at the edge
lambda_edge_role = aws.iam.Role('lamda-edge-role', 
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": ["lambda.amazonaws.com", "edgelambda.amazonaws.com"]
            }
        }]
    })
)

lambda_edge_policy = aws.iam.RolePolicy('lambda-edge-policy',
    role=lambda_edge_role.id,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:*:*:*"
        },{
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream", 
                "logs:PutLogEvents"
            ],
            "Resource": ["arn:aws:logs:*:*:log-group:/aws/lambda/*"]
        }]
    })
)


# Create signin lambda function
## zip signin lambda
path_to_signin_lambda = "../authentication/signin"
relroot = os.path.abspath(os.path.join(path_to_signin_lambda, os.pardir))
signin_zip_file="signin.zip"

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(path_to_signin_lambda))
template = env.get_template('index.js.j2')

# pulumi.Output.all(todo_user_pool.id,user_pool_client.id, todo_user_pool_domain.domain).apply(
#     lambda args: render_index_js(args[0], args[1], args[2]),
#     opts=pulumi.ResourceOptions(depends_on=[todo_user_pool, user_pool_client, todo_user_pool_domain])
# )
def render_index_js(user_pool_id, user_pool_app_id, user_pool_domain):
    variables = {
        "region": "eu-west-1",
        "user_pool_id": user_pool_id,
        "user_pool_app_id": user_pool_app_id,
        "user_pool_domain": user_pool_domain
    }
    rendered_content = template.render(variables)
    rendered_file_path = f'{path_to_signin_lambda}/index.js'
    with open(rendered_file_path, 'w') as rendered_file:
        rendered_file.write(rendered_content)

def handle_output(args):
    if not all(isinstance(arg, str) for arg in args):
        print(f"Error: Unexpected output types: {[type(arg) for arg in args]}")
        return
    render_index_js(args[0], args[1], args[2])
    
def log_resource(name, resource):
    print(f"Resource {name}: {type(resource)}")
    if isinstance(resource, tuple):
        print(f"{name} is a tuple with {len(resource)} elements:")
        for i, item in enumerate(resource):
            print(f"  Element {i}: {type(item)}")
            if hasattr(item, 'id'):
                print(f"    ID: {item.id}")
            if hasattr(item, 'domain'):
                print(f"    Domain: {item.domain}")
    else:
        if hasattr(resource, 'id'):
            print(f"{name} ID: {resource.id}")
        else:
            print(f"{name} has no 'id' attribute")
        if hasattr(resource, 'domain'):
            print(f"{name} Domain: {resource.domain}")
        else:
            print(f"{name} has no 'domain' attribute")

# Log resource information
# Log resource information
log_resource("todo_user_pool", todo_user_pool)
log_resource("user_pool_client", user_pool_client)
log_resource("todo_user_pool_domain", todo_user_pool_domain)

# Use apply on each resource individually
todo_user_pool.id.apply(lambda id: print(f"todo_user_pool ID: {id}"))

# Handle user_pool_client differently since it's a tuple
if isinstance(user_pool_client, tuple):
    print("user_pool_client is a tuple, accessing first element")
    if len(user_pool_client) > 0 and hasattr(user_pool_client[0], 'id'):
        user_pool_client[0].id.apply(lambda id: print(f"user_pool_client ID: {id}"))
    else:
        print("Unable to access id of user_pool_client")
else:
    user_pool_client.id.apply(lambda id: print(f"user_pool_client ID: {id}"))

todo_user_pool_domain.domain.apply(lambda domain: print(f"todo_user_pool_domain Domain: {domain}"))

# Modify the Output.all call to handle the tuple
pulumi.Output.all(
    todo_user_pool.id,
    user_pool_client.id,
    todo_user_pool_domain.domain
).apply(handle_output)

# rendered_file_path = f'{path_to_signin_lambda}/index-2.js'
# with open(rendered_file_path, 'w') as rendered_file:
#     rendered_file.write(rendered_content)

with zipfile.ZipFile(signin_zip_file, "w", zipfile.ZIP_DEFLATED) as zip:
    for root, dirs, files in os.walk(path_to_signin_lambda):
        zip.write(root,os.path.relpath(root,relroot))
        for file in files:
           filename = os.path.join(root, file)
           if os.path.isfile(filename) and not file.endswith('.j2'):
               file_in_zip = os.path.join(os.path.relpath(root, relroot), file)
               zip.write(filename, file_in_zip)

    ## Create signin lambda edge (Note that edge functions are in us-east-1)
    signin_edge_function = aws.lambda_.Function('signin-edge-function',
        code=pulumi.FileArchive(signin_zip_file),
        role=lambda_edge_role.arn,
        handler='signin/index.handler',
        runtime='nodejs18.x',
        publish = True,
        opts=pulumi.ResourceOptions(provider=us_east_1) 
    )

# Create authentication parser to extract token for backend
parser_zip_file = "auth_parser.zip"
# script_dir = os.path.dirname(os.path.abspath(__file__))
# real_path = os.path.abspath(os.path.join(script_dir, "../authentication/parse-auth/index.js"))
path_to_index = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../authentication/parse-auth/")), "index.js")
print(path_to_index)
with zipfile.ZipFile(parser_zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(path_to_index, "index.js")


    ## Create auth parser edge lambda (Note that edge functions are in us-east-1)
    parse_auth_edge_function = aws.lambda_.Function('auth-parser',
        code=pulumi.FileArchive(parser_zip_file),
        role=lambda_edge_role.arn,
        handler='index.handler',
        runtime='nodejs18.x',
        publish = True,
        opts=pulumi.ResourceOptions(provider=us_east_1) 
    )

# Cloudfront origin access
# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket('lp-todo-frontend-react')
## Create a CloudFront Origin Access Identity
origin_access_identity = aws.cloudfront.OriginAccessIdentity('todo-app-origin-access-identity',
    comment="Todo App s3 access identity")

## create bucket policy which allows origin access to s3 bucket contents
bucket_policy = aws.s3.BucketPolicy('bucketPolicy',
    bucket=bucket.id,
    policy= pulumi.Output.all(bucket.id, origin_access_identity.iam_arn).apply(lambda args: json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowCloudFrontServicePrincipalReadOnly",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudfront.amazonaws.com"
                },
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{args[0]}/*",
            },
            {
                "Effect": "Allow",
                "Principal": {
                    # ARN of the CloudFront Origin Access Identity
                    "AWS": args[1]
                },
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{args[0]}/*"
            }
        ]
    }))
)

# Cloudfront certificate
certificate = aws.acm.Certificate("todo-acm-certificcate",
    domain_name=frontend_domain,
    validation_method="DNS",
    opts=pulumi.ResourceOptions(provider=us_east_1) 
)

validation_records = aws.route53.Record("certValidationRecord",
    name=certificate.domain_validation_options[0].resource_record_name,
    zone_id=zone.zone_id,
    type=certificate.domain_validation_options[0].resource_record_type,
    records=[certificate.domain_validation_options[0].resource_record_value],
    ttl=300,
    opts=pulumi.ResourceOptions(provider=us_east_1)
)

# Wait for the certificate to be validated
validation = aws.acm.CertificateValidation("certificateValidation",
    certificate_arn=certificate.arn,
    validation_record_fqdns=[validation_records.fqdn],
    
    opts=pulumi.ResourceOptions(provider=us_east_1)
)



# Create CloudFront with two origins
distribution = aws.cloudfront.Distribution('todo-app-distribution',
    enabled=True,
    default_root_object="index.html",
    origins=[
        aws.cloudfront.DistributionOriginArgs(
            origin_id='todo-app',
            domain_name=bucket.bucket_regional_domain_name,
            s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
                origin_access_identity=origin_access_identity.cloudfront_access_identity_path
            )
        ),
        aws.cloudfront.DistributionOriginArgs(
            origin_id='todo-api',
            domain_name=backend_domain,
            custom_origin_config=aws.cloudfront.DistributionOriginCustomOriginConfigArgs(
                http_port=80,
                https_port=443,
                origin_protocol_policy='https-only',
                origin_ssl_protocols=['TLSv1.2']
            )
        )
    ],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        target_origin_id='todo-app',  # Default to S3 origin
        viewer_protocol_policy='redirect-to-https',
        allowed_methods=['GET', 'HEAD', 'OPTIONS'],
        cached_methods=['GET', 'HEAD'],
        forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=False,
            cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(forward='none')
        ),
        lambda_function_associations=[ 
            aws.cloudfront.DistributionDefaultCacheBehaviorLambdaFunctionAssociationArgs(
                event_type = "viewer-request",
                lambda_arn = signin_edge_function.qualified_arn
            )
        ]
    ),
     ordered_cache_behaviors=[{
        "allowedMethods": ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"],
        "viewerProtocolPolicy": "https-only",
        "cachedMethods": ["HEAD", "GET"],
        "targetOriginId": "todo-api",
        "pathPattern": "/api/*",
        "minTtl": 0,
        "defaultTtl": 0,
        "lambdaFunctionAssociations": [{
            "eventType": "viewer-request",
            "lambdaArn": parse_auth_edge_function.qualified_arn,
        }],
        "maxTtl": 0,
        "forwardedValues": {
            "cookies": {
                "forward": "none",
            },
            "queryString": False,
        },
        "smoothStreaming": False,
        "compress": False,
    }],
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type='none'
        )
    ),
    aliases=[
        frontend_domain,
    ],
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
        acm_certificate_arn=validation.certificate_arn,
        ssl_support_method="sni-only",
        minimum_protocol_version="TLSv1.2_2021"
    )
)

# Create Route53 records
www = aws.route53.Record("todo-record",
    zone_id=zone.zone_id,
    name=f"todo.{zone.name}",
    type=aws.route53.RecordType.A,
    aliases=[{
        "name": distribution.domain_name,
        "zone_id": distribution.hosted_zone_id,
        "evaluate_target_health": False,
    }])


# def replace_cognito_variables(variables):
#     path_to_index = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../authentication/signin/")), "index.js")
#     sign_in_index_content  = open(path_to_index, "r")
#     updated_signin__index_content


# Export outputs
pulumi.export('todo-bucket-name', bucket.id)
pulumi.export("invoke_url", deployment.invoke_url)
pulumi.export("application_url", distribution.domain_name)