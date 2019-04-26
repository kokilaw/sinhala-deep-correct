from seq2seq import infer_greedy
from load import init
from pre_process import *


def evaluate(input_sentences, output_sentences, model, params):
    correct_predictions = 0
    incorrect_predictions = 0
    for i in range(len(input_sentences)):
        input_sentence = input_sentences[i]
        output_sentence = output_sentences[i]
        predicted_sentence = infer_greedy(input_sentence, model, params)
        print('>', input_sentence)
        print('=', output_sentence)
        if output_sentence == predicted_sentence:
            correct_predictions += 1
            print('<', predicted_sentence)
        else:
            incorrect_predictions += 1
            print('[WRONG] <', predicted_sentence)
        print('')
    return correct_predictions, incorrect_predictions


# Calculating accuracy of the model
def percentage(part, whole):
    return 100 * float(part) / float(whole)


if __name__ == "__main__":
    corrector, model, params = init()

    eval_pairs = prepare_data("./data/all_corpus_sentence_pairs_v6_evaluation.txt")
    input_eval_data = [row[0] for row in eval_pairs]
    output_eval_data = [row[1] for row in eval_pairs]

    correct_predictions, incorrect_predictions = evaluate(input_eval_data, output_eval_data, model, params)

    percentage_value = percentage(correct_predictions, correct_predictions + incorrect_predictions)
    print("Accuracy of the model based on parsed test set is %d.2f percent" % percentage_value)
