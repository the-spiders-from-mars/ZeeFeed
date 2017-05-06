/**
 * Created by zeling on 2017/5/6.
 */
const FeedParser = require('feedparser');
const request = require('request'); // for fetching the feed
const summary = require('node-summary');
const _ = require('underscore');
const NaturalLanguageUnderstandingV1 = require('watson-developer-cloud/natural-language-understanding/v1.js');

const nlu = new NaturalLanguageUnderstandingV1({
    username: "0db91844-fcf1-4cfb-9575-7b6a667ed1f2",
    password: "J5qwraJbMPuA",
    version_date: NaturalLanguageUnderstandingV1.VERSION_DATE_2017_02_27
});


function parseRss(url) {
    return new Promise(function(resolve, reject) {

        const req = request(url);
        const feedparser = new FeedParser();

        let ret = {
            name: undefined,
            url: url,
            logo: undefined,
            articles: []
        };

        req.on('error', function (error) {
            reject(error);
        });

        req.on('response', function (res) {
            var stream = this; // `this` is `req`, which is a stream

            if (res.statusCode !== 200) {
                this.emit('error', new Error('Bad status code'));
            }
            else {
                stream.pipe(feedparser);
            }
        });

        feedparser.on('error', function (error) {
            reject(error);
        });

        feedparser.on('readable', function () {
            // This is where the action is!
            const stream = this; // `this` is `feedparser`, which is a stream
            const meta = this.meta; // **NOTE** the "meta" is always available in the context of the feedparser instance
            let item;

            if (!ret.name) ret.name = meta.title;
            if (!ret.logo) ret.logo = meta.logo;

            while (item = stream.read()) {
                if (item.description === null) continue;
                nlu.analyze({
                    html: item.description,
                    features: {
                        concepts: {},
                    }
                }, function (err, response) {
                    if (err) {
                        reject(err);
                    } else {
                        let tags = _.pluck(response.concepts, 'text');
                        if (!item.summary) {
                            summary.summarize(item.title, item.description, function (err, sum) {
                                ret.articles.push({
                                    title: item.title,
                                    enclosures: item.enclosures,
                                    content: item.description,
                                    date: item.date,
                                    author: item.author || meta.author,
                                    tags: tags,
                                    summary: sum,
                                    link: item.link
                                });
                            });
                        } else {
                            ret.articles.push({
                                title: item.title,
                                enclosures: item.enclosures,
                                content: item.description,
                                date: item.date,
                                author: item.author || meta.author,
                                tags, tags,
                                summary: item.summary,
                                link: item.link
                            });
                        }
                    }
                });


            }
        });

        feedparser.on('end', function() {
            resolve(ret);
        })
    });
}


url_list = ["http://feeds.feedburner.com/techcrunch",
            "http://feeds.feedburner.com/elise/simplyrecipes",
            "http://feeds.feedburner.com/boingboing/ibag",
            "http://feeds.feedburner.com/Mashable",
            "http://feeds.feedburner.com/readwriteweb",
            "http://feeds.feedburner.com/JohnBattellesSearchblog",
            "http://feeds.feedburner.com/43Folders",
            "http://feeds.feedburner.com/37signals/beMH",
            "http://feeds.feedburner.com/DumbLittleMan",
            "http://feeds.feedburner.com/InterestingThingOfTheDay"];
/*
Promise.all(_.map(url_list, parseRss)).then(function (data) {
    console.log(data);
}, function (err) {
    console.log(err);
});
*/

parseRss('https://daringfireball.net/feeds/main').then(console.log);
