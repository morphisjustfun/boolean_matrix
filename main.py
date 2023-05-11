import os
from nltk.stem.snowball import SnowballStemmer

def save_matrix(matrix, files):
    # save into output/boolean_matrix.txt
    with open('output/boolean_matrix.txt', 'w') as f:
        # first write columns
        for i in range(len(files)):
            f.write(files[i] + ' ')
        f.write('\n')
        for row in matrix:
            for column in row:
                f.write(str(column) + ' ')
            f.write('\n')

stopwords = []
with open('input/stoplist.txt', 'r') as f:
    for line in f:
        stopwords.append(line.strip())

stemmer = SnowballStemmer("spanish")
files = os.listdir('documents/')
files.sort()

words = []
for file in files:
    with open('documents/' + file, 'r') as f:
        for line in f:
            for word in line.split():
                words.append(word)

filtered_words = [word for word in words if word not in stopwords]
roots = []

for word in filtered_words:
    roots.append(stemmer.stem(word))

# for each word make the boolean matrix, row = word, column = document
boolean_matrix = []
# init
for word in roots:
    initial = [word] + [0] * len(files)
    boolean_matrix.append(initial)

for i in range(len(roots)):
    for j in range(len(files)):
        if roots[i] in open('documents/' + files[j]).read():
            boolean_matrix[i][j + 1] = 1

# 1
save_matrix(boolean_matrix, files)

# make a query like first1 AND first2 AND first3 NOT second1
query = input('Enter query: ')
query = query.split()
# 2
# the boolean_matrix to make logical operations over the words
# first make a list with the words in the query
# then make a list with the operations
query_words = []
query_operations = []

for word in query:
    if word == 'AND' or word == 'OR' or word == 'NOT':
        query_operations.append(word)
    else:
        query_words.append(word)

# make a list with the indexes of the words in the query
binary_list = []
for word in query_words:
    for i in range(len(boolean_matrix)):
        if word == boolean_matrix[i][0]:
            binary_list.append(boolean_matrix[i][1:])

# perform the operations bit by bit
for i in range(len(query_operations)):
    if query_operations[i] == 'AND':
        binary_list[0] = [x and y for x, y in zip(binary_list[0], binary_list[1])]
        del binary_list[1]
    elif query_operations[i] == 'OR':
        binary_list[0] = [x or y for x, y in zip(binary_list[0], binary_list[1])]
        del binary_list[1]
    elif query_operations[i] == 'NOT':
        binary_list[0] = [1 - x for x in binary_list[0]]

print (binary_list[0])

