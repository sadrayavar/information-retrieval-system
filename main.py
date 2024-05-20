from dependencies.log import Log
from dependencies.indexer.document_parser import doc_parser
from dependencies.query.query_resolver import QueryResolver
from dependencies.indexer.positional import PositionalIndexer
from dependencies.indexer.wildcard import KgramIndexer


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
        tkns_entity = doc_parser(self.paths["document"], self.log)

        # index documents
        self.positional = PositionalIndexer(
            tkns_entity, self.paths["posting"], self.paths["dict"], self.log
        ).result

        # wildcard indexer
        self.wildcard = KgramIndexer(tkns_entity, self.paths["dict"], self.log).result

        while True:
            print("\n#####################################")
            query = input("Please enter your query: ").strip()
            QueryResolver(query, self.positional, self.wildcard, self.log)


Main()
