import json
from dependencies.common_funcs import pre_process
from dependencies.query_resolver.resolve_operator import merge_dicts
from dependencies.query_resolver.resolve_wildcard import match_wildcard, make_queries


class QueryResolver:
    operators = ["AND", "OR", "NOT", "\\"]
    search_wild = False

    def __init__(self, query, positional_index, wildcard_index, log):
        self.positional_index = positional_index
        self.wildcard_index = wildcard_index
        self.log = log
        self.query_parser(query)

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

    def fill_ops(self, index, tkn_list):
        # fill operator and second operand
        if tkn_list[index] in self.operators:
            operator = tkn_list[index]
            right_oprnd = tkn_list[index + 1]
        else:
            operator = "AND"
            right_oprnd = tkn_list[index]

        return operator, right_oprnd

    def posting_content(self, tkn):
        try:
            tkn_path = self.positional_index[tkn]["path"]
            with open(tkn_path, "r") as file:
                return json.load(file)
        except:
            return {}

    ############################################################
    ### main method
    ############################################################
    def query_parser(self, query):
        query = self.my_tokenize(query)

        # check if any wildcard tokens left on query
        has_wild = False
        for i in range(len(query)):
            tkn = query[i]

            if "*" in tkn:
                self.search_wild = True
                has_wild = True
                terms = match_wildcard(tkn, self.wildcard_index)
                self.log(f"\nFound wildcard token:\t{tkn} -> {terms}")
                new_queries = make_queries(query, tkn_pos=i, terms=terms)
                for new_query in new_queries:
                    self.query_parser(new_query)
        if has_wild:
            return

        """
        resolve clean query (without wildcard)
        """

        # pre-process first token
        first_tkn = pre_process(query[0])[0]["stem"]

        # get the documetns that has first token
        result = self.posting_content(first_tkn)

        i = 1
        while i < len(query):
            is_oprtr = query[i] in self.operators

            # extract right opearand and operator from query
            operator, right_oprnd = self.fill_ops(i, query)

            # pre-process right operand
            right_oprnd = pre_process(right_oprnd)[0]["stem"]

            # fix stepping if token is an operator
            if is_oprtr:
                i += 1

            # main section which calculates the result
            if operator == "\\":
                pass
            else:
                right_content = self.posting_content(right_oprnd)
                offset = (i - 1) if is_oprtr else i
                result = merge_dicts(result, operator, right_content, offset)

            # stop processing other tokens if there are no results for this tokens
            if len(result) == 0:
                if not self.search_wild:
                    self.log(f'No results for -> "{" ".join(query)}"')
                return

            # increment step
            i += 1

        self.log(f'Results of "{" ".join(query)}" ->\t{result}')
