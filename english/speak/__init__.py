# -*- coding: UTF-8 -*-

from random import sample

from flask import Flask
from flask import request
from flask.json import jsonify
from flask_cors import CORS

from english.speak.storage import builder

# from flask_restx import Api

app = Flask(__name__)
CORS(app)
# api = Api(app, version='0.1', title='English study API',
#           description='Tiny API for english studying with a '
#                       'set of grammar rules, phrasal verbs and IELTS themes',
#           )

grammar_data = builder.json_file("data/grammar_rules.json")
murphy_data = builder.flat_file("data/murphy.list")
phrasal_verbs_data = builder.flat_file_pairs("data/phrasal_verbs.list", builder.phrasal_verb_record_transformer)
expression_data = builder.flat_file_pairs("data/expressions.list", builder.dumb_transformer)
topics_q1_question_data = builder.flat_file_map("data/questions1.txt", "---")
topics_q23_question_data = builder.flat_file_map("data/questions23.txt", "---")


@app.route('/topics_q1/random')
def topics_q1():
    return jsonify(builder.wrap_flat_records(sample(topics_q1_question_data.keys(), 1)))


@app.route('/topics_q23/random')
def topics_q23():
    return jsonify(builder.wrap_flat_records(sample(topics_q23_question_data.keys(), 1)))


@app.route('/topics_q1/<string:topic_value>')
def topic_q1_questions(topic_value):
    return jsonify(builder.wrap_flat_records(topics_q1_question_data[topic_value].get_all()))


@app.route('/topics_q23/<string:topic_value>')
def topic_q23_questions(topic_value):
    return jsonify(builder.wrap_flat_records(topics_q23_question_data[topic_value].get_all()))


@app.route('/topics_q1/<string:topic_value>/vocabulary')
def topic_q1_vocabulary(topic_value):
    topic_q1_vocabulary_data = builder.flat_file("data/topics_q1/{0}.list".format(topic_value))
    return jsonify(topic_q1_vocabulary_data.get_exact_part(7))


@app.route('/topics_q23/<string:topic_value>/vocabulary')
def topic_q23_vocabulary(topic_value):
    topic_q23_vocabulary_data = builder.flat_file("data/topics_q23/{0}.list".format(topic_value))
    return jsonify(topic_q23_vocabulary_data.get_exact_part(7))


@app.route('/phrasal_verbs')
def phrasal_verbs():
    count = int(request.args.get('count', '5'))
    return jsonify(phrasal_verbs_data.get_exact_part(count))


@app.route('/grammar')
def grammar():
    count = int(request.args.get('count', '4'))
    return jsonify(grammar_data.get_exact_part(count))


@app.route('/murphy')
def murphy():
    count = int(request.args.get('count', '4'))
    return jsonify(murphy_data.get_exact_part(count))


@app.route('/expressions')
def expressions():
    count = int(request.args.get('count', '5'))
    return jsonify(expression_data.get_exact_part(count))
