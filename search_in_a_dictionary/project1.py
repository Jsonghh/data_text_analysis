import re
from collections import defaultdict

# prepare the lines in file and skipwords; store data in two lists.
file = open("grimms.txt", "r")  
lines_in_file = [] 
for line in file:  
    lines_in_file.append(line)  
file.close()

file1 = open("stopwords.txt", "r")
skipwords = []
for line in file1:
	skipwords.append(line[:-1])
file1.close()



# Find the fair tales names in the content table, and use these names as keys to build a dictionary
titles = set()

content_start_index = 0
content_end_index = 0


for i in range(len(lines_in_file)):
	if 'CONTENTS' in lines_in_file[i]:
		content_start_index = i + 2
		
	if 'SNOW-WHITE AND ROSE-RED' in lines_in_file[i]:
		content_end_index = i
		break


for k in range(content_start_index, content_end_index + 1):
	story_name = lines_in_file[k].strip()
	match = re.search(r'[A-Z].*', story_name)
	if match:
		titles.add(match.group())

# index words afer line 124, the preliminary output a dictionary with relationship 
#  {match_word => [(title, line_in_file)]}
index = defaultdict(list)
title = ''

for i in range(124, 9212):
	if lines_in_file[i].strip() in titles:
		title = lines_in_file[i].strip()
		
		continue

	# if lines_in_file[i] is title:
	# 	title = lines_in_file[i]
	# 	inner_dict[title] = []
	#		continue
	
	
	line = lines_in_file[i].strip().lower()
	# remove puctuation
	line_sans_punc = re.sub(r'[^\w\s]', '', line)
	words = line_sans_punc.split(' ')
	for word in words:
			if word not in skipwords:
				index[word].append((title, i + 1))
				
# convert the tupple list{word => [(title, line)]} into a dictionary of dictionary
result = {}
for word in index:
	inner_dict = {}
	for _tuple in index[word]:
		if _tuple[0] in inner_dict:
			inner_dict[_tuple[0]].append(_tuple[1])
		else:
			inner_dict[_tuple[0]] = [_tuple[1]]
	result[word] = inner_dict

		
print(result['raven'])





