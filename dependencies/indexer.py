from dependencies.posting import Posting, create_posting_list


def indexer(token_list, postings_path, log):
    log("Started to execute indexer")
    dict = {}

    for tkn in token_list:
        # add token to dictionary (if does not exist)
        if tkn not in dict:
            path = f"{postings_path}/{tkn[0]}.json"
            create_posting_list(tkn, path)
            dict[tkn[0]] = path

    return dict
