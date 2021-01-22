from bs4 import BeautifulSoup
import os

access_directory = os.listdir("Test-corpus/")

write_directory = "Test-corpus/Cleaned_files/"


i=0
for ele in access_directory:
    access_directory[i]="Test-corpus/"+ele+"/"
    i=i+1

os.mkdir(write_directory)

for dirs in access_directory:
    files = os.listdir(dirs)
    for file in files:
        write_file = open(write_directory+file.split('.')[0]+".txt", "w+")
        filename = open(dirs+file)
        content = BeautifulSoup(filename, features="lxml")
        sent_arr = content.find_all("s")
        for sentence in sent_arr:
            for word in sentence.find_all("w"):
                text = word.get_text().strip()
                tag = word.get('c5')
                write_file.write(text + "_" + tag.split("-")[0] + " ")
        filename.close()
        write_file.close()

