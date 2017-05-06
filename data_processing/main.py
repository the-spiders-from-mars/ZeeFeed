# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    
"""
import json

import feedparser
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import config

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username=config.BLUEMIX_USER_NAME,
    password=config.BLUEMIX_USER_PASS)

__author__ = "freemso"


def get_tags(html):
    response = natural_language_understanding.analyze(
        html=html,
        features=[
            # features.Concepts(), # keep
            # features.Entities(emotion=True, sentiment=True),
            # features.Keywords(emotion=True, sentiment=True),
            # features.Categories(),
            # features.Emotion(document=True),
            # features.MetaData(),
            # features.SemanticRoles(entities=True, keywords=True),
            # features.Relations(),
            # features.Sentiment(document=True)
        ])
    print(json.dumps(response, indent=2))


LANGUAGE = "english"
SENTENCES_COUNT = 3


def get_summary(html):
    parser = HtmlParser.from_string(html, tokenizer=Tokenizer(LANGUAGE), url=None)
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)


if __name__ == '__main__':
    feed = feedparser.parse("https://daringfireball.net/feeds/main")
    item = feed["items"][0]
    # print(item)
    content_html = item["content"][0]["value"]
    print("#############CONTENT#############")
    print(content_html)
    # print("############TAG#################")
    # get_tags(content)
    print("###############SUMMARY##########")
    get_summary(content_html)
