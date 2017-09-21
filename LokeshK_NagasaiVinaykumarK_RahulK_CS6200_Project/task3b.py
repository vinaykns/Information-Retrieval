import Retriever
import Indexer
import string
import os
import glob
import re

def get_stemmed_corpus():
    total_stemmed_corpus = {}
    stemmed_corpus = {}
    doc_ids = []
    stop_if = ['pm', 'am']
    cacm_stem = open('cacm_stem.txt', 'r')
    for eachline in cacm_stem.readlines():
        if eachline[0] == "#":
            string = eachline
            search = re.search(r'\d+', string)
            doc_id = search.group()
            doc_id = 'CACM-' + ((4-len(doc_id)) * '0') + doc_id
            total_stemmed_corpus[doc_id] = []
            stemmed_corpus[doc_id] = []
            doc_ids.append(doc_id)
        else:
            words = eachline.split()
            total_stemmed_corpus[doc_ids[len(doc_ids) - 1]] += words


    for doc_id, content in total_stemmed_corpus.viewitems():
        length = len(content)
        for i in range(length):
            if  stop_if[0] in content[length - i - 1] or stop_if[1] in content[length - i - 1]:
                index = length - i
                stemmed_corpus[doc_id] = total_stemmed_corpus[doc_id][:index]
                break

    return stemmed_corpus

def task3b(model):
    output_directory = os.path.join(os.getcwd(), "output")
    stemmed_corpus = get_stemmed_corpus()
    f = open('cacm_stem.query.txt', 'r')
    stemmed_queries = f.readlines()
    f.close()

    I = Indexer.InvertedIndexer('')
    I.stemmed_indexer(stemmed_corpus)
    r = Retriever.Retriever('', I, os.getcwd())
    file_name = os.path.join(output_directory, 'task3b_' + model + '_stemmed.txt')
    f = open(file_name, 'w')
    query_no = [12,13,19,23,24,25,50]
    q_iter = 0
    for each_query in stemmed_queries:
        r.process_query(each_query)
        docs_and_scores = r.get_scores_for_docs(model, query_no[q_iter])

        # save results into appropriate file
        docs = docs_and_scores[0]
        scores = docs_and_scores[1]
        for i in range(100):
            f.write(str(query_no[q_iter]) \
                    + " Q0 " \
                    + str(docs[i]) + ' ' \
                    + str((i + 1)) + " " \
                    + str(scores[i]) + " " \
                    + model + "\n")
        q_iter += 1
    f.close()