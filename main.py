# genearal dependencies
import os
from dependencies.log import Log
from dependencies.document_parser import doc_parser

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
        positional = PositionalIndexer(
            tkns_entity, self.paths["posting"], self.paths["dict"], self.log
        ).result

        # wildcard indexer
        wildcard = KgramIndexer(tkns_entity, self.paths["dict"], self.log).result

        # tf-idf scoring
        vectors = get_vectors(positional, self.paths["dict"])

        while True:
            input_query = input('Please enter your query (or "clear" to clear terminal): ').strip()
            if input_query=='clear':
                os.system('clear')
                continue

            queries = WildcardResolver(input_query, wildcard, self.log).queries
            for query in queries:
                BoolResolver(query, positional, wildcard, self.log)
                RankedResolver(query, positional, vectors, self.log)

                # print a line
                terminal_width = os.get_terminal_size()[0]
                line = ''.join(['=' for i in range(terminal_width)])
                print(f"\n{line}\n")


Main()
