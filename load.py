from deep_correct import DeepCorrect


def init(param_file_path='./checkpoints/params', weights_file_path='./checkpoints/checkpoint_weights.h5'):
    corrector = DeepCorrect(param_file_path, weights_file_path)
    return corrector, corrector.model, corrector.params
