import gensim
import nltk
import re

class SentencesSemanticSimilarity():

    query = ""
    sentencesSet = []
    sanitizedSentencesSet = []
    dictionary = {}
    corpus = []
    processedQuery = ""

    def __init__(self, query, sentencesSet):
        self.query = query
        self.sentencesSet = sentencesSet
        self.sanitizedSentencesSet = self.preProcessSentences()
        self.dictionary = self.createDictionary()
        self.corpus = self.createCorpus()


    #Sanitize and tokenize
    #A document will now be a list of tokens.
    def preProcessSentences(self):
        processedSentences = []


        #Keep alphanumeric
        for sentence in self.sentencesSet:
            sentence = re.sub(r'^[a-zA-Z0-9\s]', '', sentence)


        #Tokenize
        processedSentences = [[w.lower() for w in nltk.word_tokenize(sentence)] for sentence in self.sentencesSet]

        return processedSentences



    #We will create a dictionary from a list of documents. A dictionary maps every word to a number.
    def createDictionary(self):
        return gensim.corpora.Dictionary(self.preProcessSentences())



    #Now we will create a corpus. A corpus is a list of bags of words.
    # A bag-of-words representation for a document just lists the number of times each word occurs in the document.
    def createCorpus(self):
        return [self.dictionary.doc2bow(sentence) for sentence in self.preProcessSentences()]


    #calculate similarity
    def getSimilarity(self):
        # we create a tf-idf model from the corpus. Note that num_nnz is the number of tokens.
        tf_idf = gensim.models.TfidfModel(self.corpus)
        s = 0
        for i in self.corpus:
            s += len(i)

        # we will create a similarity measure object in tf-idf space.
        # tf-idf stands for term frequency-inverse document frequency. Term frequency
        # is how often the word shows up in the document and inverse document fequency scales the value by how rare the word is in the corpus.
        sims = gensim.similarities.Similarity(' Similarity', tf_idf[self.corpus], num_features=len(self.dictionary))

        #now create a query document and convert it to tf-idf.
        self.query = re.sub(r'^[a-zA-Z0-9\s]', '', self.query)
        self.query = [w.lower() for w in nltk.word_tokenize(self.query)]

        query_doc_bow = self.dictionary.doc2bow(self.query)
        query_doc_tf_idf = tf_idf[query_doc_bow]

        #Return an array of document similarities to query. We see that the second document
        # is the most similar with the overlapping of socks and force.
        return sims[query_doc_tf_idf]
