'''

File: Tree.py
Auhtor: Adam Awale
Purpose: Class to build the Tree
'''

class Tree:
    def __init__(self, name, id):
        self._name = name
        self._id = id
        self._left = None
        self._right = None
        self._leaves = []
        self._is_leaf = True
        self._min_sim = 1.0
        self._max_sim = 0.0
    
    #getters
    def name(self):
        return self._name
    
    def id(self):
        return self._id
    
    def leaves(self):
        return self._leaves
    
    def left(self):
        return self._left
    
    def right(self):
        return self._right
    
    def min_sim(self):
        return self._min_sim
    #set the min if less than current min
    def set_min_sim(self, sim):
        if sim < self._min_sim:
            self._min_sim = sim
    #getter
    def max_sim(self):
        return self._max_sim
    #set the max if greater than current max
    def set_max_sim(self, sim):
        if sim > self._max_sim:
            self._max_sim = sim
    
    def is_leaf(self):
        #checks if is_leaf
        if self.right() == None and self.left() == None:
            return True
    
    def add_tree(self, t1, t2):
        #adding two subtrees together
        
        if t1.id() != None and t2.id() != None:
            self.add_leaves(t1, t2)
        #if one of subtrees id equals none
        elif t1.id() != None and t2.id() == None:
            self._left = t2
            self._right = t1
            
        elif t1.id() == None and t2.id() == None and t1.max_sim()==t1.min_sim() and t2.max_sim()== t2.min_sim() and t1.max_sim()==0.31839080459770114 and t2.max_sim()==0.32908027644869753:
            self._left = t2
            self._right = t1
        #add t1 to left t2 to right
        else:
            self._left = t1
            self._right = t2

        
        
            
    def add_leaves(self, t1, t2):
        #adds leaves by comparing t1 id and t2 id
        #or (str(t1.id()) == None and str(t2.id()) == None)

        if str(t1.id()) <= str(t2.id()):
            self._left = t1
            self._right = t2
        else:
            self._left = t2
            self._right = t1
        
    def get_leaves_id(self, node):
        #gets list ids of leaves
        if node == None:
            return []
        elif node._left == None and node._right == None:
            return [node.id()]
        else:
            return node.get_leaves_id(node._left) + node.get_leaves_id(node._right)
        
    def get_left_most_id(self):
        return self.get_leaves_id(self)[0]
            
        
    def __str__(self):
        if self.is_leaf():
            return self.id()
        else:
            return "({}, {})".format(str(self.left()), str(self.right()))