import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download("punkt")


def pre_process_docs(path, log):
    """_summary_

    Args:
        path (string): the directory in which text files exist
        log (function): logging function for this session

    Returns:
        list: list fo dictionaries with token, doc_id, and tkn_id keys
    """
    log("Started to execute pre_process")

    token_list = []

    for doc_id in range(5):
        with open(f"{path}/{doc_id}.text", "r") as file:
            # read file and pass it to the query pre_proessor
            temp_list = pre_process_query(file.read(), log)

            # append document id for saving on posting list
            for tkn_id in range(len(temp_list)):
                temp_list[tkn_id] = {
                    "token": temp_list[tkn_id],
                    "doc_id": doc_id,
                    "tkn_id": tkn_id,
                }

            token_list += temp_list

    return token_list


def pre_process_query(query, log):
    stemmer = PorterStemmer()

    # lower case
    query = query.lower()

    # tokenizing
    query = word_tokenize(query)

    # removing symbols
    query = [token for token in query if token.isalnum()]

    # stemming
    query = [stemmer.stem(token) for token in query]

    return query
