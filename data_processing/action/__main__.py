# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    OpenWhisk python action
"""
import json
from time import strftime
import pdb

import feedparser
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

__author__ = "freemso"

LANGUAGE = "english"
NUM_SUMMARY_SENTENCE = 3

BLUEMIX_USER_NAME = "0db91844-fcf1-4cfb-9575-7b6a667ed1f2"
BLUEMIX_USER_PASS = "J5qwraJbMPuA"
BLUEMIX_VERSION = "2017-02-27"


class Article:
    def __init__(self, title, link, author, date, content, logo,
                 enclosures=None):
        self.title = title
        self.link = link
        self.author = author
        self.date = date
        self.content = content
        self.logo = logo
        self.enclosures = enclosures


def main(args):
    # parse args to get input
    source_urls = args.get("sources")
    feed_data_list = get_feed_data(source_urls)
    print(len(feed_data_list))
    result = []
    for feed_name, feed_data in feed_data_list.items():
        articles = []
        for item in feed_data[0:2]:
            content = item.content
            title = item.title
            link = item.link
            author = item.author
            date = item.date
            logo = item.logo
            enclosures = item.enclosures
            feature_dict = get_features(content)
            tag_set = set()
            for concept in feature_dict["concepts"]:
                tag_set.add(concept["text"])
            summary = get_summary(content)
            article = {
                "content": content,  # a html string
                "tags": list(tag_set),  # a list of tags(str)
                "summary": summary,  # a plain text string
                "title": title,  # a plain text
                "date": date,  # a string
                "author": author,  # a string
                "link": link,  # an url
                "logo": logo,  # an url
                "enclosures": enclosures  # not used
            }
            articles.append(article)
        source = {
            "articles": articles,  # article list
            "name": feed_name,  # plain text
        }
        print(json.dumps(source, indent=2))
        result.append(source)
    return result


def get_summary(article, url=False, num_sentence=NUM_SUMMARY_SENTENCE):
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

    summ_sents = summarizer(parser.document, num_sentence)
    summary = " ".join([str(s).strip() for s in summ_sents])

    return summary


def get_features(html):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=BLUEMIX_VERSION,
        username=BLUEMIX_USER_NAME,
        password=BLUEMIX_USER_PASS)

    feature_dict = natural_language_understanding.analyze(
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
    return feature_dict
    # print(json.dumps(features, indent=2))


def get_feed_data(sources):
    feed_data_list = {}
    for source in sources:
        feed = feedparser.parse(source)
        # Feed Element
        feed_data = []  # data is a list of Articles
        feed_logo = feed.feed.get('image', None)
        if feed_logo is not None:
            feed_logo = feed_logo["href"]
        feed_name = feed.feed.title

        # Entry Element
        for entry in feed.entries[0:10]:
            title = entry.title
            link = entry.link
            author = entry.get('author', feed_name)
            date = strftime('%Y.%m.%d.%H.%M.%S', entry.published_parsed)
            content = entry.get('content', None)
            if content is None:
                continue
                # TODO summary_details
            content = content[0]["value"]
            logo = feed_logo
            if hasattr(feed, 'enclosures') and len(feed.enclosures) > 0:
                article = Article(title, link, author, date, content, logo,
                                  feed.enclosures)
            else:
                article = Article(title, link, author, date, content, logo)
            feed_data.append(article)
        feed_data_list[feed_name] = feed_data
    return feed_data_list
