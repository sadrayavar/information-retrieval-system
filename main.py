from dependencies.log import Log
from dependencies.document_parser import doc_parser
from dependencies.query_resolver import query_parser
from dependencies.indexer import Indexer
from dependencies.wildcard import KgramIndexer


class Main:
    dict = {}
    wildcard_dict = {}
    paths = {
        "document": "Database/Documents",
        "log": "Database/Logs",
        "posting": "Database/Posting List",
        "dict": "Database/Dictionary",
        # the path of the log files is created in the log.py
    }

    def __init__(self):
        # initializing logging system
        self.log = Log(self.paths["log"]).log

        # pre-process documents
        tokens = doc_parser(self.paths["document"], self.log)

        # index documents
        indxr = Indexer(tokens, self.paths["posting"], self.paths["dict"], self.log)
        self.dict = indxr.dict

        # # create wildcard matcher
        # matcher = Indexer(tokens, 1, self.log)
        # self.dict = indxr.dict

        # wildcard indexer
        wildcard = KgramIndexer(self.dict, self.paths["dict"], self.log)
        self.wildcard_dict = wildcard.dict

        while True:
            query = input("Please enter your query: ")
            results = query_parser(query)
            print("results are: ", results)


Main()
