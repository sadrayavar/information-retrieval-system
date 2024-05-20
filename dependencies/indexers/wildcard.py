import json
from dependencies.common_funcs import two_chars


class KgramIndexer:
    result = {}

    def __init__(self, tkns, dict_path, log):
        self.log = log

        for tkn in tkns:
            processed_tkn = tkn["base_token"]
            tkn = tkn["token"]

            for two_char in two_chars(f"${processed_tkn}$"):

                # initialize respected two_char key with empty array
                if two_char not in self.result:
                    self.result[two_char] = []

                if tkn not in self.result[two_char]:

                    # add token to respected two_chars
                    self.result[two_char].append(tkn)
                    self.result[two_char].sort()

                    # sort dictionary
                    self.result = dict(sorted(self.result.items()))

        # create file
        with open(f"{dict_path}/wildcard.json", "w") as file:
            json.dump(self.result, file, indent=4)
