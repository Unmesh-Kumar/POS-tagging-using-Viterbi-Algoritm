import os 
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)

orig_files = os.listdir("Test-corpus/Cleaned_files/")

orig_folder = "Test-corpus/Cleaned_files/"
pred_folder = "predicted_tags/"

tag_dict = dict()

for file in orig_files :
	filename = open(orig_folder+file,"r")
	text = filename.read()
	for word_tag in text.split() :
		if not word_tag.split('_')[1] in tag_dict :
			tag_dict[word_tag.split('_')[1]]=1
	filename.close()


i=0
for tag in tag_dict :
	tag_dict[tag]=i
	i=i+1

matrix = np.zeros((87,87),dtype='int64')

for file in orig_files:
	with open(orig_folder+file,"r") as filename, open(pred_folder+"predictions_"+file,"r") as pred_filename :
		for line1, line2 in zip(filename, pred_filename):
			list_orig = line1.split()
			list_pred = line2.split()
			i=0
			for each in list_orig:
				row=tag_dict[each.split('_')[1]]
				col=tag_dict[list_pred[i].split('_')[1]]
				matrix[row][col]=matrix[row][col]+1
				i=i+1

print("The confusion matrix is : \n")

print(matrix)

filename = open("confusion_matrix.txt","w")
filename.write(str(matrix))
filename.close()