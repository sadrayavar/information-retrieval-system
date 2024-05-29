from dependencies.common_funcs import remove_symbol, two_chars, my_tokenizer


class WildcardResolver:

    def __init__(self, query, wildcard_index, log):
        self.queries = []
        self.wildcard_index = wildcard_index
        self.log = log
        self.recursive_resolver(my_tokenizer(query))

    def recursive_resolver(self, tkn_list):
        is_wild = False
        for i in range(len(tkn_list)):
            tkn = tkn_list[i]
            if "*" in tkn:
                is_wild = True

                # matching wildcard with its terms
                terms = match_wildcard(tkn, self.wildcard_index)
                self.log(f'"{tkn}" matched with => {terms}\n\n')

                # creating new queries with each matched term
                new_queries = make_queries(tkn_list, tkn_pos=i, terms=terms)

                # check generated queries for wildcard
                for query in new_queries:
                    self.recursive_resolver(my_tokenizer(query))

        if not is_wild:
            self.queries.append(" ".join(tkn_list))


"""it takes a term list, query, and a position which terms should be placesd and returns new query
"""


def make_queries(query, tkn_pos, terms):
    # creating new query
    new_queries = []
    for term in terms:
        before = " ".join(query[:tkn_pos])
        after = " ".join(query[tkn_pos + 1 :])
        new_query = f"{before} {term} {after}".strip()
        new_queries.append(new_query)

    # resolve the query with new token
    return new_queries


"""it takes a wildcard token and returns a list of terms which matchs with that token
"""


def match_wildcard(tkn, wildcard_index):
    # divinding token into two part, before the star and after the star
    tkn = divide_star(tkn)

    # remove symbols
    tkn["before"] = "".join(remove_symbol(tkn["before"]))
    tkn["after"] = "".join(remove_symbol(tkn["after"]))

    # creating two_chars list
    before_list = two_chars("$" + tkn["before"])
    after_list = two_chars(tkn["after"] + "$")

    # find the common terms
    return common_terms(set(before_list + after_list), wildcard_index)


def divide_star(tkn):
    for i in range(len(tkn)):
        if tkn[i] == "*":
            first_part = tkn[:i]
            second_part = tkn[i + 1 :]
            return {"before": first_part, "after": second_part}


def common_terms(two_chars, index):
    results = []

    for two_char in two_chars:
        if two_char in index:
            tkns = index[two_char]
            results = list(set(results) & set(tkns)) if (len(results) != 0) else list(tkns)
            results.sort()
        else:
            return []

    return results
