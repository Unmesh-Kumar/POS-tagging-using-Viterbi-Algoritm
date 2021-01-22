import os
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)


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


i=0
tag_dict=dict_tag;
for tag in tag_dict :
	tag_dict[tag]=i
	i=i+1

transition = open('transition.txt', 'r').read()

transition_prob = eval(transition)
emission_prob = word_by_tag

tags =[x for x in dict_tag.keys()]

inp = input("Enter a sentence : ")

words = inp.split(" ")
length = len(words)
# print(words)
# print(length)
res_tag= np.ones(length,dtype='int64')
product_so_far=1
for k in range(length):
	if k == 0:
		tag1 = '^'
	else:
		tag1=tags[res_tag[k-1]]
	max_prob = -200000
	for i in range(57):
		
		tag2=tags[i]	
		# print(tag2)
		# print("\n")
		
		TP = transition_prob[tag1 + '_' + tag2]
		word = words[k]
		if word in emission_prob[tag2].keys() :
			EP = emission_prob[tag2][word]
		else:
			EP=0
		value =product_so_far * TP * EP
		if value > max_prob:
			max_prob = value
			res_tag[k] =i
	product_so_far=max_prob

print("\nThe word-tag string for above input is : \n")
for i in range(length):
	print(words[i],":",tags[res_tag[i]])