class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


def find_node(head, position):
    first_p, next_p = head, head

    count = 0

    while next_p is not None:
        next_p = next_p.next

        if count > position:
            first_p = first_p.next

        count += 1

    return first_p


def create_link():
    head = Node(0)
    p = head

    for i in range(1, 20):
        new_node = Node(i)
        p.next = new_node
        p = new_node

    return head


def main():
    head = create_link()

    p = find_node(head, 14)

    l = [i for i in range(20)]
    print(l[-14])

    print(p.value, '99999k')


if __name__ == '__main__':
    main()
