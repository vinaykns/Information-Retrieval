The entire operation for the Assignment 3: is implemented in the file task1, if you want to execute the file u can run by ./task1

   Initially the class indexer gets initialised by taking the input file 'task1.txt'.

a. For one need to build the raw corpus from the given links from the previous assignment, one can uncomment the line e.build_raw_corpus(), which will get the raw corpus folder.

b. Then if we need to process the corpus by considering the criteria given in the question we have to uncomment the line e.parsed_corpus().

c. Then if we want to get the corpus statistics, give the value of n (1,2,3) which gets the n-gram,(By default it is 1), then uncomment e.invertedindex(n) and e.tf_table() to get invertedindex of n-gram and tf table.
   Then if we want to get df table for the n-gram, the uncomment e.invertedindex(n) (By default n is 1), then uncomment e.invertedindex() and e.df_table.

d. Then if we want the stoplist for the unigram, then uncomment e.invertedindex(n) e.tf_table() e.df_table()
   e.stopwordcalculation()

e. With the selection of n-gram one can get automatically the zipf's law n-gram distribution 
