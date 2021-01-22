import os

base = 'Test-corpus/Cleaned_files/'

# file = os.listdir(base)

# print(file)

probability_folder = "word_probability/"

words_prob = dict()
for i in range(500):
    file_string = open(probability_folder+'words_prob' + str(i), "r").read()
    ind_dict = eval(file_string)
    words_prob.update(ind_dict)
print(len(words_prob))  # 192632

files = os.listdir("Test-corpus/Cleaned_files/")

# print(files)

predict_folder = "predicted_tags/"

for file in files:
    open_file = open(base+file , "r")
    predictions = open(predict_folder+"predictions_"+file,"w+")
    for line in open_file:
        for word_tag in line.split():
            words=word_tag.split('_')[0]
            if words in words_prob:
                keyMax = max(words_prob[words],key = words_prob[words].get)
                predictions.write(words + "_" + keyMax + " ")	
            else :
                predictions.write(words + "_" + "UNC" + " ")
    open_file.close()
    predictions.close()
