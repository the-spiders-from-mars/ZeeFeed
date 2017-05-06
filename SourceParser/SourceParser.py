import feedparser
from time import strftime
from Article import Article
from Video import Video

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
        if hasattr(feed, 'enclosures') and len(feed.enclosures) > 0:
            enclosure = feed.enclosures[0]
            e_type = enclosure["type"]
            length = enclosure["length"]
            href = enclosure["href"]
            video = Video(e_type, length, href)
            feed_data.append(video)
        else:
            title = entry.title
            link = entry.link
            author = entry.get('author', feed_name)
            date = strftime('%Y.%m.%d', entry.published_parsed)
            content = entry.get('content', None)
            img = feed_img
            article = Article(title, link, author, date, content, img)
            feed_data.append(article)
    data_list[feed_name] = feed_data

for feed_name, feed_data in data_list.items():
    print (feed_name)
    for para in feed_data:
        print (para.__dict__)
    print ("")
