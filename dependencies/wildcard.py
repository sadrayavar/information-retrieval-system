import json
from dependencies.common_funcs import two_words


class KgramIndexer:
    dict = {}

    def __init__(self, dictionary, dict_path, log):
        self.log = log

        for tkn in dictionary:
            for two_word in two_words(f"${tkn}$"):

                # add two words to dictionary
                if two_word not in self.dict:
                    self.dict[two_word] = []

                # add token to respected two_words
                self.dict[two_word].append(tkn)

                # sort dictionary
                self.dict = dict(sorted(self.dict.items()))

        # create file
        with open(f"{dict_path}/wildcard.json", "w") as file:
            json.dump(self.dict, file, indent=4)
