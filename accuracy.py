import os
from bs4 import BeautifulSoup

orig_files = os.listdir("Test-corpus/Cleaned_files/")

correct = 0
total = 0

orig_folder = "Test-corpus/Cleaned_files/"
pred_folder = "predicted_tags/"

for file in orig_files:
	with open(orig_folder+file,"r") as filename, open(pred_folder+"predictions_"+file,"r") as pred_filename :
		for line1, line2 in zip(filename, pred_filename):
			list_orig = line1.split()
			list_pred = line2.split()
			i=0
			for ele in list_orig:
				if ele==list_pred[i]:
					correct=correct+1
				total=total+1
				i=i+1
	print("Filename:"+file+" :: "+"True predictions(till this file):"+str(correct)+" :: "+"Total size:"+str(total)+"\n")

print("Accuracy : "+str(correct/total)+"\n")