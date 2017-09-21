#!/usr/bin/python2
import os
import glob
from Evaluation import Evaluation
import ttest
from task1 import run_task
from task3a import task3a
from task3b import task3b
import SnippetGenerator

# save required file names
project_directory = os.getcwd()
raw_corpus_directory = raw_input("Enter the raw corpus directory (html files)(Full path): ")
output_directory = os.path.join(project_directory, "output")
evaluation_directory = os.path.join(project_directory, "evaluation_output")
t_test_directory = os.path.join(project_directory,"t_test")
file_names = ["task1_bm25.txt", "task1_tfidf.txt", "task1_lucene.txt",
              "task2_bm25.txt", "task2_tfidf.txt",
              "task3a_bm25.txt", "task3a_tfidf.txt"]

print "Select a task number\n\t1. Task - 1 " \
      "\n\t2. Task - 2 " \
      "\n\t3. Task - 3a" \
      "\n\t4. Task - 3b" \
      "\n\t5. Phase - 2" \
      "\n\t6. t-test" \
      "\n\t7. Snippet Generation" \
      "\n\t8. exit"
task = raw_input()
task = int(task)
if task == 1:
    model = raw_input("Enter the retreival model(bm25 or tfidf): ")
    run_task(1, model, raw_corpus_directory)

if task == 2:
    model = raw_input("Enter the retreival model(bm25 or tfidf): ")
    run_task(2, model, raw_corpus_directory)

if task == 3:
    model = raw_input("Enter the retreival model(bm25 or tfidf): ")
    task3a(model, raw_corpus_directory)

if task == 4:
    model = raw_input("Enter the retreival model(bm25 or tfidf): ")
    task3b(model)

if task == 5:
    if not os.path.exists(evaluation_directory):
        os.mkdir(evaluation_directory, 0755)

    for each_file in file_names:
        score = {}
        p_k = [5,20]
        f = open(os.path.join(output_directory, each_file), 'r')
        output = f.readlines()
        f.close()
        for line in output:
            words = line.split()
            if score.has_key(words[0]):
                score[words[0]].append((words[2],words[4]))
            else:
                score[words[0]] = []
                score[words[0]].append((words[2],words[4]))
        filename = os.path.join(evaluation_directory, each_file)
        e = Evaluation(score, p_k, filename)
        e.evaluation()

if task == 6:
    if not os.path.exists(t_test_directory):
        os.mkdir(t_test_directory, 0755)
    base_file = file_names[2]       # change filename for changing reference run
    base_file_path = os.path.join(evaluation_directory, base_file[0:-4] + "_ap.txt")
    for each_file in file_names:
        if each_file == base_file:
            continue
        each_file_path = os.path.join(evaluation_directory, (each_file[0:-4]) + "_ap.txt")
        result_file_name = each_file[0:len(each_file) - 4] + "_ttest.txt"
        result_file_name = os.path.join(t_test_directory, result_file_name)
        ttest.t_test(base_file_path, each_file_path, result_file_name)
if task == 7:
    file_name = os.path.join(output_directory, file_names[0])
    SnippetGenerator.generate_snippet(file_name)
