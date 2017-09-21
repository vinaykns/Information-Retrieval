#!/usr/bin/python2

import indexer
import os
import sys
import glob
from collections import Counter
import operator
import math
import re
import pdb

class retriever:
    
    def __init__(self):
      queries=[]
      queries.append('global warming potential')
      queries.append('green power renewable energy')
      queries.append('solar energy california')
      queries.append('light bulb bulbs alternative alternatives')
      self.queries=queries
      cwd = os.getcwd()
      self.cwd = cwd

     
    def implementation(self):
      bm25_score = {}      
      avglen = 0
      total_sum = 0
      e = indexer.Indexer()
      n=1
      inverted_index = e.invertedindex(1)
      total_docs = e.total_documents()
      noof_tokens_doc = e.tokens_doc()
      df_words = e.df_table()
      docId = e.document_Ids()
      os.chdir(self.cwd + "/processed_corpus")
  
      for v in noof_tokens_doc.viewvalues():
        total_sum += v
 
      avglen = total_sum/total_docs          
      total_files = glob.glob('*txt')
      for query in self.queries:
        bm25_score[query]={}
        split_query = query.split()

        for each in total_files:
          bm_sum = 0          
          for s_word in split_query:
            try:
              exp1 = math.log(float(0.5 * (total_docs - df_words[s_word] + 0.5))/(0.5 * (df_words[s_word] + 0.5)))
              K = 1.2*((1 - 0.75) + 0.75*(float(noof_tokens_doc[each[:len(each)-4]]/avglen)))
              exp2 = (((1 + 1.2) * inverted_index[s_word][docId[each[:len(each)-4]]])/(K + inverted_index[s_word][docId[each[:len(each)-4]]]))
              exp3 = 101/101
              product = exp1 * exp2 * exp3
              bm_sum += product

            except:
              continue
          
          bm25_score[query][each] = bm_sum              
      
      os.chdir(self.cwd)
      
      for index in range(len(self.queries)):
        #try:
          sortedbm25_score = sorted(bm25_score[self.queries[index]].items(), key=operator.itemgetter(1), reverse=True)
          rank = 1
          sys.stdout = open(self.queries[index],'w')
          #file1 = open(self.queries[index],'w')
          for i in range(100):
            try:
              print "{} Q0 {} {} {} system_name".format(index,docId[sortedbm25_score[i][0][:len(sortedbm25_score[i][0])-4]],rank,sortedbm25_score[i][1])
              rank += 1
              #sys.stdout.close()
            except KeyError:
              continue

          sys.stdout.close()
        #except:
        #  continue     

r = retriever()
r.implementation()         
