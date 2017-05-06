/**
 * Created by zeling on 2017/5/6.
 */
const express = require("express");
const cors = require("cors");
const cfenv = require("cfenv");
const bodyParser = require('body-parser');
const feedParser = require('feedparser');
const _ = require('underscore');
const req = require('request');

const app = express();

var ziggy;
var timer;

app.use(cors());


app.use(bodyParser.urlencoded({extended: false}));


app.use(bodyParser.json());

app.post("/api/register", function (request, response) {
    const username = request.body.userName;
    const password = request.body.userPassword;

    console.log("received register request" + username + ":" + password);

    ziggy.get(username, function (err, body) {
        console.log(JSON.stringify(body));

        if (!err || !(err.statusCode == 404)) {
            console.log(err);
            console.log(body);
            response.json( false );
            return;
        }

        ziggy.insert({
            _id: username,
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

    ziggy.get(username, function (err, body) {
        console.log(JSON.stringify(body));
        if (!err && body.password === password) {
            response.json(true);
        } else {
            response.json(false);
        }
    });

});

app.get('/api/tag', function (request, response) {
    const username = request.params.userName;
    if (!username) response.status().send("Sorry");
    ziggy.get(username, function (err, body) {
        if (err) {
            response.status(500).send("Internal Error");
        } else if (!body) {
            response.state(400).send("")
        } else {
            let ret = [];
            for (let tag of body.tags) {
                let cnt = 0;
                for (let article of body.sources.article) {
                    if (article.tags.includes(tag) && !article.read) {
                        ++cnt;
                    }
                }
                ret.push({tagName: tag, tagCount: /*cnt*/ 10 + Math.floor(Math.random() * 11) });
            }
            response.json(ret);
        }
    });
});

// setInterval(function() {console.log("hello"); }, 100000);

app.get('/api/sources', function (request, response) {
    const username = request.query.userName;
    ziggy.get(username, function (err, body) {
        if (!err && body) {
            response.json( _.map(body.sources, function (source) {
                return {
                    url: source.url,
                    name: source.name,
                    logo: source.logo
                }
            } ));
        } else {
            response.state(404).send("sth wrong");
        }
    });
});

app.get('/api/blog', function (request, response) {
    let username = request.params.userName;
    let tagname = request.params.tagName;
    ziggy.get(username, function (err, body) {
        if (err) {
            response.status(500).send("Internal Error");
        } else if (!body) {
            response.state(400).send("")
        } else {
            let ret = [];
            for (let tag of body.tags) {
                let cnt = 0;
                for (let article of body.sources.article) {
                    if (article.tags.includes(tag)) {
                        ret.push(article);
                    }
                }
            }
            response.json(ret);
        }
    });
});

app.post('/api/:username/sources', function (request, response) {
    const username = request.params.username;
    const sourceUrls = request.body.urls;
    ziggy.get(username, function (err, user) {
        if (!err && user) {
            const diff = _.difference(_.pluck(user.sources, 'url'), sourceUrls);
            req.post('http://'/* fixme */, function (err, res, body) {
                if (!err && body) {
                    user.sources += _.object(['url', 'articles', 'logo', 'name'], diff, body.articles, body.articles.logo, body.name);
                    ziggy.insert(user, function (err, r) {
                        if (!err) {
                            console.log(r);
                            response.json(true);
                        } else {
                            response.json(false);
                        }
                    });
                }
            });
        } else {
            response.state(404).send("sth wrong");
        }
    });
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
