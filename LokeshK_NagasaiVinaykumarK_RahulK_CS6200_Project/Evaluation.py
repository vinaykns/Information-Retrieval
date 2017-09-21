#!/usr/bin/python2

import pdb
from operator import itemgetter
import os

class Evaluation:

    def __init__(self, query_results, p_k, file_name):
        self.query_results = query_results #Give the document results corresponding to the query_id.
        self.p_k = p_k
        self.file_name = file_name[0:len(file_name) - 4]

    def evaluation(self):
        query_relevant = {}
        temp_query_results = self.query_results

        #Store the relevant documents corresponding to a query into a dictionary.
        '''relevant = open('cacm.rel','r')
        for line in relevant.readlines():
          words = line.split()
          if query_relevant.has_key(words[0]):
            query_relevant[words[0]].append(words[2])
          else:
            query_relevant[words[0]] = []
            query_relevant[words[0]].append(words[2])

        relevant.close()'''

        relevant_list = open("cacm.rel", 'r')
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
        relevant_list.close()

        #Calculate the recall and precision scores for a run.
        precision_recall_query = {}
        scores = {}
        seq_docs = {}
        MAP_query_id = []
        MAP = [] 
        MRR = []
        p_5_dict = {}
        p_20_dict = {}
        p_5 = open(self.file_name+ '_p_5.txt','w')
        p_20 = open(self.file_name+ '_p_20.txt','w')
        query_results = {}
        for key,value in temp_query_results.viewitems():
            query_results[int(key)] = value

        for query_id,docs in query_results.viewitems():
          try:
            total_relevant_docs_query = len(query_relevant[query_id])
            precision_recall_query[query_id] = {}
            scores[query_id] = {}
            seq_docs[query_id] = []
            precision_sum = 0
            relevance_rank = 0
            relevant_doc = 0
            relevancy = 0
            count = 0
            p_count = 0

            for doc in docs:
              if doc[0] in query_relevant[query_id]:
                relevant_doc += 1
                relevancy = 1
                precision_sum += float(relevant_doc)/(docs.index(doc)+1)

              if relevant_doc == 1 and count < 1:
                count += 1
                relevance_rank = 1 / float(docs.index(doc)+1)

              p_count += 1  
              scores[query_id][doc[0]] = doc[1]
              precision = float(relevant_doc)/(docs.index(doc)+1)
              recall = float(relevant_doc)/ len(query_relevant[query_id])
              precision_recall_query[query_id][doc[0]] = (precision,recall)
              seq_docs[query_id].append(doc[0])
              if p_count == self.p_k[0]:
                p_5_dict[query_id] = precision 
                #p_5.write("{} {}".format(query_id,precision) + '\n')

              if p_count == self.p_k[1]:
                p_20_dict[query_id] = precision 
                #p_20.write("{} {}".format(query_id,precision) + '\n')

            avg_precision = float(precision_sum)/relevant_doc
            MAP_query_id.append(query_id)
            MAP.append(avg_precision)
            MRR.append(relevance_rank) 
          except (KeyError,ZeroDivisionError) as e:
            continue

        file_map = open(self.file_name+ '_map.txt','w')
        file_ap = open(self.file_name+ '_ap.txt', 'w')
        file_mrr = open(self.file_name+ '_mrr.txt','w')
        total_querys = [int(key) for key in precision_recall_query]
        total_querys.sort()
        total_querys = [key for key in total_querys]
        map_result = sum(MAP)/len(MAP)
        mrr_result = sum(MRR)/len(MRR)

        for i in range(len(MAP)):
            file_ap.write('{} {}'.format(MAP_query_id[i],MAP[i]) + '\n')

        file_map.write("{}".format(map_result))
        file_mrr.write("{}".format(mrr_result))
        file_map.close()
        file_mrr.close() 
        file1 = open(self.file_name+ '_precision_recall.csv','w')
        file1.write("Query_id, Rank, Doc_id, Score, Relevant/NRelevant, Precision, Recall" + '\n')
        for query in total_querys:
          rank = 0
          p_5.write("{} {}".format(query,p_5_dict[query]) + '\n')
          p_20.write("{} {}".format(query,p_20_dict[query]) + '\n')
          for doc_id in seq_docs[query]:
            rank += 1
            if doc_id in query_relevant[query]:
              file1.write("{}, {}, {}, {}, {}, {}, {}".format(query,rank,doc_id,scores[query][doc_id],1,precision_recall_query[query][doc_id][0],precision_recall_query[query][doc_id][1]) + '\n')
            else:
              file1.write("{}, {}, {}, {}, {}, {}, {}".format(query,rank,doc_id,scores[query][doc_id],0,precision_recall_query[query][doc_id][0],precision_recall_query[query][doc_id][1]) + '\n')

        file1.close()
        p_5.close()
        p_20.close() 
