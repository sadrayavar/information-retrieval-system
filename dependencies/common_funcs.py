import os
from nltk.stem import PorterStemmer


def delete_files(directory):
    for filename in os.listdir(directory):
        # Create the full path to the file
        filepath = os.path.join(directory, filename)
        os.remove(filepath)


def two_words(tkn):
    two_word_list = []

    for i in range(len(tkn) - 1):
        two_char = tkn[i] + tkn[i + 1]
        two_word_list.append(two_char)

    return two_word_list


def lower(tkn_list):
    return [tkn.lower() for tkn in tkn_list]


def remove_symbol(tkn_list):
    return [token for token in tkn_list if token.isalnum()]


def stem(tkn_list):
    stm = PorterStemmer()
    return [{"stemed": stm.stem(tkn), "base": tkn} for tkn in tkn_list]
