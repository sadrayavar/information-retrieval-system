import json


class KgramIndexer:
    dict = {}
    dic_path = "dictionary"

    def __init__(self, dictionary):

        for tkn in dictionary:
            for two_word in self.two_words(tkn):

                # add two words to dictionary
                if two_word not in self.dict:
                    self.dict[two_word] = []

                # add token to respected two_words
                self.dict[two_word].append(tkn)

                # sort dictionary
                self.dict = dict(sorted(self.dict.items()))

        # create file
        with open(f"{self.dic_path}/wildcard.json", "w") as file:
            json.dump(self.dict, file, indent=4)

    def two_words(self, tkn):
        tkn = f"${tkn}$"
        two_word_list = []

        for i in range(len(tkn) - 1):
            two_char = tkn[i] + tkn[i + 1]
            two_word_list.append(two_char)

        return two_word_list
