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
        #search_word = 'raven or owl'

        # call query1 method to print the result
        if len(search_word.split(' ')) == 1:
            self.query1(search_word)

        # call query2 method to print the result
        if 'or' in search_word:
            parsed_words = search_word.split(' ')
            word1 = parsed_words[0]
            word2 = parsed_words[-1]
            self.query2(word1, word2)

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
        # build a set to record all the stories that contain either word1 or word2, or both.
        valid_titles = set(dictionary[word1].keys()) | set(dictionary[word2].keys())
        # loop in the valid title set
        for title in valid_titles:
            print('    ' + title)
            # print searching result for word1
            print('      ' + word1)
            if title not in dictionary[word1].keys():
                print('        ' + '--')
            else:
                for line in dictionary[word1][title]:
                    out_line = self.lines_in_file[line - 1].strip()
                    out_result = re.sub(word1, '**' + word1.upper() + '**', out_line)
                    print('        ' + str(line) + ' ' + out_result)
            # print searching result for word2
            print('      ' + word2)
            if title not in dictionary[word2].keys():
                print('        ' + '--')
            else:
                for line in dictionary[word2][title]:
                    out_line = self.lines_in_file[line - 1].strip()
                    out_result = re.sub(word2, '**' + word2.upper() + '**', out_line)
                    print('        ' + str(line) + ' ' + out_result)

test = Search()
te_indext = test.get_dictionary()
test.search_word()
