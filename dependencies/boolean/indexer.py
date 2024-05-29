import os, json
from dependencies.common_funcs import delete_files


class PositionalIndexer:
    """_summary_

    Args:
        tkns_entities (list): list of token entities: {base, stem, doc_id, tkn_pos}
        postings_direct (string): directory in which posting list should be saved
        log (function): logging function for this session

    Returns:
        dictionary: dictionary of term with their frequency and posting list path
    """

    result = {}

    def __init__(self, tkns_entities, post_dir, dict_path, log):
        self.log = log
        log("Started to execute PositionalIndexer")

        # delete all of posting list files
        delete_files(post_dir)

        for tkn_entity in tkns_entities:
            stem = tkn_entity["stem"]
            doc_id = tkn_entity["doc_id"]
            tkn_pos = tkn_entity["tkn_pos"]
            file_path = f"{post_dir}/{stem}.json"

            # create index
            self.create_index(stem, file_path)

            # create posting list
            self.create_posting(str(doc_id), tkn_pos, file_path)

        # create index file
        with open(f"{dict_path}/positional.json", "w") as file:
            json.dump(self.result, file, indent=4)

    def create_index(self, token, post_file):
        # add path and frequency
        if token not in self.result:
            self.result[token] = {"path": post_file, "freq": 0}

        # increase frequency of term in dictionary
        self.result[token]["freq"] += 1

        # sort dictionary
        self.result = dict(sorted(self.result.items()))

    def create_posting(self, doc_id, tkn_pos, post_path):
        # create posting file (if ir does not exist)
        if not os.path.exists(post_path):
            with open(post_path, "w") as file:
                json.dump({}, file)

        # read posting file
        with open(post_path, "r") as file:
            posting = json.load(file)

        # add token position to its document list
        with open(post_path, "w") as file:
            token_ids = posting[doc_id] if (doc_id in posting) else []
            token_ids.append(tkn_pos)
            posting[doc_id] = token_ids

            json.dump(posting, file, indent=4)
