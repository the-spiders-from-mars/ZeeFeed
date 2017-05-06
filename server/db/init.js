/**
 * Created by zeling on 2017/5/6.
 */

var cloudant = require('./db.js').cloudant;


for (let dbName of ['users', 'articles']) {
    cloudant.db.create(dbName, function (err) {
        if (err) throw err;
        console.log("Successfully created database " + dbName);
    });
}

