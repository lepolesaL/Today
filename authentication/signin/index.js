const { Authenticator } = require('cognito-at-edge');

const authenticator = new Authenticator({
  // Replace these parameter values with those of your own environment
  region: 'eu-west-1', // user pool region
  userPoolId: 'eu-west-1_FU6ySVJyb', // user pool ID
  userPoolAppId: '3untv7fd99ihuba6f0tup4tb61', // user pool app client ID
  userPoolDomain: 'lp-auth.auth.eu-west-1.amazoncognito.com', // user pool domain
});

exports.handler = async (request) => authenticator.handle(request);