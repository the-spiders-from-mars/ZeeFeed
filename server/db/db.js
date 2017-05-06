/**
 * Created by zeling on 2017/5/6.
 */
const cfenv = require('cfenv');

let vcapLocal;
try {
    vcapLocal = require('../vcap-local.json');
    console.log("Loaded local VCAP", vcapLocal);
} catch (e) { }

const appEnvOpts = vcapLocal ? { vcap: vcapLocal} : {}

const appEnv = cfenv.getAppEnv(appEnvOpts);

if (appEnv.services['cloudantNoSQLDB']) {
    // Load the Cloudant library.
    var Cloudant = require('cloudant');

    // Initialize database with credentials
    exports.cloudant = cloudant = Cloudant(appEnv.services['cloudantNoSQLDB'][0].credentials);
}


