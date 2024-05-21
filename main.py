from dependencies.log import Log

# positional and wildcarddependencies
from dependencies.indexer.document_parser import doc_parser
from dependencies.indexer.positional import PositionalIndexer
from dependencies.indexer.wildcard import KgramIndexer
from dependencies.query.query_resolver import QueryResolver

# ranked dependencies
from dependencies.scoring.scoring import get_vectors
from dependencies.scoring.resolver import RankedResolver


class Main:
    positional = {}
    wildcard = {}
    vectors = {}
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

        # tf-idf scoring
        self.vectors = get_vectors(self.positional, self.paths["dict"])

        while True:
            print("\n#####################################")
            query = input("Please enter your query: ").strip()
            QueryResolver(query, self.positional, self.wildcard, self.log)
            RankedResolver(query, self.positional, self.vectors, self.log)


Main()
