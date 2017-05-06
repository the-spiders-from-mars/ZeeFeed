import feedparser
from time import strftime
from Article import Article

url_list = ["http://feeds.feedburner.com/techcrunch",
            "http://feeds.feedburner.com/elise/simplyrecipes",
            "http://feeds.feedburner.com/boingboing/ibag",
            "http://feeds.feedburner.com/Mashable",
            "http://feeds.feedburner.com/readwriteweb",
            "http://feeds.feedburner.com/JohnBattellesSearchblog",
            "http://feeds.feedburner.com/43Folders",
            "http://feeds.feedburner.com/37signals/beMH",
            "http://feeds.feedburner.com/DumbLittleMan",
            "http://feeds.feedburner.com/InterestingThingOfTheDay"]

data_list = {}

for url in url_list:
    feed = feedparser.parse(url)
    # Feed Element
    feed_data = []
    feed_img = feed.feed.get('image', None)
    feed_name = feed.feed.title

    # Entry Element
    for entry in feed.entries:
            title = entry.title
            link = entry.link
            author = entry.get('author', feed_name)
            date = strftime('%Y.%m.%d', entry.published_parsed)
            content = entry.get('content', None)
            img = feed_img
            article = None
            if hasattr(feed, 'enclosures') and len(feed.enclosures) > 0:
                article = Article(title, link, author, date, content, img,
                                  feed.enclosures)
            else:
                article = Article(title, link, author, date, content, img)
            feed_data.append(article)
    data_list[feed_name] = feed_data

for feed_name, feed_data in data_list.items():
    print (feed_name)
    for para in feed_data:
        print (para.__dict__)
    print ("")
