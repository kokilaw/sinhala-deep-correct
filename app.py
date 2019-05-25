import re
import sys
import os

from load import init
from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin

import kenlm

from pre_process import normalize_string
from utils import tokenize_sinhala_text

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

global corrector, model, params

# Building and loading the keras model, params file contains the encoding/decoding dictionaries.
corrector, model, params = init()
ngramModel = kenlm.LanguageModel('./lm/sinhala_lm.binary')

regexp = re.compile(r'[^\u0D80-\u0DFF.!?,\s\u200d]')


def valid_sinhala_sentence(sentence):
    if not sentence:
        return False
    elif sentence == '':
        return False
    elif regexp.search(sentence):
        return False
    else:
        return True


def ngram_score_calculation(sentence):
    ngramScore = ngramModel.score(sentence['suggestion'])
    return {
        'suggestion': sentence['suggestion'],
        'grammarModelProb': sentence['grammarModelProb'],
        'ngramScore': ngramScore
    }


def get_corrections(sentence, useBeamSearch=False, beamSize=3, useNgramScore=False):
    normalized_sentence = normalize_string(sentence)
    normalized_sentence = normalized_sentence.strip()
    corrections = {}
    corrections["sentence"] = normalized_sentence
    if useBeamSearch:

        corrections['results'] = corrector.get_beam_search_corrections(
            normalized_sentence, beamSize)

        if useNgramScore:
            corrections['results'] = list(map(ngram_score_calculation, corrections['results']))
            corrections['attributeAffected'] = "grammarModelProb"
            if corrections['results'][0]['grammarModelProb'] <= 0.71:
                corrections['results'].sort(key=lambda x: x['ngramScore'], reverse=True)
                corrections['attributeAffected'] = "ngramScore"

        corrections['isCorrect'] = corrections['results'][0]["suggestion"] == normalized_sentence
    else:
        corrections['results'] = [{
            "suggestion": corrector.get_greedy_search_correction(
                normalized_sentence),
            "probability": None
        }]
        corrections['isCorrect'] = corrections['results'][0]["suggestion"] == normalized_sentence

    return corrections


@app.route('/')
def index():
    return 'Sinhala-Deep-Grammar Rest API'


@app.route('/api/correct', methods=['POST'])
@cross_origin()
def correct():
    if request.is_json:
        request_data = request.get_json()
        print(request_data)

        if 'sentence' in request_data.keys() and valid_sinhala_sentence(request_data['sentence']):
            sentence = request_data['sentence']
            useBeamSearch = request_data['useBeamSearch'] if 'useBeamSearch' in request_data.keys(
            ) else False
            useNgramScore = request_data['useNgramScore'] if 'useNgramScore' in request_data.keys(
            ) else False
            corrections = get_corrections(
                sentence, useBeamSearch=useBeamSearch, useNgramScore=useNgramScore)
            corrections['useBeamSearch'] = useBeamSearch
            corrections['useNgramScore'] = useNgramScore
            return jsonify(corrections)
        else:
            abort(422, "Unsupported argument. Invalid Sinhala sentence type.")

        return jsonify(request_data)
    else:
        abort(400, "Invalid JSON request")


@app.route('/api/correct/paragraph', methods=['POST'])
@cross_origin()
def correct_paragraph():
    if request.is_json:
        request_data = request.get_json()
        print(request_data)

        if 'text' in request_data.keys() and valid_sinhala_sentence(request_data['text']):
            text = request_data['text']
            useBeamSearch = request_data['useBeamSearch'] if 'useBeamSearch' in request_data.keys(
            ) else False
            useNgramScore = request_data['useNgramScore'] if 'useNgramScore' in request_data.keys(
            ) else False
            sentences = tokenize_sinhala_text(text)

            sentence_corrections = []

            for sentence in sentences:
                corrections = get_corrections(
                    sentence, useBeamSearch=useBeamSearch, useNgramScore=useNgramScore)
                sentence_corrections.append(corrections)

            evaluation = {'useBeamSearch': useBeamSearch, 'useNgramScore': useNgramScore,
                          "sentences": sentence_corrections}

            return jsonify(evaluation)
        else:
            abort(422, "Unsupported argument. Invalid Sinhala sentence type.")

        return jsonify(request_data)
    else:
        abort(400, "Invalid JSON request")


if __name__ == "__main__":
    # decide what port to run the app in
    # port = int(os.environ.get('PORT', 5000))
    port = int(os.environ.get('PORT', 80))
    # run the app locally on the givn port
    # app.run(host='0.0.0.0', port=port)
    # optional if we want to run in debugging mode
    # app.run(debug=True)
    app.run()
