class FindRecursive:

    def __init__(self, list_of_lists):
        self.results = []
        if len(list_of_lists) == 1:
            self.results = list_of_lists[0]
            return

        for num in list_of_lists[0]:
            result = self.find_in(list_of_lists[1:], num)
            if result != None:
                self.results.append(f"{num}->{result[:-2]}")

    def find_in(self, list_of_lists, prev=None):
        if len(list_of_lists) == 0:
            return ""

        for num in list_of_lists[0]:
            if num == prev + 1:
                next_part = self.find_in(list_of_lists[1:], prev=num)
                if next_part == None:
                    break
                else:
                    return str(num) + "->" + next_part

        return None
