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
        list: list fo dictionaries with token, doc_id, and tkn_pos keys
    """
    log("Started to execute pre_process")

    token_list = []

    for doc_id in range(5):
        with open(f"{path}/{doc_id}.text", "r") as file:
            # read file and pass it to the query_pre_proessor
            temp_list = pre_process_query(file.read(), log)

            # creating token entity with token, doc_id, and tkn_pos keys
            for tkn_pos in range(len(temp_list)):
                temp_list[tkn_pos] = {
                    "token": temp_list[tkn_pos],
                    "doc_id": doc_id,
                    "tkn_pos": tkn_pos,
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
