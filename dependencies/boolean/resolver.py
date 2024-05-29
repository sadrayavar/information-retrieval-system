from dependencies.common_funcs import get_content, my_tokenizer
from dependencies.boolean.operations import merge_dicts


class BoolResolver:
    operators = ["AND", "OR", "NOT", "\\"]

    def __init__(self, query, positional_index, wildcard_index, log):
        self.positional_index = positional_index
        self.wildcard_index = wildcard_index
        self.log = log
        self.log_query = query
        self.query_parser(my_tokenizer(query))

    def extract_operator(self, query):
        tkn = query[0]

        if isinstance(tkn, str):
            tkn_is_oprtr = ("NOT" in tkn) or ("AND" in tkn) or ("\\" in tkn)
            if tkn_is_oprtr:
                oprtr = tkn
                query = query[1:]
                tkn = query[0]
            else:
                oprtr = "AND"

            return oprtr, query, tkn
        else:
            self.log("This token is not a string", "ERROR")
            return "AND", query, tkn

    ############################################################
    ### main method
    ############################################################
    def query_parser(self, query):
        self.log(f"Processing query:\t{self.log_query}")

        """
        resolve OR
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
                left = get_content(self.positional_index, left, self.log)
                right = get_content(self.positional_index, right, self.log)

                # resolve with or operator
                result = merge_dicts(left, "OR", right, 0)

                # push the result to new query
                new_query.append(result)

                # set the jump flag
                jump_flag = True

        query = query if len(query) == 0 else new_query

        """
        resolve AND, NOT, \\N
        """

        # pre-process first token and get the posting list content
        result = get_content(self.positional_index, query[0], self.log)

        # process multi-term queries
        query = query[1:]
        offset = 1
        while len(query) > 0:
            tkn = query[0]

            # extract operator from query
            oprtr, query, tkn = self.extract_operator(query)

            # pre-process and get the documents that has the right operand in them
            oprnd = get_content(self.positional_index, tkn, self.log)

            # calculating offset
            if oprtr[0] == "\\":
                offset += int(oprtr[1:]) - 2

            # calculating results
            result = merge_dicts(result, oprtr, oprnd, offset)

            # stop processing other tokens if there are no results for this tokens
            if len(result) == 0:
                self.log(f'No results found for => "{self.log_query}"')
                return

            # increment
            query = query[1:]
            offset += 1

        # sort and show the results
        print()
        self.log(f"Results ->\t{dict(sorted(result.items()))}")
        print()
