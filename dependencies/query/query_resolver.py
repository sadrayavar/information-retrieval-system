import json
from dependencies.common_funcs import pre_process
from dependencies.query.resolve_operator import merge_dicts
from dependencies.query.resolve_wildcard import match_wildcard, make_queries


class QueryResolver:
    operators = ["AND", "OR", "NOT", "\\"]

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

    def get_content(self, base_tkn):
        try:
            if not isinstance(base_tkn, dict):
                # pre-process
                stem = pre_process(base_tkn)[0]["stem"]

                tkn_path = self.positional_index[stem]["path"]
                with open(tkn_path, "r") as file:
                    return json.load(file)
            else:
                return base_tkn
        except:
            self.log(
                f'There are no instance of "{stem}" in positional dictionary', "ERROR"
            )
            return {}

    def clean_wild(self, query):
        has_wild = False

        for i in range(len(query)):
            tkn = query[i]

            if "*" in tkn:
                has_wild = True

                # matching wildcard with its terms
                terms = match_wildcard(tkn, self.wildcard_index)
                self.log(f"\nFound wildcard token:\t{tkn} -> {terms}")

                # creating new queries with each matched term
                new_queries = make_queries(query, tkn_pos=i, terms=terms)

                # resolve each new query
                for new_query in new_queries:
                    self.query_parser(new_query)

        return {"has_wild": has_wild}

    def extract_operator(self, query, tkn):
        if isinstance(tkn, str):
            tkn_is_oprtr = ("NOT" in tkn) or ("AND" in tkn) or ("\\" in tkn)
            if tkn_is_oprtr:
                oprtr = tkn
                query = query[1:]
                tkn = query[0]
            else:
                oprtr = "AND"
        else:
            self.log("This token is not a string", "ERROR")

        return oprtr, query, tkn

    ############################################################
    ### main method
    ############################################################
    def query_parser(self, query):
        log_query = query
        self.log(f"\n\nProcessing query:\t{log_query}")

        """
        Handle *
        """
        query = self.my_tokenize(query)

        # check if any wildcard tokens left on query
        result = self.clean_wild(query)

        # stop processing query if it has wildcard in it
        if result["has_wild"]:
            return

        """
        Handle OR
        """

        new_query = []
        jump_flag = False
        for i in range(len(query)):
            if jump_flag:
                jump_flag = False
                continue

            if query[i] != "OR":
                new_query.append(query[i])
            else:
                if not isinstance(new_query[-1], dict):
                    new_query.pop()
                left = query[i - 1]
                right = query[i + 1]

                # pre-process left and right operands and get the posting list content
                left = self.get_content(left)
                right = self.get_content(right)

                # resolve with or operator
                result = merge_dicts(left, "OR", right, 0)

                # push the result to new query
                new_query.append(result)

                # set the jump flag
                jump_flag = True

        query = query if len(query) == 0 else new_query

        """
        Handle AND, NOT, \\N
        """

        # pre-process first token and get the posting list content
        result = self.get_content(query[0])

        # process multi-term queries
        query = query[1:]
        offset = 1
        while len(query) > 0:
            tkn = query[0]

            # extract operator from query
            oprtr, query, tkn = self.extract_operator(query, tkn)

            # pre-process and get the documents that has the right operand in them
            oprnd = self.get_content(tkn)

            # calculating offset
            if oprtr[0] == "\\":
                offset += int(oprtr[1:]) - 2

            # calculating results
            result = merge_dicts(result, oprtr, oprnd, offset)

            # stop processing other tokens if there are no results for this tokens
            if len(result) == 0:
                self.log(f"No results found for {log_query}")
                return

            # increment
            query = query[1:]
            offset += 1

        # sort and show the results
        self.log(f"Results ->\t{dict(sorted(result.items()))}")
