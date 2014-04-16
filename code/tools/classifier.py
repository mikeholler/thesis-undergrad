import random
from sys import argv
from nltk.classify import apply_features
import os
import json
import nltk

# How to run this script:
# python classifier.py /path/to/wiki-text/ \
#                      /path/to/book-txt/ \
#                      /path/to/indexToWiki.json

word_features = None

word_feat_contains_fd = nltk.FreqDist()
word_feat_first_sent_fd = nltk.FreqDist()
word_feat_first_word_in_sent_fd = nltk.FreqDist()

count = 0

TECHNIQUE_RANDOM = 1
TECHNIQUE_MOST_FREQUENT = 2
TECHNIQUE_LEAST_FREQUENT = 3

FEAT_CONTAINS = 1
FEAT_FIRST_SENT = 2
FEAT_BEGIN_SENT = 3
FEAT_LINKED_TITLES = 4


def get_train_tuples(directory):
    """ Get tuples of (item, label).
    """

    files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    tuples = list()

    for _file in files:
    
        path = os.path.join(directory, _file)
        
        with open(path, 'r') as f:
            text = f.read()

            if CASE_SENSITIVE:
                pass
            else:
                text = text.lower()

            paras = text.split('\n\n')

        # create a tuple per paragraph
        for para in paras:
            para = para.strip().replace('\n', ' ')

            if para:
                # only use paragraphs that contain text
                sents = nltk.sent_tokenize(para)

                if word_feat_contains_fd is not None:
                    word_feat_contains_fd.update(
                        sents_to_words(sents)
                    )

                word_feat_first_sent_fd.update(
                    nltk.word_tokenize(sents[0])
                )

                for sent in sents:
                    words = nltk.word_tokenize(sent)
                    word_feat_first_word_in_sent_fd.inc(
                        words[0]
                    )

                # remove extension
                label = _file[:-len('.txt')]
                
                t = (sents, label,)
                tuples.append(t)

    return tuples


def get_test_tuples(directory):
    """ Get tuples of (item, label).
    """

    files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    tuples = list()

    for _file in files:

        label = _file[:-len('.txt')]  # remove extension

        path = os.path.join(directory, _file)

        with open(path, 'r') as f:
            text = f.read()

            if CASE_SENSITIVE:
                pass
            else:
                text = text.lower()

            paras = text.split('\n\n')

        # create a tuple per paragraph per document
        for para in paras:
            para = para.strip().replace('\n', ' ')
            if para:
                # only use paragraphs that contain text
                t = (nltk.sent_tokenize(para), label,)
                tuples.append(t)

    return tuples


def sents_to_words(sents):
    # paragraph_sents = nltk.sent_tokenize(para)
    #
    paragraph_words = list()
    for sent in sents:
        paragraph_words += nltk.word_tokenize(sent)

    return paragraph_words


def paragraph_features(paragraph_sents):
    global count
    count += 1
    print '\r', count,

    if FEATURE == FEAT_CONTAINS:
        paragraph_words = set(
            sents_to_words(paragraph_sents)
        )
    elif FEATURE == FEAT_LINKED_TITLES:
        paragraph_words = ' '.join(paragraph_sents)
    elif FEATURE == FEAT_FIRST_SENT:
        paragraph_words = nltk.word_tokenize(
            paragraph_sents[0]
        )
    elif FEATURE == FEAT_BEGIN_SENT:
        paragraph_words = {
            nltk.word_tokenize(sent)[0]
            for sent in paragraph_sents
        }
    else:
        paragraph_words = None
        print 'FEATURE NOT SUPPORTED'
        exit()

    features = dict()
    for word in word_features:
        features[word_features[word]] = (
            word in paragraph_words
        )

    return features


def classify(training_set, test_set):
    training_set = apply_features(
        paragraph_features,
        training_set
    )
    
    test_set = apply_features(
        paragraph_features,
        test_set
    )

    print '\nTraining...'
    classifier = nltk.NaiveBayesClassifier.train(
        training_set
    )

    global count
    count = 0

    print '\nTesting...'

    results = nltk.classify.accuracy(classifier, test_set)

    print '\nAccuracy:', results


