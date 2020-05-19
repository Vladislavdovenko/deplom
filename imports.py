import numpy
import random
import time
import re

import numpy as np
import pickle
import langid

import tensorflow as tf
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from flask import Flask, request, jsonify
from langdetect import detect_langs, DetectorFactory, detect
from langid.langid import LanguageIdentifier, model as langid_model
from textblob import TextBlob
import translators as tr

from config import *
from web_config import host, port
from cmsDetector import start

DetectorFactory.seed = 0
symbol_batch = 600
words_limit = 100

with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
    model = load_model(model_name)

model.summary()
file = open(token_name, "rb")
tokenizer = pickle.load(file)
graph = tf.get_default_graph()


def makeObj(prediction):
    obj = obj_template
    res = []

    for category, predict in zip(categories_list, prediction):
        template = dict()
        template['key'] = category
        template['val'] = predict*100  # make value in percent%
        res.append(template)

    res = sorted(res, key=lambda k: k['val'], reverse=True)
    obj['res'] = res

    return obj
