import os
import glob
import math
import string
import operator
import Indexer
import re

class Retriever:
    def __init__(self, corpus_directory, I, project_directory = ''):
        self.corpus_directory = corpus_directory
        # parser = indexer.Parser()
        # self.I = Indexer.InvertedIndexer(self.corpus_directory)
        self.I = I
        self.query_dic = {}  # stores the parsed query and its frequency
        self.score_dic = {}  # scores of each document
        self.current_query = ''     # used to open the file with query name and save results

        self.avdl = 0;  # average doc length
        self.first_query = True
        self.project_directory = project_directory
        self.relevance_data = self.get_relevance_data()

    def build_indexes(self):
        # parser = indexer.Parser()
        # parser.build_corpus(self.raw_corpus_directory)
        # I = indexer.InvertedIndexer(self.raw_corpus_directory)
        self.I.ngram_indexer(1)

    def get_scores_for_docs(self, model, query_no = 1):
        if model == 'bm25':     # use bm25 retrieval model
            if self.first_query:
                self.first_query = False
                # initialize score_dic to zero
                for each_doc in self.I.doc_lengths:
                    self.avdl += self.I.doc_lengths[each_doc]
                self.avdl = float(self.avdl) / len(self.I.doc_lengths)
            for each_file in self.I.docIDs:
                BM25_score = 0
                for each_query_term in self.query_dic:      # replace current_query with query_dic
                    BM25_score += self.calculate_BM25_score(each_query_term, each_file, query_no)
                self.score_dic[each_file] = BM25_score

        if model == 'tfidf':    # use tf-idf retrieval model
            for each_file in self.I.docIDs:
                tfidf_score = 0
                for each_query_term in self.current_query:
                    fk = 0  # number of occurrences of term k in document
                    doc_len = self.I.doc_lengths[each_file]
                    if each_query_term in self.I.inverted_indexes:
                        if each_file in self.I.inverted_indexes[each_query_term]:
                            fk = self.I.inverted_indexes[each_query_term][each_file]
                    else:
                        continue
                    tf = float(fk) / doc_len
                    idf = math.log(float(len(self.I.docIDs)) / len(self.I.inverted_indexes[each_query_term]))
                    tfidf_score += (tf * idf)
                self.score_dic[each_file] = tfidf_score

        # sort the documents based on scores
        sorted_docs = sorted(self.score_dic.items(), key=operator.itemgetter(1), reverse=True)
        docs = [x[0] for x in sorted_docs]
        scores = [x[1] for x in sorted_docs]
        return docs, scores

    def calculate_BM25_score(self, query_term, docID, query_id):     # query_term - single word in the whole query
        if query_term not in self.I.inverted_indexes:
            return 0
        if query_id not in self.relevance_data:
            R = 0
            ri = 0
        else:
            R = len(self.relevance_data[query_id])
            ri = 0
            for each_doc in self.relevance_data[query_id]:
#                if query_term in self.I.corpus[each_doc]:
                if each_doc in self.I.inverted_indexes[query_term]:
                    ri += 1
        N = len(self.I.docIDs)
        n = 0
        f = 0
        n = len(self.I.inverted_indexes[query_term])
        if docID in self.I.inverted_indexes[query_term]:
            f = self.I.inverted_indexes[query_term][docID]
        qf = self.query_dic[query_term]
        k1 = 1.2
        b = 0.75
        k2 = 200
        dl = self.I.doc_lengths[docID]
        K = k1*((1-b) + (b*(dl/self.avdl)))
        BM25_score_per_query = math.log(((float(N) - n - R + ri + 0.5) / (n - ri + 0.5)) * ((ri + 0.5) / (R - ri + 0.5))) * \
                               (float((k1 + 1)*f) /(K+f)) * \
                               ((float((k2 + 1) * qf)) / float(k2 + qf))

        return BM25_score_per_query

    def process_query(self, query, ret = False, stopped = False, stopwords = []):  # similar to process used while parsing corpus
        query = query.lower()
        # special_chars = re.sub("[,.-:]", "", string.punctuation)
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '}', '[', ']', '|', '\\', ';', "'", '"', '/', '<', '>', '?']
        query = query.translate(None, ''.join(special_chars))
        query = query.replace(':', " ")
        query = query.replace('-', ' ')     # to split the words containg '-' symbol
                                            # eg: multi-targeted to 'multi', 'targeted'
        tokens = query.split()
        tokens = [each_token.strip('.,-') for each_token in tokens]
        parsed_query = ''
        self.query_dic = {}
        stopwords_in_query = []
        for each_token in tokens:
            if stopped:
                if each_token in stopwords:
                    stopwords_in_query.append(each_token)
                    continue
            parsed_query += each_token + ' '
            self.query_dic[each_token] = 0
        if ret:
            return parsed_query

        self.current_query = parsed_query.split()
        for each_token in tokens:
            if each_token not in stopwords_in_query:
                self.query_dic[each_token] += 1     # term frequency for bm25 (qf)

    def get_relevance_data(self):
        relevant_list = open(os.path.join(self.project_directory, "cacm.rel"), 'r')
        query_relevant = {}
        for line in relevant_list.readlines():
            words = line.split()
            if query_relevant.has_key(int(words[0])):
                doc_no = words[2][5:]
                doc_no = str(doc_no)
                doc = 'CACM-' + (4 - len(doc_no)) * '0' + doc_no
                query_relevant[int(words[0])].append(doc)
            else:
                query_relevant[int(words[0])] = []
                doc_no = words[2][5:]
                doc = 'CACM-' + (4 - len(doc_no)) * '0' + doc_no
                query_relevant[int(words[0])].append(doc)
        return query_relevant


def hw4():
    directory = raw_input('Enter corpus directory: ')
    if not os.path.exists(directory):
        print "Please enter valid directory address"
        directory = raw_input()
    r = Retriever(directory)
    r.build_indexes()
    e = False   # e - exit
    while not e:
        query = raw_input("Enter the Query: ")
        while not query:
            query = raw_input("Enter the Query: ")
        if query == 'e':
            e = True
            break
        r.process_query(query)
        r.get_scores_for_docs()




