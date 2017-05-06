/**
 * Created by zeling on 2017/5/6.
 */
const express = require("express");
const cors = require("cors");
const cfenv = require("cfenv");
const bodyParser = require('body-parser');

const app = express();

var ziggy;

app.use(cors());


app.use(bodyParser.urlencoded({extended: false}));


app.use(bodyParser.json());

app.post("/api/register", function (request, response) {
    const username = request.body.userName;
    const password = request.body.userPassword;

    console.log("received register request" + username + ":" + password);

    ziggy.find({ selector: {username: username} }, function (err, body) {
        if (!err && body.docs.length > 0) {
            response.json( false );
            return;
        }
        console.log(JSON.stringify(body));
        ziggy.insert({
            username: username,
            password: password,
            tags: [],
            sources: [],
        }, function(err, body, header) {
            if (err) {
                return console.log('[mydb.insert] ', err.message);
            }
            console.log(JSON.stringify(body));
            response.json( true );
        });
    });


});

app.get("/api/login", function (request, response) {
    const username = request.query.userName;
    const password = request.query.userPassword;

    console.log("received login request" + username + ":" + password);

    ziggy.find({ selector: {username: username} }, function (err, body) {
        console.log(JSON.stringify(body));
        if (!err && body.docs.length > 0 && body.docs[0].password === password) {
            response.json(true);
        } else {
            response.json(false);
        }
    });

});

app.get('/api/:username/source', function (request, response) {
    const username = request.param('username');
    ziggy.find({selector: {username: username}}, function (err, body) {
        if (!err) {
            response.json(body);
        }
    });
});

app.post('/api/:username/source', function (req, res) {
    const username = request.param('username');
    const sourceUrl = request.body.url;

});


// load local VCAP configuration  and service credentials
let vcapLocal;
try {
    vcapLocal = require('./vcap-local.json');
    console.log("Loaded local VCAP", vcapLocal);
} catch (e) { }

const appEnvOpts = vcapLocal ? { vcap: vcapLocal} : {}

const appEnv = cfenv.getAppEnv(appEnvOpts);

if (appEnv.services['cloudantNoSQLDB']) {
    // Load the Cloudant library.
    var Cloudant = require('cloudant');

    // Initialize database with credentials
    var cloudant = Cloudant(appEnv.services['cloudantNoSQLDB'][0].credentials);

    let dbName = 'ziggy';
    cloudant.db.create(dbName, function (err, data) {
        if (!err) //err if database doesn't already exists
            console.log("Created database: " + dbName);
    });

    ziggy = cloudant.db.use('ziggy');
}


const port = process.env.PORT || 3000;
app.listen(port, function() {
    console.log("To view your app, open this link in your browser: http://localhost:" + port);
});
