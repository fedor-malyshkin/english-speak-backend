# -*- coding: UTF-8 -*-

from random import sample

from flask import Flask
from flask import request
from flask.json import jsonify
from flask_cors import CORS

from english_speak_backend.storage import builder

app = Flask(__name__)
CORS(app)

grammar_data = builder.json_file("data/grammar_rules.json")
murphy_data = builder.flat_file("data/murphy.list")
phrasal_verbs_data = builder.json_file("data/phrasal_verbs.json")
verbs_with_prep_data = builder.json_file("data/verbs_with_prep.json")
expression_data = builder.flat_file_pairs("data/expressions.list")
topics_q1_question_data = builder.flat_file_map("data/questions1.txt", "---")
topics_q23_question_data = builder.flat_file_map("data/questions23.txt", "---")
interview_question_data = builder.flat_file_map("data/interview.txt", "---")
random_words_data = builder.flat_file("data/random_words.list")
conv_exp_data = builder.json_file("data/conversation_exp.json")


@app.route('/interview/random')
def interview():
    key = sample(interview_question_data.keys(), 1)[0]
    return jsonify(builder.wrap_flat_records(interview_question_data[key].get_all()))


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


@app.route('/verbs_with_prepositions')
def verbs_with_prepositions():
    count = int(request.args.get('count', '5'))
    return jsonify(verbs_with_prep_data.get_exact_part(count))


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


@app.route('/random_words')
def random_words():
    count = int(request.args.get('count', '7'))
    return jsonify(random_words_data.get_exact_part(count))


@app.route('/conversation_expressions')
def conversation_expressions():
    count = int(request.args.get('count', '5'))
    return jsonify(conv_exp_data.get_exact_part(count))
