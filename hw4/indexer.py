#!/usr/bin/python2

import requests
import os
import sys
import glob
from bs4 import BeautifulSoup
from collections import Counter
import operator
import math
import re
import string
import matplotlib.pyplot as plt
import pdb


class Indexer:

    def __init__(self):
      self.name = 'input_urls.txt'
      self.cwd = os.getcwd()
 

    #Build a raw corpse from the list of url's collected the from hw1
    def build_raw_corpus(self):            
      urls = self.name
      file1 = open(urls,'r')
      current_dir = self.cwd
      if (os.path.isdir(current_dir+"/raw_corpus")):
        DIR = current_dir+"/raw_corpus"
        print len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) 
        print "The rawcorpus is already collected"
  
      else:
        os.mkdir(current_dir+"/raw_corpus")
        os.chdir("raw_corpus")
        cwd = os.getcwd()
        for rawurl in file1.readlines():
          try:
            url = rawurl.split("\n")
            request = requests.get(unicode(url[0]))
            request_page = request.text
            req = url[0].split('/wiki/')  
            raw_doc = open(req[1]+".txt",'w')
            raw_doc.write(request_page.encode('utf-8'))
            raw_doc.close()
          except:
            if (req[1]=="M/s"):
              raw_doc = open('MetersPerSecond.txt','w')
              raw_doc.write(request_page.encode('utf-8'))
              raw_doc.close()

            elif (req[1]=="HIV/AIDS"):
              raw_doc = open('Hivaids.txt','w')
              raw_doc.write(request_page.encode('utf-8'))
              raw_doc.close()
              #pdb.set_trace()

            #pdb.set_trace()
            continue

      file1.close()
    
    #Collect the raw files from the corpus, parse the document and store it in the directory parsed_corpus:
    def parsed_corpus(self):
      current_dir = self.cwd
      notreq_div = ['toc', 'thumb', 'navbox', 'reflist']
      notreq_table = ['vertical-navbox', 'wikitable']
      notreq_tag = ['sup', 'dl', 'table']
      os.chdir(current_dir+"/raw_corpus")
      tobe_processed_files = glob.glob('*.txt')
      for each in tobe_processed_files:
        raw = open(each,'r')
        raw_file = raw.read()
        raw_file = raw_file.decode('utf-8')
        soup = BeautifulSoup(raw_file,'html.parser') 
        required_content = soup.find("div", {"id": "mw-content-text"})
        
        for section in notreq_div:
          try:  
            for div in required_content.find_all('div', {'class': section}):
              div.decompose()
          except:
            continue 

        for section in notreq_table:
          try:
            for div in required_content.find_all('table', {'class': section}):
              div.decompose()
          except:
            continue

        for section in notreq_tag:
          try: 
            for div in required_content.find_all(section):
              div.decompose()
          except:
            continue 

        try:  
          for div in required_content.find_all('span', {'class': 'mw-editsection'}):
            div.decompose()
        except:
          continue

        raw_text = required_content.get_text()
        raw_text = raw_text.encode('utf-8','ignore')
        raw_text = raw_text.translate(None, string.punctuation)
        raw_text = re.sub(r'x[a-z][0-9]',"", raw_text) 
        raw_text = raw_text.split()
        processed_text = ' '
        for index in range(len(raw_text)):
          try:
            if raw_text[index][0:1] == "-":
              raw_text[index] = raw_text[index][1:]
              raw_text[index] = raw_text[index].lower()
            if raw_text[index] == "-":
              continue
         
            self.word = raw_text[index] 
            if self.num_there()=="False":
              raw_text[index] = raw_text[index].strip('.,-')
              raw_text[index] = raw_text[index].strip(',')
      
            processed_text += raw_text[index] + ' '
          except:
            continue

        raw.close()

      #Check if the directory is present, if yes print the no of files in the corpus 
      #Else create a directory and store all the processed documents

        if not (os.path.isdir(current_dir + "/processed_corpus")):
          DIR = current_dir+"/processed_corpus"    
          os.mkdir(DIR) 
   
        fname = each.split(".txt")
        fname[0] = fname[0].translate(None, string.punctuation)
        fname[0] = current_dir + "/processed_corpus" + "/" + fname[0]
        process_file = open(fname[0]+".txt",'w')
        process_file.write(processed_text)
        process_file.close()   
       

    #Check if the word has any digit.
    def num_there(self):
      word = self.word
      return bool(re.search(r'\d',word))
  
    #Implementation of inverted index.
    def invertedindex(self,n):
      self.n = n
      cwd = self.cwd
      os.chdir(cwd)
      #print "Inverted Index"
      #pdb.set_trace()
      os.chdir(cwd + "/processed_corpus")
      total_files = glob.glob('*.txt')
      docId = {}
      counter=0

      #Initialize the docId for each file
      for each in total_files:
        docId[each[:len(each)-4]] = counter
        counter += 1

      #Tokenize the words from each document.
      self.docId = docId
      self.total_docs = len(docId.viewkeys())
      noof_tokens_doc = {}
      inverted_index = {}
      inv_index = {}

      for each in total_files:
        parsed = open(each)
        parsed_file = parsed.read()
        text = parsed_file.split()
        noof_tokens_doc[each[:len(each)-4]] = len(text) 

        #Tokenize the words based on the n-gram.
        cnt = Counter()
        if n == 1:
          for word in text:
            cnt[word] += 1
          for k,v in cnt.viewitems():
            result = inverted_index.get(k,"Empty")
            if result is "Empty":
              inverted_index[k] = {}
              inverted_index[k][docId[each[:len(each)-4]]] = v
            else:
              inverted_index[k][docId[each[:len(each)-4]]] = v

          self.inverted_index = inverted_index  
   
        elif n != 1:
          tuple_values = zip(*[text[i:] for i in range(n)])
          gram_list = [] 
          for element in tuple_values:
            conv = list(element)
            comb = ' '.join(conv)
            gram_list.append(comb)

          for biword in gram_list:
            cnt[biword] += 1

          for k,v in cnt.viewitems():
            result = inv_index.get(k, "Empty")
            if result is "Empty":
              inv_index[k] = {}
              inv_index[k][docId[each[:len(each)-4]]] = v
            else:
              inv_index[k][docId[each[:len(each)-4]]] = v

          self.inverted_index = inv_index
            
        else:      
          print "Please specify the appropriate n-gram"

      self.noof_tokens_doc = noof_tokens_doc
      #pdb.set_trace()
      os.chdir(cwd)
      return inverted_index               

    def tf_table(self):
      index = self.inverted_index
      table_tf = {}
      frequency_count = 0

      for key,value in index.viewitems():
        frequency_count = 0
        for k,v in value.items():
          frequency_count += v
        
        table_tf[key] = frequency_count
      
      #Get the result sorted in descending order.
      table_sorted = sorted(table_tf.items(), key=operator.itemgetter(1), reverse=True)
      self.tf_words = table_sorted
             
    def df_table(self):
      index = self.inverted_index
      terms = []
      df_words = {}
      for key in index.viewkeys():
        terms.append(key)
         
      terms = sorted(terms)
      
      #sys.stdout = open('gram_dftable.txt', 'w')
      for term in terms:
        docs = []
        for doc in index[term].viewkeys():
          docs.append(doc)

        df = len(index[term].viewkeys())
        df_words[term] = df 
        #print term,docs,df
      
      #sys.stdout.close()

      self.df_words = df_words
      return df_words

    def stopwordcalculation(self):
      tf_words = self.tf_words
      df_words = self.df_words
      total_docs = self.total_docs
      stopword_list = {}
      tfidf = 0.0
      for key,value in df_words.viewitems():
        idf = math.log(float((total_docs)/(df_words[key])),2)
        stopword_list[key] = idf
      
      sorted_stopword_list = sorted(stopword_list.items(), key=operator.itemgetter(1), reverse=False)
      sys.stdout = open('stopword-list', 'w')
      for collection in sorted_stopword_list:
        print collection[0],collection[1]   

      sys.stdout.close() 
      

    def tokens_doc(self):
      temp = self.noof_tokens_doc
      return temp          

    def total_documents(self):
      #pdb.set_trace()
      total_docs = self.total_docs
      return total_docs
    
    def document_Ids(self):
      docId = self.docId
      return docId

#file = 'input_urls.txt' 
#e = Indexer()
#e.build_raw_corpus()
#e.parsed_corpus()
#n = 1
#e.invertedindex(n)
#e.tf_table()


#e.invertedindex(n)
#e.df_table()

#e.invertedindex(n)
#e.tf_table()
#e.df_table()
#e.stopwordcalculation()
