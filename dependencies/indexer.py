import os, json


def indexer(token_list, postings_direct, log):
    """_summary_

    Args:
        token_list (list): list fo dictionaries with token, doc_id, and tkn_id keys
        postings_direct (string): directory in which posting list should be saved
        log (function): logging function for this session

    Returns:
        dictionary: dictionary of term with their frequency and posting list path
    """
    log("Started to execute indexer")

    # delete all of posting list
    delete_files(postings_direct)

    dict = {}

    for tkn_info in token_list:
        
        token = tkn_info["token"]
        doc_id = str(tkn_info["doc_id"])
        tkn_id = tkn_info["tkn_id"]

        posting_path = f"{postings_direct}/{token}.json"

        # add token to dictionary (if does not exist)
        if token not in dict:
            # create posting list file
            create_posting_file(token, posting_path, log)

            # add path and frequency to dictionary
            dict[token] = {"path": posting_path, "freq": 0}

        # increase frequency of term in dictionary
        dict[token]["freq"] += 1

        # add doc_id and tkn_id to posting list
        posting = {}

        with open(posting_path, "r") as file:
            posting = json.load(file)

        with open(posting_path, "w") as file:
            # add token position to its document list
            token_ids = posting[doc_id] if (doc_id in posting) else []
            token_ids.append(tkn_id)
            posting[doc_id] = token_ids

            json.dump(posting, file, indent=4)

    return dict


def create_posting_file(term, path, log):
    if os.path.exists(path):
        log(f"Posting list file for '{term}' already exists in '{path}'")
        return

    try:
        with open(path, "w") as file:
            json.dump({}, file)
    except:
        log(f"Some error occured during creating posting file of {term} in '{path}'")


def delete_files(directory):
    for filename in os.listdir(directory):
        # Create the full path to the file
        filepath = os.path.join(directory, filename)
        os.remove(filepath)
