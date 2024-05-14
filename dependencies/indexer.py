import os, json


class Indexer:
    """_summary_

    Args:
        token_list (list): list fo dictionaries with token, doc_id, and tkn_id keys
        postings_direct (string): directory in which posting list should be saved
        log (function): logging function for this session

    Returns:
        dictionary: dictionary of term with their frequency and posting list path
    """

    def __init__(self, tkn_list, post_dir, log):
        self.log = log
        self.dict = {}
        log("Started to execute indexer")

        # delete all of posting list files
        self.delete_files(post_dir)

        for tkn_entity in tkn_list:
            token = tkn_entity["token"]
            doc_id = tkn_entity["doc_id"]
            tkn_pos = tkn_entity["tkn_pos"]
            post_file = f"{post_dir}/{token}.json"

            self.process_token(token, post_file)

            self.process_posting(str(doc_id), tkn_pos, post_file)

    def delete_files(self, directory):
        for filename in os.listdir(directory):
            # Create the full path to the file
            filepath = os.path.join(directory, filename)
            os.remove(filepath)

    def process_token(self, token, post_file):
        # add token to dictionary (if does not exist)
        if token not in self.dict:
            self.create_posting(token, post_file)

            # add path and frequency to dictionary
            self.dict[token] = {"path": post_file, "freq": 0}

            # sort dictionary
            self.dict = dict(sorted(self.dict.items()))

        # increase frequency of term in dictionary
        self.dict[token]["freq"] += 1

    def create_posting(self, token, post_path):
        if os.path.exists(post_path):
            self.log(f"Posting list file for '{token}' already exists in '{post_path}'")
            return

        with open(post_path, "w") as file:
            json.dump({}, file)

    def process_posting(self, doc_id, tkn_pos, post_file):
        posting = {}

        with open(post_file, "r") as file:
            posting = json.load(file)

        with open(post_file, "w") as file:
            # add token position to its document list
            token_ids = posting[doc_id] if (doc_id in posting) else []
            token_ids.append(tkn_pos)
            posting[doc_id] = token_ids

            json.dump(posting, file, indent=4)
