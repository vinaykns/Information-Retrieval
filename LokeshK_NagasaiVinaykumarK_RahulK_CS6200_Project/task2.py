import Retriever
import Indexer
from bs4 import BeautifulSoup
import os
import glob
from collections import Counter
import operator

def Query_Expander(query, docs, corpus, k = 12, n = 5):
    query_terms = query.split()

    top_docs = docs[0:k]
    total_text = [] # text present in top k docs
    for each_doc in top_docs:
        total_text += corpus[each_doc]

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

current_directory = os.getcwd()

corpus_directory = os.path.join(current_directory, "processed_corpus")
I = Indexer.InvertedIndexer(corpus_directory)
I.ngram_indexer(1)
r = Retriever.Retriever(corpus_directory, I)

model = 'bm25'
# get the results from the previous runs (bm25 and tfidf)
file_name = 'task1_' + model + '.txt'
results_file_dir = os.path.join(current_directory, "task1")
results_file_dir = os.path.join(results_file_dir, file_name)

f = open(results_file_dir, 'r')
data = f.readlines()
f.close()
list_of_lines = []
for each_line in data:
    list_of_lines.append(each_line.split())     # contains parsed lines from the task1 output file

task1_output = {}       # results for each; key = query ID(number), value = list of relevant files
for each_line in list_of_lines:
    task1_output.setdefault(int(each_line[0]), []).append(each_line[2])


# get corpus
os.chdir(corpus_directory)
files_list = glob.glob('*.html')
corpus = {}
for each_file in files_list:
    doc_name = each_file[:len(each_file) - 5]
    text = open(each_file).read()
    corpus[doc_name] = text.split()


# get the queries from the given file(cacm.query.txt)
os.chdir(current_directory)
f = open('cacm.query.txt', 'r')
soup = BeautifulSoup(f.read(), 'html.parser')
f.close()

query_dic = {}
for i in range(64):
    query_no = (soup.find('docno')).text.encode('utf-8')    # extract query number and query
    query_no = query_no.strip()
    (soup.find('docno')).decompose()
    query = (soup.find('doc')).text.encode('utf-8')
    (soup.find('doc')).decompose()
    query_dic[int(query_no)] = query

os.chdir(current_directory)
f = open('expanded_queries_'+ model +'.txt', 'w')
expanded_query_dic = {}
for query_no, query in query_dic.viewitems():
    processed_query = r.process_query(query, True)
    expanded_query_dic[query_no] = Query_Expander(processed_query, task1_output[query_no], corpus)
    f.write(str(query_no) + " " + expanded_query_dic[query_no] + "\n")
f.close()

f = open('task2_expanded_'+ model + '.txt', 'w')
for query_no, query in expanded_query_dic.viewitems():
    r.process_query(query)          # parse the query
    # r.clean_content(query)
    docs_and_scores = r.get_scores_for_docs(model)   # retrieve relevant documents

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