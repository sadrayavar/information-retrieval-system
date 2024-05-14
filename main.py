from dependencies.log import Log
from dependencies.parser import doc_parser, query_parser
from dependencies.indexer import Indexer
from dependencies.wildcard import KgramIndexer


class Main:
    dict = {}
    wildcard_dict = {}
    paths = {
        "document": "documents",
        "posting": "posting list",
        # the path of the log files is created in the log.py
    }

    def __init__(self):
        # initializing logging system
        self.log = Log().log

        # pre-process documents
        tokens = doc_parser(self.paths["document"], self.log)

        # index documents
        indxr = Indexer(tokens, self.paths["posting"], self.log)
        self.dict = indxr.dict

        # wildcard indexer
        wildcard = KgramIndexer(self.dict)
        self.wildcard_dict = wildcard.dict

        # while True:
        #     (input("Please enter your query: "))
        #     query_parser()

        #     self.rank_results()

    def rank_results(self):
        self.log("Started to execute rank_results")


Main()
