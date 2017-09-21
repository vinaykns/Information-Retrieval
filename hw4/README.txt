For this assignment we retrieve the documents for the given query.

 a. To get the above functionality there are two scripts indexer.py(To build indexes) and retriever.py(retrieve the documents to output the results).
    The pre assumed criteria to run this retriever.py (python retriever.py) is having the processed_corpus directory (i.e having the processed collection after extracting from raw_corpus).
    In case if one want to generate processes_corpus uncomment lines 296,297,298,299 in indexer.py. Give the input list of urls in the init definition of indexer

 b. Then to get the top 100 documents for the given queries, please run python retriever.py which will generate 4 output files associated with each query.  

 c. Make sure that the processed_corpus, indexer.py and retriever.py are present in the same directory. 
