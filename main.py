from log import Log

dictionary = {}


class Main:

    def __init__(self):
        # initializing logging system
        self.log = Log().log

        self.start_indexing()
        while True:
            self.take_query()
            self.rank_results()

    def start_indexing(self):
        self.log("start_indexing executed")

    def take_query(self):
        input()
        self.log("take_query executed")

    def rank_results(self):
        self.log("rank_results executed")


Main()
