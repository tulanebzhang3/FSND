/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-54hg6pgw', // the auth0 domain prefix
    audience: 'http://127.0.0.1:5000', // the audience set for the auth0 app
    clientId: '0Uf6L5m0Hytky1N6K0PVeLdnA2eSEVli', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8400', // the base url of the running ionic application.
  }
};
