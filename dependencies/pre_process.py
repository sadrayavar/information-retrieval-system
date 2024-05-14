import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download("punkt")


def pre_process_docs(path, log):
    log("Started to execute pre_process")

    token_list = []

    for doc_id in range(5):
        with open(f"{path}/{doc_id}.text", "r") as file:
            # read file and pass it to the query pre_proessor
            temp_list = pre_process_query(file.read(), log)

            # append document id for saving on posting list
            for token_id in range(len(temp_list)):
                temp_list[token_id] = (temp_list[token_id], doc_id, token_id)

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
