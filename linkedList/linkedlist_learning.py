class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0


    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1


    def prepend(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.size += 1


    def remove_first(self):
        if self.head is None:
            return None

        data = self.head.data
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        self.size -= 1
        return data

    def remove_last(self):
        if self.head is None:
            return None

        current = self.head
        while current.next.next:
            current = current.next
        current.next = None
        self.talt = current
        self.size -= 1

    def show_data(self):
        if not self.size:
            print("the list is empty")
        current = self.head
        while current:
            print(current.data)
            current = current.next




