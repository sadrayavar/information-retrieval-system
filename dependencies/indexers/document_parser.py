import nltk
from nltk.tokenize import word_tokenize
from dependencies.common_funcs import lower, remove_symbol, stem

# nltk.download("punkt")


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
            temp_list = lower(temp_list)
            temp_list = stem(temp_list)

            # creating token entity with token, doc_id, and tkn_pos keys
            for i in range(len(temp_list)):
                temp_list[i] = {
                    "token": temp_list[i]["stemed"],
                    "doc_id": doc_id,
                    "tkn_pos": i,
                    "base_token": temp_list[i]["base"],
                }
            token_list += temp_list
    return token_list
