import csv

with open('movie_dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    file1 = open("ok.txt","a")
    i=0
    for row in csv_reader:
            if(row[7]!='original_title'):
                file1.write('"'+row[7]+'",')
                file1.write("\n")
    file1.close()