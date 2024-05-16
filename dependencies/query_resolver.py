import json
from nltk.tokenize import word_tokenize
from dependencies.find_recursive import FindRecursive

# from common_funcs import lower, remove_symbol, stem
from dependencies.common_funcs import lower, remove_symbol, stem


class QueryResolver:
    results = {}

    def __init__(self, query, positional):
        self.positional = positional
        self.query_parser(query)

    def query_parser(self, query):
        result = []
        tkn_list = self.my_tokenize(query)

        for i in range(len(tkn_list)):
            tkn = tkn_list[i]

            # ignores "AND" since its default operator is AND
            if "AND" in tkn:
                continue

            if "OR" in tkn:
                pass

            tkn = word_tokenize(tkn)
            tkn = remove_symbol(tkn)
            tkn = lower(tkn)
            tkn = [tkn["stemed"] for tkn in stem(tkn)]
            result += tkn

        return self.get_results(result)

    def get_results(self, tkns):
        content = {}

        # load posting list contents
        for tkn in tkns:
            with open(self.positional[tkn]["path"], "r") as file:
                content[tkn] = json.load(file)

        for doc_id in range(5):
            list_of_lists = []
            for tkn in tkns:
                if str(doc_id) in content[tkn]:
                    list = content[tkn][str(doc_id)]
                    list_of_lists.append(list)
                else:
                    list_of_lists = []
                    break

            if len(list_of_lists) > 0:
                self.results[doc_id] = FindRecursive(list_of_lists).results

    def my_tokenize(self, sentence):
        tkn_list = []
        tkn = ""
        for i in range(len(sentence) + 1):
            word_finished = i == len(sentence)
            if word_finished or sentence[i] == " ":
                if tkn != "":
                    tkn_list.append(tkn)
                    tkn = ""
            else:
                tkn += sentence[i]
        return tkn_list

    def convert_star(self, tkn):
        first_part = ""
        second_part = ""
        for i in range(len(tkn)):
            if tkn[i] == "*":
                first_part = "$" + tkn[:i]
                second_part = tkn[i + 1 :] + "$"
                break
        return (first_part, second_part)

    def commons(self, first, second):
        if len(first) == 0:
            return second
        elif len(second) == 0:
            return first
        return list(set(first) & set(second))