def print_type():

    if CASE_SENSITIVE:
        print 'Case-sensitive',
    else:
        print 'Case-insensitive',

    if TECHNIQUE == TECHNIQUE_LEAST_FREQUENT:
        print 'least frequent',
    elif TECHNIQUE == TECHNIQUE_MOST_FREQUENT:
        print 'most frequent',
    elif TECHNIQUE == TECHNIQUE_RANDOM:
        print 'random frequency',

    if FEATURE == FEAT_CONTAINS:
        print 'contains',
    elif FEATURE == FEAT_BEGIN_SENT:
        print 'first word in sent',
    elif FEATURE == FEAT_FIRST_SENT:
        print 'in first sent',
    elif FEATURE == FEAT_LINKED_TITLES:
        print 'linked from wiki article',

    print 'with {0} samples'.format(N_SAMPLES)


def main():
    wiki_dir = argv[1]
    index_dir = argv[2]
    index_to_wiki_file = argv[3]
    ranked_titles_file = '../sourceTexts/rankedTitles.txt'
    

    print 'Loading indexToWiki conversion table...'
    with open(index_to_wiki_file, 'r') as f:
        index_to_wiki = json.loads(f.read())

    print 'Loading training data...'
    wiki_tuples = get_train_tuples(wiki_dir)

    if FEATURE == FEAT_CONTAINS:
        ranked_words = word_feat_contains_fd.keys()
    elif FEATURE == FEAT_FIRST_SENT:
        ranked_words = word_feat_first_sent_fd.keys()
    elif FEATURE == FEAT_BEGIN_SENT:
        ranked_words = (
            word_feat_first_word_in_sent_fd.keys()
        )
    elif FEATURE == FEAT_LINKED_TITLES:
        ranked_words = list()

        with open(ranked_titles_file, 'r') as f:
            for title in f:

                if CASE_SENSITIVE:
                    pass
                else:
                    title = title.lower()

                ranked_words.append(title.strip())
    else:
        ranked_words = None
        print 'FEATURE NOT SUPPORTED'
        exit()

    print 'keys', len(ranked_words)

    print 'Loading test data...'
    index_tuples = get_test_tuples(index_dir)

    # Convert index labels to Wikipedia titles.
    print 'Converting idx tuple titles to wiki titles...'
    tmp = list()
    for t in index_tuples:
        try:
            t = (t[0], index_to_wiki[t[1]],)
        except KeyError:
            print 'KeyError:', t[1]

        tmp.append(t)

    index_tuples = tmp

    if TECHNIQUE == TECHNIQUE_MOST_FREQUENT:
        # NLTKwP p.228
        ranked_words = ranked_words[:N_SAMPLES]
    elif TECHNIQUE == TECHNIQUE_LEAST_FREQUENT:
        # Inspired by NLTKwP p.228
        ranked_words = ranked_words[-N_SAMPLES:]
    elif TECHNIQUE == TECHNIQUE_RANDOM:
        # Pick words at random from our set
        ranked_words = random.sample(
            ranked_words,
            N_SAMPLES
        ) 
    else:
        ranked_words = None
        print 'TECHNIQUE NOT SUPPORTED'
        exit()

    global word_features

    word_features = dict()

    print 'Forming feature dictionary...'
    for i, k in enumerate(ranked_words):
        word_features[k] = i  

    print_type()

    classify(wiki_tuples, index_tuples)


if __name__ == '__main__':
    # Change these variables to change the classifier's
    # behavior before running.
    
    # Acceptible values:
    # * True: features are case sensitive
    # * False: features are case insensitive
    CASE_SENSITIVE = True
    
    # Acceptible values:
    # * TECHNIQUE_RANDOM: features randomly sorted
    # * TECHNIQUE_MOST_FREQUENT: most frequent features
    #   appear first
    # * TECHNIQUE_LEAST_FREQUENT: least frequent features
    #   appear first
    TECHNIQUE = TECHNIQUE_MOST_FREQUENT
    
    # Acceptible values:
    # * FEAT_CONTAINS: document contains string
    # * FEAT_FIRST_SENT: first sentence in paragraph
    #   contains string
    # * FEAT_BEGIN_SENT: a sentence in the string begins
    #   with string
    # * FEAT_LINKED_TITLES: paragraph contains word or
    #   phrase linked in Wikipedia article(s)
    FEATURE = FEAT_BEGIN_SENT
    
    # Represents the cardinality of the feature set taken
    # from the population of possible features determined
    # by the type of FEATURE and ranked according to
    # TECHNIQUE. Samples are taken in the order of
    # TECHNIQUE from the superset of possible features
    # until N_SAMPLES have been selected.
    #
    # Acceptible values 1 to N.
    #
    # Note: Increasing this number will linearly increase
    #       memory consumption to high levels (nearly 2GB
    #       for values of 2000).
    N_SAMPLES = 100

    main()
