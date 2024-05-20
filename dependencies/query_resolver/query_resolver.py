import json
from nltk.tokenize import word_tokenize
from dependencies.find_recursive import FindRecursive
from dependencies.common_funcs import lower, remove_symbol, stem
from dependencies.query_resolver.handle_star.handle_star import resolve_wildcard


class QueryResolver:
    results = {}

    def __init__(self, query, positional_index, wildcard_index, log):
        self.positional_index = positional_index
        self.wildcard_index = wildcard_index
        self.log = log
        self.query_parser(query)

    def query_parser(self, query):
        self.log(f"Starting to resolve:\t{query}")

        result = []
        tkn_list = self.my_tokenize(query)

        for i in range(len(tkn_list)):
            tkn = tkn_list[i]

            if "*" in tkn:
                # getting equivalance of the wildcard query
                new_tkns = resolve_wildcard(tkn, self.wildcard_index)
                self.log(f'Tokens retrieved for "{tkn}" are:\t{", ".join(new_tkns)}')

                for new_tkn in new_tkns:

                    # creating new token
                    full_token = " ".join(tkn_list[:i])
                    full_token += " " + new_tkn + " "
                    full_token += " ".join(tkn_list[i + 1 :])
                    full_token = full_token.strip()

                    # resolve the query with new token
                    result += self.query_parser(full_token)
                    return

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
            with open(self.positional_index[tkn]["path"], "r") as file:
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
