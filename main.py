from dependencies.log import Log
from dependencies.pre_process import pre_process_docs, pre_process_query
from dependencies.indexer import indexer


class Main:
    paths = {
        "document": "documents",
        "posting": "posting list",
        # the path of the log files is created in the log.py
    }

    def __init__(self):
        # initializing logging system
        self.log = Log().log

        tokens = pre_process_docs(self.paths["document"], self.log)
        self.dictionary = indexer(tokens, self.paths["posting"], self.log)
        print(self.dictionary)
        # while True:
        #     self.take_query()
        #     self.rank_results()

    def take_query(self):
        self.log("Started to execute take_query")
        input()

    def rank_results(self):
        self.log("Started to execute rank_results")


Main()
