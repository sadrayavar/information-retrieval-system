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

    def fill_ops(self, first_tkn, second_tkn):
        if (
            first_tkn == "NOT"  # NOT tkn
            or first_tkn == "AND"  # AND tkn
            or (isinstance(first_tkn, str) and first_tkn[0] == "\\")  # \N tkn
        ):
            operator = first_tkn
            operand = second_tkn
            step = 2
        else:  # tkn tkn
            operator = "AND"
            operand = first_tkn
            step = 1

        return operator, operand, step

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

    ############################################################
    ### main method
    ############################################################
    def query_parser(self, query):
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

        i = 1
        while i < len(query):
            # extract right opearand and operator from query
            if len(query) > 2:
                operator, right_oprnd, step = self.fill_ops(query[i], query[i + 1])
            else:
                operator, right_oprnd, step = "AND", query[-1], 1

            # pre-process and get the documents that has the right side token in them
            right_content = self.get_content(right_oprnd)

            # calculating offset
            offset = i
            if operator[0] == "\\":
                offset += int(operator[1:]) - 2

            # calculating results
            result = merge_dicts(result, operator, right_content, offset)

            # stop processing other tokens if there are no results for this tokens
            if len(result) == 0:
                self.log(f"No results found")
                return

            # increment step
            i += step

        self.log(f"Results ->\t{result}")
