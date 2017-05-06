# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    OpenWhisk python action
"""
import json
from time import strftime

import feedparser
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

from Article import Article

__author__ = "freemso"

LANGUAGE = "english"
NUM_SUMMARY_SENTENCE = 3

BLUEMIX_USER_NAME = "0db91844-fcf1-4cfb-9575-7b6a667ed1f2"
BLUEMIX_USER_PASS = "J5qwraJbMPuA"
BLUEMIX_VERSION = "2017-02-27"


def main(args):
    # parse args to get input
    sources = args.get("sources", ["https://daringfireball.net/feeds/main"])
    feed_data_list = get_feed_data(sources)
    return json.dumps({"name": "freemso"}, indent=2)


def get_summary(article, url=False):
    """
    get the summary of one article
    :param article: html string of the article or the url of the article
    :param url: True is article is an url
    :return: the summary of the article as string
    """
    if url:
        parser = HtmlParser.from_url(article, tokenizer=Tokenizer(LANGUAGE))
    else:
        parser = HtmlParser.from_string(article, tokenizer=Tokenizer(LANGUAGE), url=None)
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summ_sents = summarizer(parser.document, NUM_SUMMARY_SENTENCE)
    summary = " ".join([s.strip() for s in summ_sents])

    return summary


def get_features(html):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=BLUEMIX_VERSION,
        username=BLUEMIX_USER_NAME,
        password=BLUEMIX_USER_PASS)

    feature_list = natural_language_understanding.analyze(
        html=html,
        features=[
            features.Concepts(),  # keep
            # features.Entities(emotion=True, sentiment=True),
            # features.Keywords(emotion=True, sentiment=True),
            # features.Categories(),
            # features.Emotion(document=True),
            # features.MetaData(),
            # features.SemanticRoles(entities=True, keywords=True),
            # features.Relations(),
            # features.Sentiment(document=True)
        ])
    return feature_list
    # print(json.dumps(features, indent=2))


def get_feed_data(sources):
    feed_data_list = {}
    for source in sources:
        feed = feedparser.parse(source)
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
            if hasattr(feed, 'enclosures') and len(feed.enclosures) > 0:
                article = Article(title, link, author, date, content, img,
                                  feed.enclosures)
            else:
                article = Article(title, link, author, date, content, img)
            feed_data.append(article)
        feed_data_list[feed_name] = feed_data
    return feed_data_list
