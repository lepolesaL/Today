'use strict';


function extractAccessTokenFromCookie(cookieString) {
  
  // Define a regular expression to match the accessToken cookie
  const accessTokenRegex = /accessToken=([^;]*)/;

  // Use the exec method to find the match in the cookie string
  const match = accessTokenRegex.exec(cookieString);

  // If a match is found, return the captured group (the access token)
  if (match && match.length > 1) {
    return match[1];
  } else {
    // If no match is found, return null or handle the case accordingly
    return null;
  }
}

exports.handler = (event, context, callback) => {
    const request = event.Records[0].cf.request;
    const headers = request.headers;
    if (headers.cookie) {
       const token = extractAccessTokenFromCookie(headers["cookie"][0].value)
       headers['authentication'] = [{"key": "Authentication", "value": `Bearer ${token}`}]
    }
    console.log(`Request uri set to "${JSON.stringify(request)}"`);
    callback(null, request);
};