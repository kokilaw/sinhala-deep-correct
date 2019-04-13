from seq2seq import build_model, infer, infer_greedy


class DeepCorrect():
    model = None
    params = None

    def __init__(self, params_path, model_weights_path):
        # loading the model
        model, params = build_model(params_path)
        DeepCorrect.model = model
        DeepCorrect.params = params
        DeepCorrect.model.load_weights(model_weights_path)

    def get_corrections_with_probability(self, sentence, beam_size=1):

        if not DeepCorrect.model:
            print('Please load the model')
        elif not DeepCorrect.params:
            print('Please load the params file')

        sentence = sentence.strip()
        sentence = infer(
            sentence, DeepCorrect.model, DeepCorrect.params, beam_size=beam_size)

        return sentence

    def get_correction(self, sentence):
        if not DeepCorrect.model:
            print('Please load the model')
        elif not DeepCorrect.params:
            print('Please load the params file')

        sentence = sentence.strip()
        sentence = infer_greedy(
            sentence, DeepCorrect.model, DeepCorrect.params)

        return sentence
