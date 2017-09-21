from bs4 import BeautifulSoup
import re
import string
import requests
import os
import glob
import operator
import math
import time
import sys
from collections import Counter

class Parser:
    def __init__(self):
        self.corpus_directory = ''      # this contains cleaned corpus directory
                                        # this variable is populated in generate_corpus() function
        self.stop_words = []

    def parse_file(self, file_name, stopped):     # file_name -> file containing raw html data
        parsed_text = ''
        f = open(file_name, 'r')
        html_page = f.read()
        soup = BeautifulSoup(html_page, 'html.parser')
        main_text = soup.get_text().encode('utf-8')

        special_chars = re.sub("[,.-:]", "", string.punctuation) # contains string of special chars
        special_chars = special_chars.replace('-', "")
        ignore_list = ['!', '@', '#', '$', '^', '&', '*', '(', ')', '_', '+', '=', '{', '[', '}', ']', '|',
                       '\\', '"', "'", ';', '/', '<', '>', '?', '%']
        main_text = main_text.translate(None, ''.join(ignore_list))    # delete chars present in special_chars
        main_text = main_text.replace(':', ' ')     # to split hours and minutes
        main_text = main_text.replace('-', ' ')     # to split the words containg '-' symbol
                                                    # eg: multi-targeted to 'multi', 'targeted'
        main_text = main_text.split()

        index = 0
        length = len(main_text)
        for i in range(length):     # to remove the content after AM and PM
            if 'AM' in main_text[length - i - 1]:
                # index = len(main_text) - i - 1
                break
            elif 'PM' in main_text[length - i - 1]:
                # index = len(main_text) - i - 1
                break
            main_text.pop(length - i - 1)
        # for i in range(index - len(main_text)): # pop number after AM and PM in main_text list
            # main_text.pop(index + i + 1)

        for each_word in main_text:
            each_word = each_word.lower()
            each_word = each_word.strip('.-,')   # remove '.', '-' from beginning and ending of the word
            # each_word = re.sub("x[a-z][0-9]", "", each_word)    #removing special chars
            '''if re.search("[0-9]", each_word):
                if(re.search("[a-z]", each_word)):
                    each_word = re.sub("[.,]", "", each_word)
                parsed_text += each_word + ' '
            else:
                each_word = re.sub("[.,]", "", each_word)   # since it is not a number, remove '.', ',' '''
            if each_word == '':
                continue
            if stopped:
                if each_word in self.stop_words:
                    continue
            parsed_text += each_word + ' '

        f.close()
        file_name = os.path.join(self.corpus_directory, file_name)
        # print file_name
        f = open(file_name, 'w')
        f.write(parsed_text)
        f.flush()
        f.close()

    def build_corpus(self, raw_corpus_directory, stopped = False):
        if stopped:
            self.corpus_directory = os.path.abspath(os.path.join(os.getcwd(), 'stopped_corpus'))
        else:
            self.corpus_directory = os.path.abspath(os.path.join(os.getcwd(), 'processed_corpus'))

        if stopped:
            f = open('common_words.txt', 'r')
            stop_words = f.readlines()
            self.stop_words = [i.strip() for i in stop_words]
            f.close()
        if not os.path.exists(self.corpus_directory):
            os.mkdir(self.corpus_directory, 0755)
            print "created directory", self.corpus_directory
        print "processing files in the corpus"
        os.chdir(raw_corpus_directory)
        files_list = glob.glob('*.html')
        for each_file in files_list:
            self.parse_file(each_file, stopped)
        print "processed files are saved into ", self.corpus_directory
        return self.corpus_directory


class InvertedIndexer:
    def __init__(self, corpus_directory):
        self.corpus_directory = corpus_directory
        self.docIDs = {}        # contains ID assigned for each document(text file)
        self.inverted_indexes = {}  # contains inverted indexes for each word
        self.doc_lengths = {}        #to store number of tokens in each document
                                    # key - doc ID; value - doc length
        self.tf_table = {}      # stores tf table
        self.df_table = {}
        self.corpus = {}


    def ngram_indexer(self, n):
        # generate doc Id's for each document using links(used to generate corpus)
        print "Generating Inverted Indexes for ", n," gram, using files in corpus directory ..."
        os.chdir(self.corpus_directory)
        files_list = glob.glob('*.html')
        id_of_doc = 1
        for each_file in files_list:
            self.docIDs[each_file[:len(each_file) - 5]] = id_of_doc
            id_of_doc += 1

        # populate inverted indexes dictionary with token and its
        # respective inverted index(another dictionary with dicID and tf)
        for each_file in files_list:
            f = open(each_file, 'r')
            data = f.read()
            f.close()
            each_file = each_file[:len(each_file)-5]    # to remove '.html' from end of the filename
            token_list = data.split()
            # self.corpus[each_file] = token_list
            # --------------------------------------------------------
            # remove stop words from token_list if stopping is enabled
            # --------------------------------------------------------

            if n == 1:
                self.doc_lengths[each_file] = len(token_list)   # to save number of tokens in each document
            else:
                # generate WORD's (word n-gram)
                ngram = zip(*[token_list[i:] for i in range(n)])
                token_list = []
                for each_token in ngram:
                    token_list.append(' '.join(list(each_token)))
                self.doc_lengths[each_file] = len(token_list)

            for each_token in token_list:
                if each_token not in self.inverted_indexes:
                    # create a dictionary and add it to inverted indexes
                    inv_index = {}
                    inv_index[each_file] = 1
                    self.inverted_indexes[each_token] = inv_index

                else:
                    # update tf
                    if each_file not in self.inverted_indexes[each_token]:
                        self.inverted_indexes[each_token][each_file] = 1
                    else:
                        self.inverted_indexes[each_token][each_file] += 1

    def stemmed_indexer(self, corpus = {}):
        print "Generating Inverted Indexes gram using stemmed corpus"
        doc_id = 1
        for each_file, file_content in corpus.viewitems():
            self.docIDs[each_file] = doc_id
            doc_id += 1
            self.doc_lengths[each_file] = len(file_content)
            word_count = dict(Counter(file_content))
            for each_word in file_content:
                if each_word not in self.inverted_indexes:
                    inv_index = dict()
                    inv_index[each_file] = word_count[each_word]
                    self.inverted_indexes[each_word] = inv_index
                else:
                    self.inverted_indexes[each_word][each_file] = word_count[each_word]
