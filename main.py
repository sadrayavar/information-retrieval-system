# genearal dependencies
from dependencies.log import Log
from dependencies.document_parser import doc_parser
from dependencies.common_funcs import pre_process

# wildcard dependencies
from dependencies.wildcard.indexer import KgramIndexer
from dependencies.wildcard.resolver import WildcardResolver

# positional dependencies
from dependencies.boolean.indexer import PositionalIndexer
from dependencies.boolean.resolver import BoolResolver

# ranked dependencies
from dependencies.scoring.indexer import get_vectors
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
            input_query = input("Please enter your query: ").strip()

            queries = WildcardResolver(input_query, self.wildcard, self.log).queries
            for query in queries:
                BoolResolver(query, self.positional, self.wildcard, self.log)
                RankedResolver(query, self.positional, self.vectors, self.log)


Main()
