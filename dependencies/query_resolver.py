from nltk.tokenize import word_tokenize
from common_funcs import lower, remove_symbol, stem

# from dependencies.common_funcs import lower, remove_symbol, stem


def my_tokenize(sentence):
    tkn_list = []
    tkn = ""
    for i in range(len(sentence)):
        last_char = i + 1 == len(sentence)
        if sentence[i] == " " or last_char:
            if tkn != "":
                apnd = tkn + sentence[i] if last_char else tkn
                tkn_list.append(apnd)
                tkn = ""
        else:
            tkn += sentence[i]
    return tkn_list


def convert_star(tkn):
    first_part = ""
    second_part = ""
    for i in range(len(tkn)):
        if tkn[i] == "*":
            first_part = "$" + tkn[:i]
            second_part = tkn[i + 1 :] + "$"
            break
    return (first_part, second_part)


def query_parser(query):
    result = []

    tkn_list = my_tokenize(query)
    for i in range(len(tkn_list)):
        tkn = tkn_list[i]

        tkn = word_tokenize(tkn)

        print(tkn)
        tkn = remove_symbol(tkn)
        print(tkn)
        tkn = lower(tkn)
        print(tkn)
        tkn = stem(tkn)
        print(tkn)
        tkn = [tkn["stemed"] for tkn in tkn]
        print(tkn)
        print()
        result += tkn

    return result


query_parser("game")
# query_parser("games,")
# query_parser(",games")
# query_parser("games have")
# query_parser("ga*")
# query_parser("*es")
# query_parser("ga*es")
# query_parser("ga*es have")
# query_parser("games \4 border")
# query_parser("games \4 bo*")
