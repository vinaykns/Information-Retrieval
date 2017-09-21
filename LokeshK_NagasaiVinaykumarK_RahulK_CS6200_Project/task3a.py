from bs4 import BeautifulSoup
import os
import Indexer
import Retriever

def task3a(model, raw_corpus_directory):
    project_directory = os.getcwd()
    p = Indexer.Parser()
    corpus_directory = p.build_corpus(raw_corpus_directory, stopped = True)
    output_directory = os.path.join(project_directory, "output")

    I = Indexer.InvertedIndexer(corpus_directory)
    I.ngram_indexer(1) # builds a unigram indexes for each word
    r = Retriever.Retriever(corpus_directory, I, project_directory)    # create a Retriever class, which contains different retrieval model

    os.chdir(raw_corpus_directory)
    os.chdir(os.pardir)
    f = open('cacm.query.txt', 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()

    f_stop_words = open('common_words.txt', 'r')
    stop_words_list = f_stop_words.readlines()
    stop_words = [i.strip() for i in stop_words_list]
    f_stop_words.close()
    file_name = os.path.join(output_directory, 'task3a_'+ model + '.txt')
    f = open(file_name, 'w')     # open file for writing results
    for i in range(64):
        query_no = (soup.find('docno')).text.encode('utf-8')    # extract query number and query
        (soup.find('docno')).decompose()
        query = (soup.find('doc')).text.encode('utf-8')
        (soup.find('doc')).decompose()

        r.process_query(query, stopped = True, stopwords = stop_words)          # parse the query
        # r.clean_content(query)
        docs_and_scores = r.get_scores_for_docs(model, int(query_no))   # retrieve relevant documents

        # save results into appropriate file
        docs = docs_and_scores[0]
        scores = docs_and_scores[1]
        for i in range(100):
            f.write(str(query_no) \
                        + " Q0 " \
                        + str(docs[i]) + ' ' \
                        + str((i+1)) + " " \
                        + str(scores[i]) + " " \
                        + model + "\n")
    f.close()