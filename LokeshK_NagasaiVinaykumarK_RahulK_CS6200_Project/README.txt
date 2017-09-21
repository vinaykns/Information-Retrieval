Files:
------------------------------------------------------------------
project.py --> contains the starting code for the project
Indexer.py	--> this file contains classes Parser, InvertedIndexer 		          which are used for parsing and generating inverted 	          indexes
Retreiver	--> contains Retreiver class used for calculating 		          scores for documents using bm25 or tfidf models
task1.py	--> code required for task 1(three base runs) and task2 		    (query expansion)
task3a.py	--> stopping with no stemming
task3b.py 	--> contains code required for stemming
Evaluation.py	--> contains code for phase-2 of the project

Platform and Required Libraries:
------------------------------------------------------------------
Python 2.7
BeautifulSoup
scipy (for calculating p-values)

(this code is run on windows platform using pycharm)


Compile and Run:
------------------------------------------------------------------
Use the following command

$ python project.py

This will ask for user to input the file directory for corpus as shown below,

Enter the raw corpus directory (html files): 
D:\Information_Retreival\Project\CCAM_Corpus

Next choose the task number from the list.
Select a task number
	1. Task - 1 
	2. Task - 2 
	3. Task - 3a
	4. Task - 3b
	5. Phase - 2
	6. t-test
	7. Snippet Generation


For Tasks 1 - 4, when asked enter model "tfidf" or "bm25"

(Run all these in order)
For tasks from 5-7, place lucene results file "task1_lucene.txt" file in directory named output

Output:
------------------------------------------------------------------
1. Output for runs are stored in directory called "output" 
2. "relevance_output" folder contains output for phase - 2 of the       project
3. t_test : contains t-values and p-values for all seven runs
processed corpus is stored in "processed_corpus"
stopped_corpus contains processed files for task 3a




