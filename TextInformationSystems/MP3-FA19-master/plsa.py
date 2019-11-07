import re

import numpy as np
import math
import codecs

def normalize(input_matrix):
    """
    Normalizes the rows of a 2d input_matrix so they sum to 1
    """

    row_sums = input_matrix.sum(axis=1)
    assert (np.count_nonzero(row_sums)==np.shape(row_sums)[0]) # no row should sum to zero
    new_matrix = input_matrix / row_sums[:, np.newaxis]
    return new_matrix

class Corpus(object):

    """
    A collection of documents.
    """

    def __init__(self, documents_path):
        """
        Initialize empty document list.
        """
        self.documents = []
        self.vocabulary = []
        self.likelihoods = []
        self.documents_path = documents_path
        self.term_doc_matrix = None 
        self.document_topic_prob = None  # P(z | d)
        self.topic_word_prob = None  # P(w | z)
        self.topic_prob = None  # P(z | d, w)

        self.number_of_documents = 0
        self.vocabulary_size = 0

    def build_corpus(self):
        """
        Read document, fill in self.documents, a list of list of word
        self.documents = [["the", "day", "is", "nice", "the", ...], [], []...]
        
        Update self.number_of_documents
        """
        # #############################
        # your code here
        # #############################
        with open(self.documents_path) as f:
            self.documents = [line.split(' ') for line in f]
        self.number_of_documents = len(self.documents)
        # print(self.documents)
        # pass    # REMOVE THIS

    def build_vocabulary(self):
        """
        Construct a list of unique words in the whole corpus. Put it in self.vocabulary
        for example: ["rain", "the", ...]

        Update self.vocabulary_size
        """
        # #############################
        # your code here
        # #############################\
        SPECIAL_CHARS = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*']
        CARRIAGE_RETURNS = ['\n', '\r\n', '\t']
        ISWORD_REGEX = "^[a-z']+$"

        unique_words = []
        for doc in self.documents:
            for w in doc:
                w = w.lower()
                if w[0].isdigit():
                    w = w[1:]
                for junk in SPECIAL_CHARS + CARRIAGE_RETURNS:
                    w = w.replace(junk,'').strip("'")
                w if re.match(ISWORD_REGEX, w) else None
                if w not in unique_words and (len(w) > 1):
                    unique_words.append(w)

        self.vocabulary = unique_words #how to remove stopwords.
        self.vocabulary_size = len(self.vocabulary)
        # pass    # REMOVE THIS

    def build_term_doc_matrix(self):
        """
        Construct the term-document matrix where each row represents a document, 
        and each column represents a vocabulary term.

        self.term_doc_matrix[i][j] is the count of term j in document i
        """
        # ############################
        # your code here
        # ############################
        self.term_doc_matrix = np.zeros([self.number_of_documents, self.vocabulary_size], dtype=np.int)
        for docIdx, doc in enumerate(self.documents): # list of words in rows of documents
            tc = np.zeros(self.vocabulary_size, dtype=int)
            for w in doc:
                if w in self.vocabulary:
                    w_idx = self.vocabulary.index(w)
                    tc[w_idx] += 1
            self.term_doc_matrix[docIdx] = tc

        # print("term_doc_matrix\n ", self.term_doc_matrix)
        # print("tdm shape ", self.term_doc_matrix.shape)
        # pass    # REMOVE THIS

    def initialize_randomly(self, number_of_topics):
        """
        Randomly initialize the matrices: document_topic_prob and topic_word_prob
        which hold the probability distributions for P(z | d) and P(w | z): self.document_topic_prob, and self.topic_word_prob

        Don't forget to normalize!
        HINT: you will find numpy’s random matrix useful [https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.random.html]
        """
        # ############################
        # your code here
        # ############################
        self.document_topic_prob = np.random.random(size= (self.number_of_documents, number_of_topics))
        normalize(self.document_topic_prob)
        self.topic_word_prob = np.random.random(size= (number_of_topics, self.vocabulary_size))
        normalize(self.topic_word_prob)
        # pass    # REMOVE THIS

    def initialize_uniformly(self, number_of_topics):
        """
        Initializes the matrices: self.document_topic_prob and self.topic_word_prob with a uniform 
        probability distribution. This is used for testing purposes.

        DO NOT CHANGE THIS FUNCTION
        """
        self.document_topic_prob = np.ones((self.number_of_documents, number_of_topics))
        self.document_topic_prob = normalize(self.document_topic_prob)

        self.topic_word_prob = np.ones((number_of_topics, len(self.vocabulary)))
        self.topic_word_prob = normalize(self.topic_word_prob)

    def initialize(self, number_of_topics, random=False):
        """ Call the functions to initialize the matrices document_topic_prob and topic_word_prob
        """
        print("Initializing...")

        if random:
            self.initialize_randomly(number_of_topics)
        else:
            self.initialize_uniformly(number_of_topics)

    def expectation_step(self):
        """ The E-step updates P(z | w, d)
        """
        print("E step:")
        
        # ############################
        # your code here
        # ############################

        pass    # REMOVE THIS
            

    def maximization_step(self, number_of_topics):
        """ The M-step updates P(w | z)
        """
        print("M step:")
        
        # update P(w | z)
        
        # ############################
        # your code here
        # ############################

        
        # update P(z | d)

        # ############################
        # your code here
        # ############################
        
        pass    # REMOVE THIS


    def calculate_likelihood(self, number_of_topics):
        """ Calculate the current log-likelihood of the model using
        the model's updated probability matrices
        
        Append the calculated log-likelihood to self.likelihoods

        """
        # ############################
        # your code here
        # ############################
        
        return

    def EStepNormalize(self, values):
        s = sum(values)
        for i in range(len(values)):
            values[i] = (values[i] * 1.0)/s

    def plsa(self, number_of_topics, max_iter, epsilon):

        """
        Model topics.
        """
        print ("EM iteration begins...")

        # build term-doc matrix
        self.build_term_doc_matrix()
        
        # Create the counter arrays.
        # P(z | d)
        self.document_topic_prob = np.zeros([self.number_of_documents, number_of_topics], dtype=np.float)
        # P(w | z)
        self.topic_word_prob = np.zeros([number_of_topics, self.vocabulary_size], dtype=np.float)

        # P(z | d, w)
        self.topic_prob = np.zeros([self.number_of_documents, number_of_topics, self.vocabulary_size], dtype=np.float)

        print("document_topic_prob ", self.document_topic_prob.shape)
        print("topic_word_prob ", self.topic_word_prob.shape)
        print("topic_prob ", self.topic_prob.shape)

        # P(z | d) P(w | z)
        self.initialize(number_of_topics, random=True)

        # Run the EM algorithm
        current_likelihood = 0.0

        for iteration in range(max_iter):
            print("Iteration #" + str(iteration + 1) + "...")

            # ############################
            # your code here
            # ############################
            # E-Step
            # for t_idx in range(number_of_topics): #for each topic
            #     for d_idx, d in enumerate(self.documents):  # for every document
            #         for v_idx in range(self.vocabulary_size):
            #             p = self.document_topic_prob[d_idx][t_idx] * self.topic_word_prob[t_idx][v_idx]
            #             self.topic_prob[d_idx][t_idx][v_idx] = p

            for d_idx, d in enumerate(self.documents):  # for every document
                for v_idx in range(self.vocabulary_size): # for every vocab
                    p = self.document_topic_prob[d_idx, :] * self.topic_word_prob[:, v_idx]
                    # print("p b4: ", p)
                    self.EStepNormalize(p)
                    # print("p after: ", p)
                    for t_idx in range(number_of_topics):
                        self.topic_prob[d_idx][t_idx][v_idx] = p[t_idx]

            print("topic_prob \n", self.topic_prob)

            # M-Step
            # P(w|z)
            # for z in range(number_of_topics):
            #     for w_idx in range(self.vocabulary_size):

            #
            # for d_idx in range(self.number_of_documents):
            #     for z in range(self.number_of_topics):
            #         p = 0
            #         for w_idx in range(self.vocabulary_size):
            #             p += self.term_doc_matrix[d_idx][w_idx] * self.topic_prob[d_idx, w_idx, z]
            #         self.document_topic_prob[d_idx][z] = p
            #         # normalize(self.document_topic_prob[d_idx])

            pass    # REMOVE THIS



def main():
    documents_path = 'data/test.txt'
    corpus = Corpus(documents_path)  # instantiate corpus
    corpus.build_corpus()
    corpus.build_vocabulary()
    print("corpusVocab:: ", corpus.vocabulary)
    print("Vocabulary size:" + str(len(corpus.vocabulary)))
    print("Number of documents:" + str(len(corpus.documents)))
    number_of_topics = 2
    max_iterations = 50
    epsilon = 0.001
    corpus.plsa(number_of_topics, max_iterations, epsilon)



if __name__ == '__main__':
    main()
