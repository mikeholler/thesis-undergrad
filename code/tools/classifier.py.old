import random
from sys import argv
from nltk.classify import apply_features
import os
import json
import nltk

word_features = None
count = 0


def get_train_tuples(directory, words_fd=None):
    """ Get tuples of (item, label).
    """

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    tuples = list()

    for _file in files:

        with open(os.path.join(directory, _file), 'r') as f:
            paras = f.read().split('\n\n')

        # create a tuple per document
        word_list = list()
        for para in paras:
            para = para.strip()
            if para:  # only use paragraphs that contain text
                word_list += paragraph_to_words(para)

        if words_fd is not None:
            words_fd.update(word_list)

        label = _file[:-len('.txt')]  # remove extension
        t = (word_list, label,)
        tuples.append(t)

    return tuples


def get_test_tuples(directory):
    """ Get tuples of (item, label).
    """

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    tuples = list()

    for _file in files:

        label = _file[:-len('.txt')]  # remove extension

        with open(os.path.join(directory, _file), 'r') as f:
            paras = f.read().split('\n\n')

        # create a tuple per paragraph per document
        for para in paras:
            para = para.strip()
            if para:  # only use paragraphs that contain text
                t = (paragraph_to_words(para), label,)
                tuples.append(t)

    return tuples


def paragraph_to_words(para):
    paragraph_sents = nltk.sent_tokenize(para)

    paragraph_words = list()
    for sent in paragraph_sents:
        paragraph_words += nltk.word_tokenize(sent)

    return paragraph_words


def paragraph_features(paragraph):
    global count
    count += 1
    print '\r', count,

    paragraph_words = set(paragraph)

    features = dict()
    for word in word_features:
        features[word_features[word]] = (word in paragraph_words)

        # if word in paragraph_words:
        #     print word

    # print json.dumps(features, indent=2)

    return features


def classify(training_set, test_set):
    training_set = apply_features(paragraph_features, training_set)
    test_set = apply_features(paragraph_features, test_set)

    print '\nTraining...'
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    global count
    count = 0

    print '\nTesting...'

    results = nltk.classify.accuracy(classifier, test_set)

    print '\nAccuracy:', results


def main():
    wiki_dir = argv[1]
    index_dir = argv[2]
    index_to_wiki_file = argv[3]

    with open(index_to_wiki_file, 'r') as f:
        index_to_wiki = json.loads(f.read())

    words_fd = nltk.FreqDist()  # we should do this only for the wiki training set

    wiki_tuples = get_train_tuples(wiki_dir, words_fd)

    print 'keys', len(words_fd.keys())
    # exit()

    # python ../../tools/classifier.py wiki-txt/ biology-txt/ indexToWiki.json

    # separate paragraphs (don't concatenate it)
    index_tuples = get_test_tuples(index_dir)


    # for t in wiki_tuples:
    #     print '{0}:\t{1}'.format(t[1], t[0][:40])

    # for t in index_tuples:
    #     print '{0}:\t{1}'.format(t[1], t[0][:40])

    # Convert index labels to wikipedia titles.
    tmp = list()
    for t in index_tuples:
        try:
            t = (t[0], index_to_wiki[t[1]],)
        except KeyError:
            print 'KeyError:', t[1]

        tmp.append(t)
        # print t[1], '\t', t[0][:40]

    index_tuples = tmp

    global word_features
    word_features = dict()
    # word_features = words_fd.keys()[:2000]  # NLTKwP p.228
    word_feature_keys = random.sample(words_fd.keys(), 500)  # Pick 2000 words at random from our set

    for i, k in enumerate(word_feature_keys):
        word_features[k] = i  # so the first item starts at 1

    classify(wiki_tuples, index_tuples)


if __name__ == '__main__':
    main()