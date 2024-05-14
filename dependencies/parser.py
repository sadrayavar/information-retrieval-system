import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download("punkt")


def doc_parser(path, log=False):
    if log:
        log("Started to execute doc_parser")

    token_list = []

    for doc_id in range(5):
        with open(f"{path}/{doc_id}.text", "r") as file:
            # read file and pass it to the query_pre_proessor
            temp_list = file.read()
            temp_list = word_tokenize(temp_list)
            temp_list = remove_symbol(temp_list)
            temp_list = stem(temp_list)

            # creating token entity with token, doc_id, and tkn_pos keys
            for tkn_pos in range(len(temp_list)):
                temp_list[tkn_pos] = {
                    "token": temp_list[tkn_pos],
                    "doc_id": doc_id,
                    "tkn_pos": tkn_pos,
                }
            token_list += temp_list
    return token_list


def remove_symbol(tkn_list):
    return [token for token in tkn_list if token.isalnum()]


def stem(tkn_list):
    stm = PorterStemmer()
    return [stm.stem(tkn) for tkn in tkn_list]


def my_tokenize(sentence):
    tkn_list = []
    tkn = ""
    for i in range(len(sentence)):
        if sentence[i] == " " or i + 1 == len(sentence):
            if tkn != "":
                tkn_list.append(tkn)
                tkn = ""
        else:
            tkn += sentence[i]
    return tkn_list


def convert_star(self, string):
    for i in range(len(string)):
        if string[i] == "*":
            string = string[:i] + "_STAR_" + string[i + 1 :]
    return string


def query_parser(query):
    tkn_list = my_tokenize(query)
    pass
