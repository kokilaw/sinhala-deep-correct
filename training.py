from pre_process import *
from seq2seq import *

from keras.utils import Sequence
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split


class MY_Generator(Sequence):

    def __init__(self, input_data, output_data, batch_size):
        self.input_data, self.output_data = input_data, output_data
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.input_data) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_X = self.input_data[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.output_data[idx * self.batch_size:(idx + 1) * self.batch_size]

        return convert_training_data(batch_X, batch_y, params)


if __name__ == "__main__":
    # reading sentences from the file
    pairs = prepare_data("./data/all_corpus_sentence_pairs_v6.txt")
    input_data = [row[0] for row in pairs]
    output_data = [row[1] for row in pairs]

    # splitting sentence pairs into training and test
    X_train, X_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.1, random_state=42)

    # building params
    build_params(input_data=X_train, output_data=y_train,
                 params_path='./checkpoints/params', max_lengths=(200, 200))

    # building model
    model, params = build_model(params_path='./checkpoints/params')

    batch_size = 128
    num_of_epochs = 200

    my_training_batch_generator = MY_Generator(X_train, y_train, batch_size)
    my_validation_batch_generator = MY_Generator(X_test, y_test, batch_size)

    checkpoint_path = "./checkpoints/checkpoint.h5"

    checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)

    callbacks_list = [checkpoint, es]

    # training
    history = model.fit_generator(generator=my_training_batch_generator,
                                  steps_per_epoch=(len(X_train) // batch_size),
                                  epochs=num_of_epochs,
                                  verbose=1,
                                  validation_data=my_validation_batch_generator,
                                  validation_steps=(len(X_test) // batch_size),
                                  max_queue_size=32,
                                  callbacks=callbacks_list)

    model.save_weights('./checkpoints/checkpoint_weights.h5')
