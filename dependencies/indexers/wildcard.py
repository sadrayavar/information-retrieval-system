import json
from dependencies.common_funcs import two_chars


class KgramIndexer:
    result = {}

    def __init__(self, tkns_entity, dict_path, log):
        self.log = log

        for tkn_entity in tkns_entity:
            base = tkn_entity["base"]

            for two_char in two_chars(f"${base}$"):

                # initialize respected two_char key with empty array
                if two_char not in self.result:
                    self.result[two_char] = []

                if base not in self.result[two_char]:

                    # add token to respected two_chars
                    self.result[two_char].append(base)
                    self.result[two_char].sort()

                    # sort dictionary
                    self.result = dict(sorted(self.result.items()))

        # create file
        with open(f"{dict_path}/wildcard.json", "w") as file:
            json.dump(self.result, file, indent=4)
