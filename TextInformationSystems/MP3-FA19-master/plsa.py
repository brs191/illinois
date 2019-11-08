import re

import numpy as np
import math

#Each row add up to 1
def normalize_row(input_matrix):
    """
    Normalizes the rows of a 2d input_matrix so they sum to 1
    """

    row_sums = input_matrix.sum(axis=1)
    assert (np.count_nonzero(row_sums) == np.shape(row_sums)[0])  # no row should sum to zero
    new_matrix = input_matrix / row_sums[:, np.newaxis]
    return new_matrix

def normalize_col(input_matrix):
    """
    Normalizes the coloums of a 2d input_matrix so they sum to 1
    """
    col_sums = input_matrix.sum(axis=0)
    assert (np.count_nonzero(col_sums) == np.shape(col_sums)[0])  # no col should sum to zero
    new_matrix = input_matrix / col_sums[np.newaxis, :]
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
        with open(self.documents_path) as f:
            self.documents = [line.split(' ') for line in f]
        self.number_of_documents = len(self.documents)

    def build_vocabulary(self):
        """
        Construct a list of unique words in the whole corpus. Put it in self.vocabulary
        for example: ["rain", "the", ...]

        Update self.vocabulary_size
        """
        SPECIAL_CHARS = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*']
        CARRIAGE_RETURNS = ['\n', '\r\n', '\t']
        ISWORD_REGEX = "^[a-z']+$"

        with open("stopwords.dic") as f:
            stopwords = [line.strip() for line in f]

        unique_words = []
        for doc in self.documents:
            for w in doc:
                w = w.lower()
                if len(w) > 1:
                    if w[0].isdigit():
                        w = w[1:]
                    for junk in SPECIAL_CHARS + CARRIAGE_RETURNS:
                        w = w.replace(junk, '').strip("'")
                    w if re.match(ISWORD_REGEX, w) else None
                    if w not in unique_words and (len(w) > 1) and w not in stopwords:
                        unique_words.append(w)

        self.vocabulary = unique_words
        self.vocabulary_size = len(self.vocabulary)

    def build_term_doc_matrix(self):
        """
        Construct the term-document matrix where each row represents a document,
        and each column represents a vocabulary term.

        self.term_doc_matrix[i][j] is the count of term j in document i
        """
        self.term_doc_matrix = np.zeros([self.number_of_documents, self.vocabulary_size], dtype=np.int)
        for d_idx, doc in enumerate(self.documents):  # list of words in rows of documents
            tc = np.zeros(self.vocabulary_size, dtype=int)
            for w in doc:
                if w in self.vocabulary:
                    tc[self.vocabulary.index(w)] += 1
            self.term_doc_matrix[d_idx] = tc
        """
        print(self.term_doc_matrix)
        [[36 27 35  0  0  0]
         [22 48 29  0  0  0]
        [4 0 8 31 33 23]
        """

    def initialize_randomly(self, number_of_topics):
        """
        Randomly initialize the matrices: document_topic_prob and topic_word_prob
        which hold the probability distributions for P(z | d) and P(w | z): self.document_topic_prob, and self.topic_word_prob

        Don't forget to normalize!
        HINT: you will find numpy’s random matrix useful [https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.random.html]
        """
        self.document_topic_prob = np.random.random(size=(self.number_of_documents, number_of_topics))
        normalize_row(self.document_topic_prob)
        self.topic_word_prob = np.random.random(size=(number_of_topics, self.vocabulary_size))
        normalize_row(self.topic_word_prob)

    def initialize_uniformly(self, number_of_topics):
        """
        Initializes the matrices: self.document_topic_prob and self.topic_word_prob with a uniform
        probability distribution. This is used for testing purposes.

        DO NOT CHANGE THIS FUNCTION
        """
        self.document_topic_prob = np.ones((self.number_of_documents, number_of_topics))
        self.document_topic_prob = normalize_row(self.document_topic_prob)

        self.topic_word_prob = np.ones((number_of_topics, len(self.vocabulary)))
        self.topic_word_prob = normalize_row(self.topic_word_prob)

    def initialize(self, number_of_topics, random=False):
        """ Call the functions to initialize the matrices document_topic_prob and topic_word_prob
        """
        print("Initializing...")

        if random:
            self.initialize_randomly(number_of_topics)
        else:
            self.initialize_uniformly(number_of_topics)

    def expectation_step(self, number_of_topics):
        """ The E-step updates P(z | w, d)
        """
        print("E step:")
        for d_idx in range(self.number_of_documents):  # for every document
            for v_idx in range(self.vocabulary_size):  # for every vocab
                p = self.document_topic_prob[d_idx, :] * self.topic_word_prob[:, v_idx]
                for t_idx in range(number_of_topics):
                    self.topic_prob[d_idx][t_idx][v_idx] = p[t_idx]
        normalize_col(self.topic_prob[:, 0, :])
        normalize_col(self.topic_prob[:, 1, :])
        # print(self.topic_prob)

    def maximization_step(self, number_of_topics):
        """ The M-step updates P(w | z)
        """
        print("M step:")

        # update P(w | z)
        # for w_idx in range(self.vocabulary_size):
        #     for z in range(number_of_topics):
        #         s = 0
        #         for d_idx in range(self.number_of_documents):
        #             s += self.term_doc_matrix[d_idx][w_idx] * self.topic_prob[d_idx, z, w_idx]
        #         self.topic_word_prob[z][w_idx] = s
        #     # normalize_row(self.topic_word_prob)
        # method1 = self.topic_word_prob

        # test = self.topic_prob.transpose((1,0,2))
        # print("transpose 1,0,2 ", test.shape)
        # print("self.term_doc_matrix ", self.term_doc_matrix.shape)

        method2 = (self.topic_prob.transpose((1,0,2)) * self.term_doc_matrix).sum(1)
        # print("method2 ", method2.shape)
        # print("self.topic_word_prob ", self.topic_word_prob.shape)
        self.topic_word_prob = method2

        # print("Bollam : ", np.array_equal(method1, method2))

        # p = self.term_doc_matrix @ self.topic_prob[:,0,:]
        # print("p ", p.shape)
        # print("term doc matrix ", self.term_doc_matrix.shape)
        # print("self.topic_prob[:,0,:] ", self.topic_prob[:,0,:].shape)
        # print("topic prob ", self.topic_prob.shape)

        # update P(z|d)
        # for d_idx in range(self.number_of_documents):
        #     for z in range(number_of_topics):
        #         p = 0
        #         for w_idx in range(self.vocabulary_size):
        #             p += self.term_doc_matrix[d_idx][w_idx] * self.topic_prob[d_idx, z, w_idx]
        #         self.document_topic_prob[d_idx][z] = p
            # normalize_row(self.document_topic_prob)
        # pass  # REMOVE THIS
        # test = self.topic_prob.transpose((1,2,0))
        # print("transpose 1,2,0 ", test.shape)
        # print("self.term_doc_matrix ", self.term_doc_matrix.transpose(1,0).shape)
        # print("self.document_topic_prob ", self.document_topic_prob.shape)

        method3 = (self.topic_prob.transpose((1,2,0)) * self.term_doc_matrix.transpose(1,0)).sum(1)
        # print("method3 ", method3.transpose(1,0).shape)
        self.document_topic_prob = method3.transpose(1,0)
        # print("shekar ", np.array_equal(method3.transpose(1,0), self.document_topic_prob))

    def calculate_likelihood(self, number_of_topics):
        """ Calculate the current log-likelihood of the model using
        the model's updated probability matrices

        Append the calculated log-likelihood to self.likelihoods

        """
        likelihood = 0
        p_wk = np.dot(self.document_topic_prob, self.topic_word_prob)
        ll = np.log(p_wk)
        # print("ll shape is ", ll.shape)
        # print("term_doc_matrix shape is ", self.term_doc_matrix.shape)
        llm = np.multiply(self.term_doc_matrix, ll)
        likelihood = np.sum(llm)
        self.likelihoods.append(likelihood)
        return likelihood

    def plsa(self, number_of_topics, max_iter, epsilon):

        """
        Model topics.
        """
        print("EM iteration begins...")

        # build term-doc matrix
        self.build_term_doc_matrix()

        # Create the counter arrays.
        # P(z | d)
        self.document_topic_prob = np.zeros([self.number_of_documents, number_of_topics], dtype=np.float)
        # P(w | z)
        self.topic_word_prob = np.zeros([number_of_topics, self.vocabulary_size], dtype=np.float)

        # P(z | d, w)
        self.topic_prob = np.zeros([self.number_of_documents, number_of_topics, self.vocabulary_size], dtype=np.float)

        # print("document_topic_prob ", self.document_topic_prob.shape)
        # print("topic_word_prob ", self.topic_word_prob.shape)
        # print("topic_prob ", self.topic_prob.shape)

        # P(z | d) P(w | z)
        self.initialize(number_of_topics, random=True)

        # Run the EM algorithm
        current_likelihood = 0.0

        # for iteration in range(max_iter):
        #     print("Iteration #" + str(iteration + 1) + "...")
        while 1:
            self.expectation_step(number_of_topics)
            self.maximization_step(number_of_topics)

            new_ll = self.calculate_likelihood(number_of_topics)
            print("new_ll ", new_ll)
            z = abs(new_ll - current_likelihood)
            print("z: ", z)
            if z <= epsilon:
                print("problem Solved!!")
                break;

def main():
    documents_path = 'data/test.txt'
    corpus = Corpus(documents_path)  # instantiate corpus
    corpus.build_corpus()
    corpus.build_vocabulary()
    print("corpusVocab:: ", corpus.vocabulary)
    print("Vocabulary size:" + str(len(corpus.vocabulary)))
    print("Number of documents:" + str(len(corpus.documents)))
    number_of_topics = 2
    max_iterations = 1 #50
    epsilon = 0.001
    corpus.plsa(number_of_topics, max_iterations, epsilon)


if __name__ == '__main__':
    main()
