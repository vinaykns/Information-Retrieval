from bs4 import BeautifulSoup
import os
import glob
import Indexer
import Retriever
from collections import Counter
import operator

def Query_Expander(query, docs, corpus, stopwords, k = 12, n = 5):
    query_terms = query.split()
    top_docs = docs[0:k]
    total_text = [] # text present in top k docs
    for each_doc in top_docs:
        total_text += corpus[each_doc]

    for each_word in total_text:        # to remove stopwords from top k documents
        if each_word in stopwords:
            total_text.remove(each_word)

    word_count = dict(Counter(total_text))
    for each_term in query_terms:
        if each_term in word_count:
            word_count[each_term] += k
        else:
            word_count[each_term] = k
    top_terms = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
    expanded_query_list = [i for i,j in top_terms][:len(query_terms) + n]
    expanded_query = " ".join(expanded_query_list)
    return expanded_query

def run_task(task, model, raw_corpus_directory):
    project_directory = os.getcwd()
    output_directory = os.path.join(project_directory, "output")

    # Parser (to process the raw corpus (no stopping))
    p = Indexer.Parser()
    corpus_directory = p.build_corpus(raw_corpus_directory)

    # Indexer - Builds the inverted indexes for the processed corpus
    I = Indexer.InvertedIndexer(corpus_directory)
    I.ngram_indexer(1) # builds a unigram indexes for each word

    # Retriever - based on the model specified, this object can  be
    #             used to get the results.
    r = Retriever.Retriever(corpus_directory, I, project_directory)

    # Get the queries from the given file
    query_dic = {}      # stores the queries; key - query ID, token - query
    os.chdir(project_directory)
    f = open('cacm.query.txt', 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()
    for i in range(64):
        query_no = (soup.find('docno')).text.encode('utf-8')  # extract query number and query
        (soup.find('docno')).decompose()
        query = (soup.find('doc')).text.encode('utf-8')
        (soup.find('doc')).decompose()
        query_dic[int(query_no)] = query

    # task 1
    if task == 1:
        os.chdir(project_directory)
        if not os.path.exists(output_directory):
            os.mkdir(output_directory, 0755)
        os.chdir(output_directory)

        f = open('task1_'+model+'.txt', 'w')
        for query_no in range(len(query_dic)):
            r.process_query(query_dic[query_no + 1])                           # parse the query
            docs_and_scores = r.get_scores_for_docs(model, (query_no + 1))   # retrieve relevant documents

            # save results into appropriate file
            docs = docs_and_scores[0]
            scores = docs_and_scores[1]
            for i in range(100):
                f.write(str(query_no + 1) \
                            + " Q0 " \
                            + str(docs[i]) + ' ' \
                            + str((i+1)) + " " \
                            + str(scores[i]) + " " \
                            + model + "\n")
        f.close()

    # task 2
    if task == 2:
        # read output files from task 1
        file_name = 'task1_' + model + '.txt'
        try:
            f = open(os.path.join(output_directory, file_name), 'r')
        except:
            print "Run Task - 1 before Task - 2"
            exit()
        data = f.readlines()
        f.close()
        list_of_lines = []
        for each_line in data:
            list_of_lines.append(each_line.split())  # contains parsed lines from the task1 output file

        task1_output = {}  # results for each; key = query ID(number), value = list of relevant files
        for each_line in list_of_lines:
            task1_output.setdefault(int(each_line[0]), []).append(each_line[2])

        # get stopwords
        f_stop_words = open('common_words.txt', 'r')
        stop_words_list = f_stop_words.readlines()
        stop_words = [i.strip() for i in stop_words_list]
        f_stop_words.close()

        # get corpus
        os.chdir(corpus_directory)
        files_list = glob.glob('*.html')
        corpus = {}
        for each_file in files_list:
            doc_name = each_file[:len(each_file) - 5]
            text = open(each_file).read()
            corpus[doc_name] = text.split()

        file_name = 'expanded_queries_' + model + '.txt'
        f = open(os.path.join(output_directory, file_name), 'w')
        expanded_query_dic = {}
        for query_no, query in query_dic.viewitems():
            processed_query = r.process_query(query, True)
            expanded_query_dic[query_no] = Query_Expander(processed_query, task1_output[query_no], corpus, stopwords=stop_words)
            f.write(str(query_no) + " " + expanded_query_dic[query_no] + "\n")
        f.close()

        file_name = 'task2_' + model + '.txt'
        f = open(os.path.join(output_directory, file_name), 'w')
        for query_no, query in expanded_query_dic.viewitems():
            r.process_query(query)  # parse the query
            # r.clean_content(query)
            docs_and_scores = r.get_scores_for_docs(model, query_no)  # retrieve relevant documents

            # save results into appropriate file
            docs = docs_and_scores[0]
            scores = docs_and_scores[1]
            for i in range(100):
                f.write(str(query_no) \
                        + " Q0 " \
                        + str(docs[i]) + ' ' \
                        + str((i + 1)) + " " \
                        + str(scores[i]) + " " \
                        + model + "\n")
        f.close()
        print "Results stored in " + output_directory + " directory"

