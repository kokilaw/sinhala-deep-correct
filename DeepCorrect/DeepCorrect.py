from seq2seq import build_model, infer


class DeepCorrect():
    deepcorrect_model = None

    def __init__(self, params_path, model_weights_path):
        # loading the model
        model, params = build_model(params_path)
        DeepCorrect.model = model
        DeepCorrect.params = params
        DeepCorrect.model.load_weights(model_weights_path)

    def correct(self, sentence, beam_size=1):
        if not DeepCorrect.deepcorrect_model:
            print('Please load the model first')

        sentence = sentence.strip()
        sentence = infer(
            sentence, DeepCorrect.model, DeepCorrect.params, beam_size=beam_size)

        return sentence
