import os, json
from dependencies.common_funcs import delete_files


class PositionalIndexer:
    """_summary_

    Args:
        token_list (list): list fo dictionaries with token, doc_id, and tkn_id keys
        postings_direct (string): directory in which posting list should be saved
        log (function): logging function for this session

    Returns:
        dictionary: dictionary of term with their frequency and posting list path
    """

    result = {}

    def __init__(self, tkn_list, post_dir, dict_path, log):
        self.log = log
        log("Started to execute PositionalIndexer")

        # delete all of posting list files
        delete_files(post_dir)

        for tkn_entity in tkn_list:
            token = tkn_entity["token"]
            doc_id = tkn_entity["doc_id"]
            tkn_pos = tkn_entity["tkn_pos"]
            post_file = f"{post_dir}/{token}.json"

            self.add_token(token, post_file)

            self.add_posting(str(doc_id), tkn_pos, post_file)

        # create file
        with open(f"{dict_path}/positional.json", "w") as file:
            json.dump(self.result, file, indent=4)

    def add_token(self, token, post_file):
        # add token to dictionary (if does not exist)
        if token not in self.result:
            self.create_posting(token, post_file)

            # add path and frequency to dictionary
            self.result[token] = {"path": post_file, "freq": 0}

            # sort dictionary
            self.result = dict(sorted(self.result.items()))

        # increase frequency of term in dictionary
        self.result[token]["freq"] += 1

    def create_posting(self, token, post_path):
        if os.path.exists(post_path):
            self.log(f"Posting list file for '{token}' already exists in '{post_path}'")
            return

        with open(post_path, "w") as file:
            json.dump({}, file)

    def add_posting(self, doc_id, tkn_pos, post_file):
        posting = {}

        with open(post_file, "r") as file:
            posting = json.load(file)

        with open(post_file, "w") as file:
            # add token position to its document list
            token_ids = posting[doc_id] if (doc_id in posting) else []
            token_ids.append(tkn_pos)
            posting[doc_id] = token_ids

            json.dump(posting, file, indent=4)
