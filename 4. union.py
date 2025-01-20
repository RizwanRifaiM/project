# Kode 1

# def union(a, b):
#     hasil = set()
#     singgung = set()
#     for i in range(len(a)):
#         hasil.add(a[i])
        
#         for j in range(len(b)):
#             if a[i] == b[j]:
#                 singgung.add(a[i])
#             else:
#                 hasil.add(b[j])
                
                
#     return f'global: {hasil} \nSinggung {singgung}'
                
# a = [10, 4, 20, 3, 6]
# b = [4, 2, 20, 8, 50, 99, 909]

# print(union(a, b))

class Node:
    def __init__(self, x):
        self.data = x
        self.next = None
    
def print_list(head):
    curr = head
    
    while curr:
        print(curr.data, end =' ')
        curr = curr.next
    print()
    
def intersection(head1, head2):
    seen = set()
    result = None
    
    p = head1
    while p:
        seen.add(p.data)
        p = p.next
    
    p = head2
    while p:
        if p.data in  seen:
            new_node = Node(p.data)
            new_node.next = result
            result = new_node
        p = p.next
            
    return result

def union(head1, head2):
    union_set = set()
    p = head1
    while p:
        union_set.add(p.data)
        p = p.next
        
    p = head2
    while p:
        union_set.add(p.data)
        p = p.next
        
    result = None
    tail = None
    
    for i in union_set:
        new_node = Node(i)
        if result is None:
            result = new_node
            tail = new_node
        else:
            tail.next = new_node
            tail = tail.next
            
    return result
    
def print_union(head1, head2):
    intersection_set = intersection(head1, head2)
    union_list = union(head1, head2)
    
    print('Singgung :')
    print_list(intersection_set)
    
    print('Seluruhnya :')
    print_list(union_list)
    
if __name__ == "__main__":
    values = [1, 2, 3, 3, 4, 5]
    head1 = Node(values[0])
    current = head1

    for value in values[1:]:
        current.next = Node(value)
        current = current.next

    # List 2: 1 -> 5 -> 6
    values = [6, 3, 4, 2, 1, 89]
    head2 = Node(values[0])
    current = head2

    for value in values[1:]:
        current.next = Node(value)
        current = current.next
    
    print_union(head1, head2)