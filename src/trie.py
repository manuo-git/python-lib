# name: Trie
# prefix: trie
# ---
from typing import *
class Trie:
    class Node:
        def __init__(self, c: str):
            self._c = c
            self._common = 0
            self.children = {}
            self.accept = []

        def is_child(self, c: str) -> bool:
            return c in self.children  
              
        def add_child(self, c: str, i: int) -> None:
            assert c not in self.children
            self.children[c] = i

        def delete_child(self, c: str) -> None:
            assert c in self.children
            self.children.pop(c)

        def get_child_id(self, c: str) -> int:
            assert c in self.children
            return self.children[c]
        
        def add_common(self, a: int) -> None:
            self._common += a

        def get_common(self) -> int:
            return self._common   
             
        def add_accept(self, id) -> None:
            self.accept.append(id)

        def get_accpet_count(self) -> int:
            return len(self.accept)  
              
        def get_accpet_list(self) -> List[int]:
            return self.accept

    def __init__(self):
        self.root = Trie.Node("*")
        self.nodes: List["Trie.Node"] = [self.root]        

    def insert(self, st: str, st_id: int = 0):
        node = self.root
        for c in st:
            if not node.is_child(c):
                id = len(self.nodes)
                self.nodes.append(Trie.Node(c))
                node.add_child(c, id)
            node.add_common(1)
            c_id = node.get_child_id(c)
            node = self.nodes[c_id]
        node.add_common(1)
        node.add_accept(st_id)
    
    def is_prefix(self, prefix: str) -> int:
        node = self.root
        for c in prefix:
            if not node.is_child(c):
                return 0
            c_id = node.get_child_id(c)
            node = self.nodes[c_id]
        return node.get_common()

    def search(self, st: str) -> bool:
        node = self.root
        for c in st:
            if not node.is_child(c):
                return 0
            c_id = node.get_child_id(c)
            node = self.nodes[c_id]
        return node.get_accpet_count()
    
    def exist_pre_of_string(self, st: str) -> bool:
        node = self.root
        for c in st:
            if not node.is_child(c):
                return False
            c_id = node.get_child_id(c)
            node = self.nodes[c_id]
            if node.get_accpet_count() > 0:
                return True
        return False

    def count_pre(self, prefix: str) -> int:
        node = self.root
        for c in prefix:
            if not node.is_child(c):
                return 0
            c_id = node.get_child_id(c)
            node = self.nodes[c_id]
        return node.get_common()
    
    def count_pre_and_delete(self, prefix: str) -> int:
        node = self.root
        li = [0]
        for c in prefix:
            if not node.is_child(c):
                return 0
            c_id = node.get_child_id(c)
            node = self.nodes[c_id]
            li.append(c_id)
        parent = self.nodes[li[-2]]
        parent.delete_child(prefix[-1])

        num = node.get_common()
        for i in li:
            self.nodes[i].add_common(-num)
        return num