import os


train_dict = {}
files = os.listdir('Train-corpus/Cleaned_files/')
directory = 'Train-corpus/Cleaned_files/'
# print(len(files)) = 520
for filename in files:
	file = open(directory+filename)
	for line in file:
	    for words in line.split():
	    	if words in train_dict :
	    		train_dict[words]=train_dict[words]+1
	    	else :
	    		train_dict[words]=1
	file.close()

length=len(train_dict) # 255506
print(length)

write_file = open("frequency.txt", "w+")
write_file.write(str(train_dict))
write_file.close() 
