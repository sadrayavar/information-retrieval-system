from dependencies.common_funcs import remove_symbol, two_chars


def resolve_wildcard(tkn, wildcard_index):
    # divinding token into two part, before the star and after the star
    tkn = divide_star(tkn)

    # remove symbols
    tkn["before"] = "".join(remove_symbol(tkn["before"]))
    tkn["after"] = "".join(remove_symbol(tkn["after"]))

    # creating two character list
    before_list = two_chars("$" + tkn["before"])
    after_list = two_chars(tkn["after"] + "$")

    # find the common terms
    results = common_finder(before_list + after_list, wildcard_index)

    return results


def divide_star(tkn):
    for i in range(len(tkn)):
        if tkn[i] == "*":
            first_part = tkn[:i]
            second_part = tkn[i + 1 :]
            return {"before": first_part, "after": second_part}


def common_finder(list, index):
    results = []

    for two_char in list:
        tkns = index[two_char]
        results = commons(results, tkns)
    # for i in range(len(list) - 1):
    #     first_tkns = index[list[i]]
    #     second_tkns = index[list[i + 1]]
    #     results = commons(first_tkns, second_tkns)

    return results


def commons(first, second):
    if len(first) == 0:
        return second
    elif len(second) == 0:
        return first
    return list(set(first) & set(second))
