import os

prob_folder = "word_probability/" 

files = os.listdir(prob_folder)

words_prob = dict()

for each in files:
	ind_dict=dict()
	file_string = open(prob_folder+each, "r").read()
	ind_dict = eval(file_string)
	words_prob.update(ind_dict)

inp = input("Enter a sentence : ")


print("\nThe word-tag string for above input is : \n")
for word in inp.split():
	if word in words_prob:
		keyMax = max(words_prob[word],key = words_prob[word].get)
		print(word + "_" + keyMax + " ")
	else :
		print(word + "_" + "UT" + " ")
