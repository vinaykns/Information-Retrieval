#!/usr/bin/python2
from bs4 import BeautifulSoup
import os
import pdb
from Retriever import Retriever

class SnippetGen:

    def __init__(self, file_name):
        self.cwd = os.getcwd()
        self.file_name = file_name

    def get_queryresults(self,name):
        all_runs = os.path.abspath(os.path.join(self.cwd,'output'))
        os.chdir(all_runs)
        results = {}
        if name == "bms25":
          bms25 = open(self.file_name,'r')
          for line in bms25.readlines():
            words = line.split()
            if results.has_key(words[0]):
              results[words[0]].append((words[2],words[4]))
            else:
              results[words[0]] = []
              results[words[0]].append((words[2],words[4]))
         
        bms25.close()
        os.chdir(self.cwd)
        return results
           
       

    def get_snippet(self,query,results):        
        processed_corpus = os.path.abspath(os.path.join(self.cwd,'processed_corpus'))
        os.chdir(processed_corpus)
        results = results[0:10]
        query = query.split()
        query_set = set()
        for word in query:
          query_set.add(word)
        
        for result in results:
          document_set = set()
          result = result[0] + '.html'
          document = open(result,'r')
          doc_string = document.read()
          doc_string = doc_string.split()

          for word in doc_string:
            document_set.add(word)

          common_words = query_set.intersection(document_set)
          snippet = []
          for word in doc_string:
            if word in common_words:
              snippet.append('"'+word+'"')
            else:
              snippet.append(word)

          document.close()
          print "Doc_Id",":",result
          print " ".join(snippet)
          print '\n'
        os.chdir(self.cwd)
          
          


def generate_snippet(file_name):
    relevant_list = open('cacm.rel','r')
    query_relevant = {}
    for line in relevant_list.readlines():
      words = line.split()
      if query_relevant.has_key(words[0]):
        doc_no = words[2][5:]
        doc_no = str(doc_no)
        doc = 'CACM-' + (4 - len(doc_no))*'0' + doc_no
        query_relevant[words[0]].append(doc)
      else:
        query_relevant[words[0]] = []
        doc_no = words[2][5:]
        doc = 'CACM-' + (4 - len(doc_no))*'0' + doc_no
        query_relevant[words[0]].append(doc)

    #Get query_dict from the file cacm.query.txt
    f = open('cacm.query.txt','r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()
    rawquery_dict = {}
    for i in range(64):
      query_no = (soup.find('docno')).text.encode('utf-8')
      (soup.find('docno')).decompose()
      query = (soup.find('doc')).text.encode('utf-8')
      (soup.find('doc')).decompose()

      query_no = query_no.strip(" ")
      rawquery_dict[query_no] = query

    r = Retriever("", "")
    query_dict = {}
    for query_no, raw_query in rawquery_dict.viewitems():
      query_dict[query_no] = r.process_query(raw_query, True)

    print "Enter the query no"
    no = raw_input()
    no = str(no)
    query = query_dict[no]
    print query
    s = SnippetGen(file_name)
    query_results = s.get_queryresults(name = 'bms25')
    results = query_results[no]
    # pdb.set_trace()
    s.get_snippet(query,results)

