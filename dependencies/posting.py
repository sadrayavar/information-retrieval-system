import os


class Node:
    value = None
    next = None

    def __init__(self, value, next=None):
        self.value = value
        self.next = None


class Posting:
    list = None

    def insert(self, doc_id):
        new_node = Node(doc_id)

        # executes when the posting list empty posting list
        if self.list == None:
            self.list = new_node
            return

        # given value is lesser or equel than the first node's value
        if new_node.doc_id <= self.list.doc_id:
            new_node.next = self.list
            self.list = new_node
            return

        # given value is grater than the first node's value
        current = self.list
        # iterate in posting list until reach the destination
        while True:
            if (current.next == None) or (current.next.doc_id > doc_id):
                break
            current = current.next

        # insert node between border nodes
        new_node.next = current.next
        current.next = new_node

        return list


def create_posting_list(term, path):
    if os.path.exists(path):
        return

    with open(path, "w") as f:
        pass
