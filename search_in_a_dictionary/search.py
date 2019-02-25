import re


class Search:
    # prepare the lines in file and self.skipwords; store lines in two lists.
    def __init__(self):
        file = open("grimms.txt", "r")
        self.lines_in_file = file.readlines()

        file1 = open("stopwords.txt", "r")
        self.skipwords = file1.readlines()

        file1.close()

    def get_dictionary(self):

        title = ''
        index = {}

        for i in range(124, 9212):

            # if find title, use the variable title to record
            match = re.search(r'[A-Z][A-Z\s\-,\[\]]+\n', self.lines_in_file[i])
            skip_title = re.search(r'[0-9]', self.lines_in_file[i])
            if match and not skip_title:
                title = match.group()[:-1]
                continue

            # if not a title, split lines and search each word,
            # put the word into dictionary as a key, put the title as the key in the inner dictionary
            # and append line index into the value list.
            line = self.lines_in_file[i].strip().lower()
            line_sans_punc = re.sub(r'[^\w\s]', '', line)
            words = line_sans_punc.split(' ')
            for word in words:
                # skip words in the self.skipwords list
                if word + '\n' not in self.skipwords:
                    index.setdefault(word, {}).setdefault(
                        title, []).append(i + 1)
        return index

    def search_word(self):
        search_word = input('Please enter your query: ').strip()

        # if search_word contains keyword morethan, call the morethan function
        if 'morethan' in search_word:
            self.morethan(search_word)
            return

        # if search_word contains keyword near, call the near function
        if 'near' in search_word:
            self.near(search_word)
            return
        # call query1 method to print the result
        if len(search_word.split(' ')) == 1:
            self.query1(search_word)

        # call query2 method to print the result from searching with key word 'or'
        elif search_word.split(' ')[1] == 'or':
            parsed_words = search_word.split(' ')
            word1 = parsed_words[0]
            word2 = parsed_words[-1]
            self.query2(word1, word2)

        # call query2 method to print the result from searching with key word 'and'
        elif search_word.split(' ')[1] == 'and':
            parsed_words = search_word.split(' ')
            query_input = parsed_words[0] + ' ' + parsed_words[-1]
            self.query3(query_input)

        else:
            self.query3(search_word)

    def query1(self, word):
        print('query = ' + word)
        # call the function to build the index dictionary
        dictionary = self.get_dictionary()
        # if the input word is no in the dictionary, print '--'
        if word not in dictionary.keys():
            print('    --')
            return
        for title in dictionary[word]:
            print('    ' + title)
            # loop within the lines that contain the input word
            for line in dictionary[word][title]:
                out_line = self.lines_in_file[line - 1].strip()
                out_result = re.sub(word, '**' + word.upper() + '**', out_line)
                print('      ' + str(line) + ' ' + out_result)

    def query2(self, word1, word2):
        print('query = ' + word1 + ' or ' + word2)
        dictionary = self.get_dictionary()
        if word1 not in dictionary.keys() and word2 not in dictionary.keys():
            print('    --')
            return
        # build a set to record all the stories that contain either word1 or word2, or both.
        elif word1 not in dictionary.keys():
            valid_titles = dictionary[word2].keys()
        elif word2 not in dictionary.keys():
            valid_titles = dictionary[word1].keys()
        else:
            valid_titles = set(dictionary[word1].keys()) | set(
                dictionary[word2].keys())
        # loop in the valid title set
        for title in valid_titles:
            print('    ' + title)
            # print searching result for word1
            print('      ' + word1)
            if word1 in dictionary:
                if title not in dictionary[word1].keys():
                    print('        ' + '--')
                else:
                    for line in dictionary[word1][title]:
                        out_line = self.lines_in_file[line - 1].strip()
                        out_result = re.sub(
                            word1, '**' + word1.upper() + '**', out_line)
                        print('        ' + str(line) + ' ' + out_result)
            else:
                print('        ' + '--')

            # print searching result for word2
            print('      ' + word2)
            if word2 in dictionary:
                if title not in dictionary[word2].keys():
                    print('        ' + '--')
                else:
                    for line in dictionary[word2][title]:
                        out_line = self.lines_in_file[line - 1].strip()
                        out_result = re.sub(
                            word2, '**' + word2.upper() + '**', out_line)
                        print('        ' + str(line) + ' ' + out_result)
            else:
                print('        ' + '--')

    def query3(self, search_input):
        words = search_input.split(' ')
        dictionary = self.get_dictionary()
        # use validate_titles to record stories that contain all input words
        validate_titles = set()
        print('query = ' + search_input)
        for word in words:
            titles = set()
            if word not in dictionary:
                print('    --')
                return
            for title in dictionary[word].keys():
                titles.add(title)
            if len(validate_titles) == 0:
                # when validate_titles is empty,
                # put into it all the element in the titles set collected from the first round of loop
                validate_titles = validate_titles | titles
            else:
                # only retain tories that shows for both the previous rounds in word loop and the current round
                validate_titles = validate_titles & titles

        if len(validate_titles) == 0 :
            print('    --')
            return 
            
        for title in validate_titles:
            # print results for validate stories, which contain all input words
            print('    ' + title)
            for word in words:
                print('      ' + word)
                for line in dictionary[word][title]:
                    out_line = self.lines_in_file[line - 1].strip()
                    out_result = re.sub(
                        word, '**' + word.upper() + '**', out_line)
                    print('        ' + str(line) + ' ' + out_result)

    def morethan(self, search_input):
        search_word = search_input.split(' ')[0]
        # parse input information, and decide to use the morethan_time method or
        # the morethan_word method
        if '0' <= search_input.split(' ')[-1] <= '9':
            times = int(search_input.split(' ')[-1])
            self.morethan_times(search_word, times)
        else:
            word1 = search_word = search_input.split(' ')[0]
            word2 = search_word = search_input.split(' ')[-1]
            self.morethan_word(word1, word2)

    def morethan_times(self, search_word, times):

        print('query = ' + search_word + ' morethan ' + str(times))
        # call the function to build the index dictionary
        dictionary = self.get_dictionary()
        # if the search_input search_input is no in the dictionary, print '--'
        if search_word not in dictionary.keys():
            print('    --')
            return
        for title in dictionary[search_word]:
            if len(dictionary[search_word][title]) <= times:
                continue
            print('    ' + title)
            # loop within the lines that contain the search_word search_word
            for line in dictionary[search_word][title]:
                out_line = self.lines_in_file[line - 1].strip()
                out_result = re.sub(search_word, '**' +
                                    search_word.upper() + '**', out_line)
                print('      ' + str(line) + ' ' + out_result)

    def morethan_word(self, word1, word2):
        print('query = ' + word1 + ' morethan ' + word2)
        dictionary = self.get_dictionary()
        # if word1 doesn't exist in the dictionary, print '--'
        if word1 not in dictionary.keys():
            print('    --')
            return
        # if word2 doesn't exist in the dictionary, call method query1()
        if word2 not in dictionary.keys():
            print(word2 + ' doesn\'t exist in the dictionary.')
            print('the original query equals to:')
            self.query1(word1)
            return

        for title in dictionary[word1]:
            # if line number of word1 less than that of word2, do not print the title
            if title in dictionary[word2] and len(dictionary[word1][title]) <= len(dictionary[word2][title]):
                continue

            # if under the story title, word2 never shows up or has less showing numbers of word1
            # print stories containing word1
            print('    ' + title)
            # loop within the lines that contain the search_word search_word
            for line in dictionary[word1][title]:
                out_line = self.lines_in_file[line - 1].strip()
                out_result = re.sub(
                    word1, '**' + word1.upper() + '**', out_line)
                print('      ' + str(line) + ' ' + out_result)

    def near(self, search_input):
        word1 = search_input.split(' ')[0]
        word2 = search_input.split(' ')[-1]

        print('query = ' + word1 + ' near ' + word2)
        dictionary = self.get_dictionary()
        # if word1 or word2 doesn't exist in the dictionary, print '--'
        if word1 not in dictionary.keys() or word2 not in dictionary.keys():
            print('    --')
            return
        # record lines for word2 to prepare for 'near' test 
        lines2 = set()
        for title in dictionary[word2]:
            for line in dictionary[word2][title]:
                lines2.add(line)
            
        for title in dictionary[word1]:
            line1 = dictionary[word1][title]
            for line in line1:
                # if line for word1 does not exist in the set lines2, and neither line - 1 nor line + 1 exists,
                # jump into the next round in the loop
                if line not in lines2 and line - 1 not in lines2 and line + 1 not in lines2:
                    continue
            
                print('    ' + title)
                # loop within the lines that contain the word1
                for line in dictionary[word1][title]:
                    # if line for word1 does not exist in the set lines2, and neither line - 1 nor line + 1 exists,
                    # jump into the next round in the loop
                    if line not in lines2 and line - 1 not in lines2 and line + 1 not in lines2:
                        continue

                    out_line = self.lines_in_file[line - 1].strip()
                    out_result = re.sub(word1, '**' + word1.upper() + '**', out_line)
                    print('      ' + str(line) + ' ' + out_result)


test = Search()
test.search_word()
