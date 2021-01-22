from bs4 import BeautifulSoup
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)


total = 0
correct_count = 0
hello = dict()
hello['total'] = 0
hello['correct'] = 0

open_file = open("frequency.txt", "r").read()

dict1 = eval(open_file)

dict_word={} 
dict_tag={}


for key in dict1:
	words=key.split('_') 
	if(len(words) != 2):
		continue
	if words[0] in dict_word :
	    dict_word[words[0]]=dict_word[words[0]]+dict1[key]
	else :
	    dict_word[words[0]]=dict1[key]

	if words[1] in dict_tag :
	    dict_tag[words[1]]=dict_tag[words[1]]+dict1[key]
	else :
	    dict_tag[words[1]]=dict1[key]


#***************************************************** finding P(e/l) *****************************************************

word_by_tag=dict()

for tag in dict_tag.keys() :
	wdict=dict()
	for word in dict_word.keys() :
		wt=word+"_"+tag
		if wt in dict1.keys() :
			freq=dict1[wt]
			wdict[wt.split("_")[0]]=(freq/dict_tag[tag])
		else :
			wdict[wt.split("_")[0]]=0
	word_by_tag[tag]=wdict


# ------------------------------------------------------- #

#               Viterbi Algorithm                         #



matrix = np.zeros((57,57),dtype='int64')
i=0
tag_dict=dict_tag;
for tag in tag_dict :
	tag_dict[tag]=i
	i=i+1

transition = open('transition.txt', 'r').read()

transition_prob = eval(transition)
emission_prob = word_by_tag

print(emission_prob.keys())

access_directory = os.listdir("Test-corpus/")
i=0
for ele in access_directory:
	access_directory[i]="Test-corpus/"+ele+"/"
	i=i+1

tags =[x for x in dict_tag.keys()]
print(tags)
print("/n")
def printArray(matrix):
	for row in matrix:
		print(row)

output = open('log.txt', 'w')
for dirs in access_directory:
	if dirs == "Test-corpus/Cleaned_files/":
		continue
	files = os.listdir(dirs)
	print(dirs)
	for file in files:
		print(file)
		filename = open(dirs+file)
		content = BeautifulSoup(filename, features="lxml")
		sent_arr = content.find_all("s")  # handling the sentence tags
		for sentence in sent_arr:
			words = sentence.find_all("w")
			length = len(words)

			# print(words)
			# print(length)
			res_tag= np.zeros(length,dtype='int64')
			product_so_far=1
			for k in range(length):
				if k == 0:
					tag1 = '^'
				else:
					tag1=tags[res_tag[k-1]]
				max_prob = -200000
				a=1
				for i in range(57):
					if words[k].get_text().strip() in emission_prob[tags[i]].keys():
						a=0
				if a==1:
					res_tag[k]=0
					continue				
				for i in range(57):
					
					tag2=tags[i]	
					# print(tag2)
					# print("\n")
					
					TP = transition_prob[tag1 + '_' + tag2]
					word = words[k].get_text().strip()
					# print(word)
					EP = emission_prob[tag2][word]
					value =product_so_far * TP * EP
					if value > max_prob:
						max_prob = value
						res_tag[k] =i
				product_so_far=max_prob
			tcount = 0
			ccount = 0
			actual = []
			for word in words:
				actual.append(word.get('c5'))
			for i in range(length):
				tcount = tcount + 1
				if "-" not in actual[i]:
					if(actual[i]== tags[res_tag[i]]):
						ccount = ccount + 1
					matrix[tag_dict[actual[i]]][tag_dict[tags[res_tag[i]]]]+=1
				else:
					if actual[i].split("-")[0]== tags[res_tag[i]] or actual[i].split("-")[1]== tags[res_tag[i]]:
						ccount = ccount + 1
						matrix[tag_dict[tags[res_tag[i]]]][tag_dict[tags[res_tag[i]]]]+=1
					matrix[tag_dict[actual[i].split("-")[0]]][tag_dict[tags[res_tag[i]]]]+=1
				# print(actual[i],"  ",tags[res_tag[i]])				
			# print(tcount,"    ",ccount)
			hello['total'] = hello['total'] + tcount
			hello['correct'] = hello['correct'] + ccount
			# print(res_tag)
		print(file,"  ",hello)
	# 	break
	# break

print(dict_tag.keys())
print(matrix)
print(hello)