from bs4 import BeautifulSoup
import os

access_directory = os.listdir("Train-corpus/")

write_directory = "Train-corpus/Cleaned_files/"

# print(access_directory)

i=0
for ele in access_directory:
	access_directory[i]="Train-corpus/"+ele+"/"
	i=i+1

os.mkdir(write_directory)

def return_tag(word):
	return word.get('c5')

def text_tag(sentence, write_file):
	for word in sentence.find_all("w"):
		text = word.get_text().strip()
		tag = word.get('c5')
		if "-" not in tag:
			write_file.write(text + "_" + tag + " ")
		else:
			write_file.write(text + "_" + tag.split("-")[0] + " ")
			write_file.write(text + "_" + tag.split("-")[1] + " ")
tag_prob = dict()
tag_freq = dict()
tag_freq['.'] = 0

sequence = []
def transition(sentence,write_file):
	words = sentence.find_all('w')
	sequence = []
	sequence.append(['^'])
	for word in words:
		tag = word.get('c5')
		sequence.append(tag.split("-"))
	sequence.append(['.'])

	length = len(sequence)
	for i  in range(length-1):
		tag_freq['.'] = tag_freq['.'] + 1
		for tag1 in sequence[i]:
			if tag1 in tag_freq:
				tag_freq[tag1] = tag_freq[tag1] + 1
			else:
				tag_freq[tag1] = 0
			for tag2 in sequence[i+1]:
				comb = tag1 + '_' + tag2
				if comb in tag_prob:
					tag_prob[comb] = tag_prob[comb] + 1
				else:
					tag_prob[comb] = 0

#********************************* for simple word tag pair creation ***********************************

# for dirs in access_directory:
# 	files = os.listdir(dirs)
# 	for file in files:
# 		write_file = open(write_directory+file.split('.')[0]+".txt", "w+")
# 		filename = open(dirs+file)
# 		content = BeautifulSoup(filename, features="lxml")
# 		sent_arr = content.find_all("s") # handling the sentence tags
# 		for sentence in sent_arr:
# 			for word in sentence.find_all("w"):
# 				text = word.get_text().strip()
# 				tag = word.get('c5')
# 				if "-" in tag :
# 					write_file.write(text + "_" + tag.split("-")[0] + " ")
# 					write_file.write(text + "_" + tag.split("-")[1] + " ")
# 				else :
# 					write_file.write(text + "_" + tag + " ")	
# 		filename.close()
# 		write_file.close()
#***************************************************************************************************


#************************* for getting sentences and transition probabilities **************************************************

for dirs in access_directory:
	files = os.listdir(dirs)
	for file in files:
		write_file = open(write_directory+file.split('.')[0]+".txt", "w+")
		filename = open(dirs+file)
		content = BeautifulSoup(filename, features="lxml")
		sent_arr = content.find_all("s")  # handling the sentence tags
		for sentence in sent_arr:
			text_tag(sentence, write_file)
			transition(sentence,write_file)
		filename.close()
		write_file.close()
	
all_tags = tag_freq.keys()

for tag1 in all_tags:
	for tag2 in all_tags:
		comb = tag1 + '_' + tag2
		if comb in tag_prob: 
			tag_prob[comb] = tag_prob[comb]/tag_freq[tag1]
		else:
			tag_prob[comb] = 0

transition = open('transition.txt', 'w')
transition.write(str(tag_prob))
transition.close()


#**************************************************************************************************************

# index_arr = []
# for i in range(26):
#     index_arr.append(chr(65+i))
# for i in range(5):
#     index_arr.append(str(1+i))
# base = "A0"
# j = 0
# for index in index_arr:
#     write_file = open("cleanTrain" + str(j) + ".txt", "w+")
#     j = j+1
#     filename = base + index
#     file = open(filename + ".xml")
#     content = BeautifulSoup(file, features="lxml")
#     sent_arr = content.find_all("s")
#     for sentence in sent_arr:
#         for word in sentence.find_all("w"):
#             text = word.get_text().strip()
#             tag = word.get('pos')
#             write_file.write(text + "_" + tag + " ")
#     file.close()
#     write_file.close()



		
	# print(tags)