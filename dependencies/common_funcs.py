import os, math, json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def delete_files(directory):
    for filename in os.listdir(directory):
        # Create the full path to the file
        filepath = os.path.join(directory, filename)
        os.remove(filepath)


def get_content(pos_index, base_tkn, log):
    try:
        if not isinstance(base_tkn, dict):
            # pre-process
            stem = pre_process(base_tkn)[0]

            tkn_path = pos_index[stem]["path"]
            with open(tkn_path, "r") as file:
                return json.load(file)
        else:
            return base_tkn
    except:
        log(f'There are no instance of "{stem}" in positional dictionary', "ERROR")
        return {}


def my_tokenizer(query):
    tkn_list = []
    tkn = ""
    for i in range(len(query) + 1):
        word_finished = i == len(query)
        if word_finished or query[i] == " ":
            if tkn != "":
                tkn_list.append(tkn)
                tkn = ""
        else:
            tkn += query[i]
    return tkn_list


# methods used in wildcard indexing


def two_chars(tkn):
    two_char_list = []

    for i in range(len(tkn) - 1):
        two_char = tkn[i] + tkn[i + 1]
        two_char_list.append(two_char)

    return two_char_list


# methods used in text (document or query) pre-processing


def pre_process(query, return_base=False):
    tkn_list = word_tokenize(query)
    tkn_list = remove_symbol(tkn_list)
    tkn_list = lower(tkn_list)
    tkn_list = stem(tkn_list, return_base)

    return tkn_list


def lower(tkn_list):
    return [tkn.lower() for tkn in tkn_list]


def remove_symbol(tkn_list):
    return [token for token in tkn_list if token.isalnum()]


def stem(tkn_list, return_base):
    stm = PorterStemmer()
    results = []
    for tkn in tkn_list:
        if return_base:
            results.append({"stem": stm.stem(tkn), "base": tkn})
        else:
            results.append(stm.stem(tkn))
    return results


# methods used in scoring


def extract_posting(path):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except:
        print("No posting files with this path:", path)


def tf_idf(tf, df, n):
    if tf == 0:
        return 0.0

    tfw = 1 + math.log(tf, 10)
    idf = math.log(n / df, 10)

    return tfw * idf
