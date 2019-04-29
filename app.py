from load import init
from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin

import re
import sys
import os

from pre_process import normalize_string

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

global corrector, model, params
corrector, model, params = init()

regexp = re.compile(r'[^\u0D80-\u0DFF.!?\s\u200d]')


def valid_sinhala_sentence(sentence):
    if not sentence:
        return False
    elif sentence == '':
        return False
    elif regexp.search(sentence):
        return False
    else:
        return True


def get_corrections(sentence, useBeamSearch=False, beamSize=3):
    normalized_sentence = normalize_string(sentence)
    normalized_sentence = normalized_sentence.strip()
    corrections = {}
    if useBeamSearch:
        corrections['results'] = corrector.get_beam_search_corrections(
            normalized_sentence, beamSize)
        corrections['useBeamSearch'] = useBeamSearch
    else:
        corrections['results'] = [{
            "sequence": corrector.get_greedy_search_correction(
                normalized_sentence),
            "probability": None
        }]
        corrections['useBeamSearch'] = useBeamSearch

    return corrections


@app.route('/correct', methods=['POST'])
@cross_origin()
def correct():
    if request.is_json:
        request_data = request.get_json()
        print(request_data)

        if 'sentence' in request_data.keys() and valid_sinhala_sentence(request_data['sentence']):
            sentence = request_data['sentence']
            useBeamSearch = request_data['useBeamSearch'] if 'useBeamSearch' in request_data.keys(
            ) else False
            corrections = get_corrections(
                sentence, useBeamSearch=useBeamSearch)
            return jsonify(corrections)
        else:
            abort(422, "Invalid Sinhala Sentece")

        return jsonify(request_data)
    else:
        abort(400, "Invalid JSON request")


if __name__ == "__main__":
    # decide what port to run the app in
    port = int(os.environ.get('PORT', 5000))
    # run the app locally on the givn port
    app.run(host='0.0.0.0', port=port)
    # optional if we want to run in debugging mode
    # app.run(debug=True)
