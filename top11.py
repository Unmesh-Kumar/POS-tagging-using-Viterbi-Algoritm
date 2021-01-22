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

# sorted_words = sorted(dict_word.items(), key=lambda a : a[1])
# sorted_tag = sorted(dict_tag.items(), key=lambda a : a[1])

# sorted_words.reverse()
# sorted_tag.reverse()

# len_words = len(sorted_words)
# len_tag = len(sorted_tag)

# print(len_words) # 192632
# print(len_tag) # 87 total tags(including multi-tags), out of which only 57 are separated ones.

# print(sorted_tag)

# write_file = open("top10.txt", "w")

# write_file.write("TOP 10 words based on frequency\n")
# for i in range(0,10):
# 	write_file.write(str(sorted_words[i]))

# write_file.write("\n\n\n")

# write_file.write("TOP 10 tags based on frequency\n")
# for i in range(0,10): # min(10,len_tag)
# 	write_file.write(str(sorted_tag[i]))

# # print(len_tag)
# # print(len_words)

# # plt.bar(dict_tag.keys(), dict_tag.values())
# # plt.show()

# ten_words = []
# ten_freqs_words = []

# for i in range(0,10):
# 	ten_freqs_words.append(sorted_words[i][1])
# 	ten_words.append(sorted_words[i][0])

# plt.bar(ten_words, ten_freqs_words)
# # plt.show()

# ten_tags = []
# ten_freqs_tags = []

# for i in range(0,10):
# 	ten_freqs_tags.append(sorted_tag[i][1])
# 	ten_tags.append(sorted_tag[i][0])

# plt.bar(ten_tags, ten_freqs_tags)
# plt.show()


#---------------------------------------------------------- WEEK 4 ----------------------------------------------------------

# words_prob = dict()
# len_word_tag = len(dict1)
# arr_tags = dict_tag.keys() 
# for key,val in dict_word.items() :
# 	word_dict = dict()
# 	for tag in arr_tags:
# 		w_t = key + "_" + tag
# 		word_count = val
# 		try:
# 			word_tag_count = dict1[w_t]
# 		except KeyError:
# 			word_tag_count = 0
# 		word_dict[tag] = word_tag_count/word_count
# 	words_prob[key] = word_dict
# 	# print(word_dict)

# dict_size = len(words_prob)
# print(dict_size) #192632

# words_in_one_file = dict_size/500
# index = 0
# fno = 0
# dic = dict()

# prob_folder = "word_probability/"

# prob_file = open(prob_folder+"words_prob" + str(fno), "w")
# for key in words_prob:
#     if(index > words_in_one_file):
#         index = 0
#         prob_file.write(str(dic))
#         prob_file.close()
#         fno = fno + 1
#         prob_file = open(prob_folder+"words_prob" + str(fno), "w")
#         dic = dict()
#     dic[key] = words_prob[key]
#     index = index + 1
# prob_file.close()
# if(len(dic) > 0):
#     prob_file = open(prob_folder+"words_prob" + str(fno), "w")
#     prob_file.write(str(dic))
#     prob_file.close()


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



def recurse_tags(rm, i, sentence, hello):
	tcount = 0
	ccount = 0
	words = sentence.find_all('w')
	actual = []
	predicted = []
	for word in words:
		actual.append(word.get('c5'))
	size = len(rm[i]) - 1
	while size:
		tag = tags[i]
		predicted.insert(0, tag)
		i = rm[i][size]
		size = size - 1
	for i in range(len(predicted)):
		tcount = tcount + 1
		if "-" not in actual[i]:
			if(actual[i]== predicted[i]):
				ccount = ccount + 1
			matrix[tag_dict[actual[i]]][tag_dict[predicted[i]]]+=1
		else:
			if actual[i].split("-")[0]== predicted[i] or actual[i].split("-")[1]== predicted[i]:
				ccount = ccount + 1
				matrix[tag_dict[predicted[i]]][tag_dict[predicted[i]]]+=1
			matrix[tag_dict[actual[i].split("-")[0]]][tag_dict[predicted[i]]]+=1
		print(actual[i],"  ",predicted[i])
		
	print(tcount,"    ",ccount)
	hello['total'] = hello['total'] + tcount
	hello['correct'] = hello['correct'] + ccount

	print(str(tcount) + str(ccount))

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
			dp = []
			rm = []
			for i in range(57):
				dp.append([])
				rm.append([])
			for i in range(57):
				dp[i].append(1)
				rm[i].append(1)
				for j in range(length):
					dp[i].append(0)
					rm[i].append(0)
			for k in range(1, length+1):
				for i in range(57):
					max_prob = -200000
					tag2=tags[i]	
					# print(tag2)
					# print("\n")
					for j in range(57):
						
						tag1=tags[j]
						# print(str(j) + " " + tag1)
						if k == 1:
							tag1 = '^'

						# print(tag1 + " " + tag2)
						TP = transition_prob[tag1 + '_' + tag2]
						# print(TP)
						word = words[k-1].get_text().strip()
						if word not in emission_prob[tag2].keys() :
							word="principal"
							# print(word)
							# print(EP)
						EP = emission_prob[tag2][word]
						value = dp[j][k-1] * TP * EP
						if value > max_prob:
							max_prob = value
							rm[i][k] = j
					dp[i][k] = max_prob
			# print("rm")
			# for x in range(len(rm)):
			# 	print(rm[x])
			# print("dp")
			# for x in range(len(dp)):
			# 	print(dp[x])
			max_proba =-1
			start = 56
			for i in range(57):
				tag1=tags[i]
				tag2 = '.'
				TP = transition_prob[tag1 + '_' + tag2]
				value = dp[i][length] * TP
				if value > max_proba:
					max_proba = value
					start = i
				# print("in->",start)
			print("start=",start)
			recurse_tags(rm, start, sentence, hello)
		print(file,"  ",hello)
		break
	break	

print(dict_tag.keys())
print(matrix)
print(hello)