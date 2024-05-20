from dependencies.log import Log
from dependencies.indexers.document_parser import doc_parser
from dependencies.query_resolver.query_resolver import QueryResolver
from dependencies.indexers.positional import PositionalIndexer
from dependencies.indexers.wildcard import KgramIndexer


class Main:
    positional = {}
    wildcard = {}
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
        self.positional = PositionalIndexer(
            tokens, self.paths["posting"], self.paths["dict"], self.log
        ).result

        # # create wildcard matcher
        # matcher = Indexer(tokens, 1, self.log)
        # self.dict = indxr.dict

        # wildcard indexer
        self.wildcard = KgramIndexer(tokens, self.paths["dict"], self.log).result

        while True:
            query = input("Please enter your query: ")
            results = QueryResolver(
                query, self.positional, self.wildcard, self.log
            ).results
            print(results)


Main()
