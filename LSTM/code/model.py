from __future__ import print_function

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file

import numpy as np
import random
import sys
import os

if __name__ == "__main__":

    all_folders = "../levels_transposed/"
    result_path = "../levels_prediction_textfiles/"
    original_level_path = all_folders + sys.argv[1]  

    try: 
        text = open(original_level_path).read().lower()
    except UnicodeDecodeError:
        import codecs
        text = codecs.open(original_level_path, encoding='utf-8').read().lower()

    chars = set(text)
    words = set(open(original_level_path).read().lower().split())

    word_indices = dict((c, i) for i, c in enumerate(words))
    indices_word = dict((i, c) for i, c in enumerate(words))

    maxlen = 30
    step = 3
    print("maxlen:",maxlen,"step:", step)
    sentences = []
    next_words = []
    next_words= []
    sentences1 = []
    list_words = []

    sentences2=[]
    list_words=text.lower().split()


    for i in range(0,len(list_words)-maxlen, step):
        sentences2 = ' '.join(list_words[i: i + maxlen])
        sentences.append(sentences2)
        next_words.append((list_words[i + maxlen]))


    # print('Vectorization...')
    X = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
    y = np.zeros((len(sentences), len(words)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, word in enumerate(sentence.split()):
            #print(i,t,word)
            X[i, t, word_indices[word]] = 1
        y[i, word_indices[next_words[i]]] = 1


    #build the model: 2 stacked LSTM
    # print('Build model...')
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, len(words))))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(len(words)))
    #model.add(Dense(1000))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    if os.original_level_path.isfile('GoTweights'):
        model.load_weights('GoTweights')

    def sample(a, temperature=1.0):
        # helper function to sample an index from a probability array
        a = np.log(a) / temperature
        a = np.exp(a) / np.sum(np.exp(a))
        return np.argmax(np.random.multinomial(1, a, 1))

    # train the model, output generated text after each iteration
    for iteration in range(1, 300):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        model.fit(X, y, batch_size=64, nb_epoch=2)
        #model.save_weights('GoTweights',overwrite=True)

        start_index = random.randint(0, len(list_words) - maxlen - 1)
        predictionText = open(result_path + os.original_level_path.splitext(sys.argv[1])[0] + "_new_"+str(iteration)+".txt", "w+") 
        loop_range = [1.0,1.2]
        for diversity in loop_range:
            print()
            print('----- diversity:', diversity)
            generated = ''
            sentence = list_words[start_index: start_index + maxlen]
            generated += ' '.join(sentence)
            print('----- Generating with seed: "' , sentence , '"')
            print()
            sys.stdout.write(generated)
            print()

            for i in range(1024):
                x = np.zeros((1, maxlen, len(words)))
                for t, word in enumerate(sentence):
                    x[0, t, word_indices[word]] = 1.

                preds = model.predict(x, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_word = indices_word[next_index]
                generated += next_word
                predictionText.write(next_word+"\n")
                del sentence[0]
                sentence.append(next_word)
                sys.stdout.write(' ')
                sys.stdout.write(next_word)
                sys.stdout.flush()
            print()


