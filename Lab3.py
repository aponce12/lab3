##CS 2302 Data Structures
##Instructor:Diego Aguirre
##TA: Anindita Nath
##Project 3 Option A
##Modified and submitted by Andres Ponce 80518680
##Date of last modification 11/02/2018
##Purpose: Create an AVL or RB binary search tree with a given file.
##The file contains word embeddings. Functions include: compute the
##number of nodes in the tree, compute the height of the tree, create a file
##with the words on the tree, create a file given a desired depth.
##Find the similarity of two words given by a file. 

import os
import random
import time
import re
import math

##AVL TREE##
class Node:
    def __init__(self,key,embed):
        self.left=None
        self.right=None
        self.key=key
        self.embed=embed

    def __str__(self):
        return "%s" % self.key

class AVLTree():
    def __init__(self):
        self.node=None
        self.height=-1
        self.balance=0

    def insert(self,key,embed):
        n = Node(key,embed)

        if self.node == None:
            self.node = n
            self.node.left = AVLTree()
            self.node.right = AVLTree()

        elif self.node.left != None:
            self.node.left.insert(key,embed)

        elif self.node.right != None:
            self.node.right.insert(key,embed)
            
        self.rebalance()

    def rebalance(self):
        self.update_heights(recursive=False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                    self.update_heights()
                    self.update_balances()
                self.rotate_right()
                self.update_heights()
                self.update_balances()
            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                    self.update_heights()
                    self.update_balances()
                self.rotate_left()
                self.update_heights()
                self.update_balances()
    def update_heights(self, recursive=True):
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.update_heights()
                if self.node.right:
                    self.node.right.update_heights()
            self.height = 1+ max(self.node.left.height, self.node.right.height)
        else:
            self.height = -1

    def update_balances(self, recursive=True):
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.update_balances()
                if self.node.right:
                    self.node.right.update_balances()
            self.balance=self.node.left.height-self.node.right.height
        else:
            self.balance=0

    def rotate_right(self):
        """
        Right rotation
            set self as the right subtree of left subree
        """
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def rotate_left(self):
        """
        Left rotation
            set self as the left subtree of right subree
        """
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def delete(self, key):
            if self.node != None:
                if self.node.key == key:
                    # Key found in leaf node, just erase it
                    if not self.node.left.node and not self.node.right.node:
                        self.node = None
                    # Node has only one subtree (right), replace root with that one
                    elif not self.node.left.node:                
                        self.node = self.node.right.node
                    # Node has only one subtree (left), replace root with that one
                    elif not self.node.right.node:
                        self.node = self.node.left.node
                    else:
                        # Find  successor as smallest node in right subtree or
                        #       predecessor as largest node in left subtree
                        successor = self.node.right.node  
                        while successor and successor.left.node:
                            successor = successor.left.node

                        if successor:
                            self.node.key = successor.key

                            # Delete successor from the replaced node right subree
                            self.node.right.delete(successor.key)

                elif key < self.node.key:
                    self.node.left.delete(key)

                elif key > self.node.key:
                    self.node.right.delete(key)

                # Rebalance tree
                self.rebalance()
                
    def search(self, key):
        if self.node != None:
            #print(key,self.node.key)
            if self.node.key == key:
                print(self.node)
                return self.node
        else:
            return
        self.node.left.search(key)
        self.node.right.search(key)

    def inorder_traverse(self):
            """
            Inorder traversal of the tree
                Left subree + root + Right subtree
            """
            result = []

            if not self.node:
                return result
            
            result.extend(self.node.right.inorder_traverse())
            result.append(self.node.key)
            result.extend(self.node.left.inorder_traverse())

            return result
        

##RED-BLACK TREE##
# RBTNode class - represents a node in a red-black tree
class RBTNode:
    def __init__(self, key, embed, parent, is_red = False, left = None, right = None):
        self.key = key
        self.embed = embed
        self.left = left
        self.right = right
        self.parent = parent
        
        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    # Returns true if both child nodes are black. A child set to None is considered
    # to be black.
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count
    
    # Returns the grandparent of this node
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # Gets this node's predecessor from the left child subtree
    # Precondition: This node's left child is not None
    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    # Returns this node's sibling, or None if this node does not have a sibling
    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    # Returns the uncle of this node
    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    # Returns True if this node is black, False otherwise
    def is_black(self):
        return self.color == "black"

    # Returns True if this node is red, False otherwise
    def is_red(self):
        return self.color == "red"

    # Replaces one of this node's children with a new child
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    # Sets either the left or right child of this node
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False
            
        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True


class RedBlackTree:
    def __init__(self):
        self.root = None
    
    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()
    
    def _bst_remove(self, key):
        node = self.search(key)
        self._bst_remove_node(node)

    def _bst_remove_node(self, node):
        if node is None:
            return

        # Case 1: Internal node with 2 children
        if node.left is not None and node.right is not None:
            # Find successor
            successor_node = node.right
            while successor_node.left is not None:
                successor_node = successor_node.left

            # Copy successor's key
            successor_key = successor_node.key

            # Recursively remove successor
            self._bst_remove_node(successor_node)

            # Set node's key to copied successor key
            node.key = successor_key

        # Case 2: Root node (with 1 or 0 children)
        elif node is self.root:
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right
                    
            # Make sure the new root, if not None, has parent set to None
            if self.root is not None:
                self.root.parent = None
                    
        # Case 3: Internal with left child only
        elif node.left is not None:
            node.parent.replace_child(node, node.left)
                
        # Case 4: Internal with right child OR leaf
        else:
            node.parent.replace_child(node, node.right)

    # Returns the height of this tree
    def get_height(self):
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node):
        if node is None:
            return -1
        left_height = self._get_height_recursive(node.left)
        right_height = self._get_height_recursive(node.right)
        return 1 + max(left_height, right_height)
    
    def insert(self, key, embed):
        new_node = RBTNode(key, embed, None, True, None, None)
        self.insert_node(new_node)
        
    def insert_node(self, node):
        # Begin with normal BST insertion
        if self.root is None:
            # Special case for root
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right
        
        # Color the node red
        node.color = "red"
            
        # Balance
        self.insertion_balance(node)

    def insertion_balance(self, node):
        # If node is the tree's root, then color node black and return
        if node.parent is None:
            node.color = "black"
            return
        
        # If parent is black, then return without any alterations
        if node.parent.is_black():
            return
    
        # References to parent, grandparent, and uncle are needed for remaining operations
        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()
        
        # If parent and uncle are both red, then color parent and uncle black, color grandparent
        # red, recursively balance  grandparent, then return
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        # If node is parent's right child and parent is grandparent's left child, then rotate left
        # at parent, update node and parent to point to parent and grandparent, respectively
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        # Else if node is parent's left child and parent is grandparent's right child, then rotate
        # right at parent, update node and parent to point to parent and grandparent, respectively
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        # Color parent black and grandparent red
        parent.color = "black"
        grandparent.color = "red"
                
        # If node is parent's left child, then rotate right at grandparent, otherwise rotate left
        # at grandparent
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    # Performs an in-order traversal, calling the visitor function for each node in the tree
    def in_order(self, visitor_function):
        self.in_order_recursive(visitor_function, self.root)

    # Performs an in-order traversal
    def in_order_recursive(self, visitor_function, node):
        if node is None:
            return
        # Left subtree, then node, then right subtree
        self.in_order_recursive(visitor_function, node.left)
        visitor_function(node)
        self.in_order_recursive(visitor_function, node.right)

    def is_none_or_black(self, node):
        if node is None:
            return True
        return node.is_black()

    def is_not_none_and_red(self, node):
        if node is None:
            return False
        return node.is_red()

    def prepare_for_removal(self, node):
        if self.try_case1(node):
            return

        sibling = node.get_sibling()
        if self.try_case2(node, sibling):
            sibling = node.get_sibling()
        if self.try_case3(node, sibling):
            return
        if self.try_case4(node, sibling):
            return
        if self.try_case5(node, sibling):
            sibling = node.get_sibling()
        if self.try_case6(node, sibling):
            sibling = node.get_sibling()

        sibling.color = node.parent.color
        node.parent.color = "black"
        if node is node.parent.left:
            sibling.right.color = "black"
            self.rotate_left(node.parent)
        else:
            sibling.left.color = "black"
            self.rotate_right(node.parent)

    def remove(self, key):
        node = self.search(key)
        if node is not None:
            self.remove_node(node)
            return True
        return False

    def remove_node(self, node):
        if node.left is not None and node.right is not None:
            predecessor_node = node.get_predecessor()
            predecessor_key = predecessor_node.key
            self.remove_node(predecessor_node)
            node.key = predecessor_key
            return

        if node.is_black():
            self.prepare_for_removal(node)
        self._bst_remove(node.key)

        # One special case if the root was changed to red
        if self.root is not None and self.root.is_red():
            self.root.color = "black"

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else: # node is root
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else: # node is root
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)
            
    def search(self, key):
        current_node = self.root
        while current_node is not None:
            # Return the node if the key matches.
            if current_node.key == key:
                return current_node
                
            # Navigate to the left if the search key is
            # less than the node's key.
            elif key < current_node.key:
                current_node = current_node.left

            # Navigate to the right if the search key is
            # greater than the node's key.
            else:
                current_node = current_node.right

        # The key was not found in the tree.
        return None

    def try_case1(self, node):
        if node.is_red() or node.parent is None:
            return True
        return False # node case 1

    def try_case2(self, node, sibling):
        if sibling.is_red():
            node.parent.color = "red"
            sibling.color = "black"
            if node is node.parent.left:
                self.rotate_left(node.parent)
            else:
                self.rotate_right(node.parent)
            return True
        return False # not case 2

    def try_case3(self, node, sibling):
        if node.parent.is_black() and sibling.are_both_children_black():
            sibling.color = "red"
            self.prepare_for_removal(node.parent)
            return True
        return False # not case 3

    def try_case4(self, node, sibling):
        if node.parent.is_red() and sibling.are_both_children_black():
            node.parent.color = "black"
            sibling.color = "red"
            return True
        return False # not case 4

    def try_case5(self, node, sibling):
        if self.is_not_none_and_red(sibling.left) and self.is_none_or_black(sibling.right) and node is node.parent.left:
            sibling.color = "red"
            sibling.left.color = "black"
            self.rotate_right(sibling)
            return True
        return False # not case 5

    def try_case6(self, node, sibling):
        if self.is_none_or_black(sibling.left) and self.is_not_none_and_red(sibling.right) and node is node.parent.right:
            sibling.color = "red"
            sibling.right.color = "black"
            self.rotate_left(sibling)
            return True
        return False # not case 6
    
    def in_order(self):
        return self.in_order_recursive4(self.root)
        
    def in_order_recursive4(self,node,items=[]):
        if node is None:
            return
        # Left subtree, then node, then right subtree
        self.in_order_recursive4(node.left,items)
        items.append(node.key)
        self.in_order_recursive4(node.right,items)
        return items

##-------------------------------FUNCTIONS----------------------------------##

##Function countNodes count the nodes of the AVL tree recursively.
##It receives a tree and count each node recursively going left and right.
def countNodes(tree, count=0):
    root=tree.node
    if root is None:
        return count
    return countNodes(root.left, countNodes(root.right, count + 1))

##Function countRBNodes count the nodes of the RedBlack tree recursively.
##It receives a tree and count each node recursively going left and right.
def countRBNodes(tree, count=0):
    if tree is None:
        return count
    return countRBNodes(tree.left, countRBNodes(tree.right, count + 1))

##Function treeHeight return the biggest depth from right or left recursively. 
def treeHeight(tree):
    if tree.node is None:
        return 0
    else:
        rightDepth=treeHeight(tree.node.right)
        leftDepth=treeHeight(tree.node.left)

        if rightDepth>leftDepth:
            return rightDepth+1
        else:
            return leftDepth+1

##Function createFile creates a file with all the keys from the AVL tree.
##Uses tree.inorder_traverse function from AVL class
def createFile(tree):
    newFile=open("listofwords.txt","w+")
    words=tree.inorder_traverse()
    for item in words:
        newFile.write(item+"\n")
    newFile.close()

##Function createRBFile creates a file with all the keys from the RB tree.
##Uses tree.in_order function from RedBlackTree class
def createRBFile(tree):
    newFile=open("listofwords.txt","w+")
    words=tree.in_order()
    for item in words:
        newFile.write(item+"\n")
    newFile.close()

##Function createFile2 creates a file with all the nodes stored at a given depth
##Uses recursion to traverse the node right and left.
def createFile2(newFile,tree,d):
    if d > (treeHeight(tree)-1):
        return
    if tree is None:
        return
    if d == 0:
        if tree.node is None:
            return
        newFile.write(tree.node.key+"\n")
    else:
        createFile2(newFile,tree.node.right,d-1)
        createFile2(newFile,tree.node.left,d-1)

##Function createFile2RB creates a file with all the nodes stored at a given depth
##Uses recursion to traverse the node right and left.
def createFile2RB(newFile,tree,d):
    if tree is None:
        return
    if d == 0:
        if tree is None:
            return
        newFile.write(tree.key+"\n")
    else:
        createFile2RB(newFile,tree.right,d-1)
        createFile2RB(newFile,tree.left,d-1)

##Function search looks for a given key inside the tree.
##Uses recursion to traverse the tree.
def search(tree, key, tri):
    if tree.node != None:
        if tree.node.key == key:
            tri.append(tree.node)
    else:
        return
    search(tree.node.right, key,tri)
    search(tree.node.left, key,tri)
    return tri

def searchRB(tree, key, tri):
    if tree != None:
        if tree.key == key:
            tri.append(tree)
    else:
        return
    searchRB(tree.right, key,tri)
    searchRB(tree.left, key,tri)
    return tri

##Function calcEmbed calculates the similarity between two
##given words using the embedding and
##formula (e_0 (dot product) e_1) / |e_0| (magnitude of e_0) * |e_1| (magnitude of e_1)
def calcEmbed(file,tree):
    try:
        for line in file:
            data=line.split()
            tri=[]
            found1=search(tree, data[0], tri)    
            found2=search(tree, data[1], tri)
            e0=found1[0].embed
            e1=found2[1].embed
            top=0
            mag1=0
            mag2=0
            for i in range (len(e0)):
                top=top+(float(e0[i])*float(e1[i]))
            for i in range (len(e0)):
                mag1=mag1+(float(e0[i])*float(e0[i]))
                mag2=mag2+(float(e1[i])*float(e1[i]))
            mag1=math.sqrt(mag1)
            mag2=math.sqrt(mag2)
            down=mag1*mag2
            sim=top/down
            print(data[0],data[1],sim)
    except Exception as e:
        print ("Type error: " + str(e))
        print(traceback.format_exc()) 

def calcEmbedRB(file,tree):
    try:
        for line in file:
            data=line.split()
            tri=[]
            found1=searchRB(tree, data[0], tri)
            found2=searchRB(tree, data[1], tri)
            e0=found1[0].embed
            e1=found2[1].embed
            top=0
            mag1=0
            mag2=0
            for i in range (len(e0)):
                top=top+(float(e0[i])*float(e1[i]))
            for i in range (len(e0)):
                mag1=mag1+(float(e0[i])*float(e0[i]))
                mag2=mag2+(float(e1[i])*float(e1[i]))
            mag1=math.sqrt(mag1)
            mag2=math.sqrt(mag2)
            down=mag1*mag2
            sim=top/down
            print(data[0],data[1],sim)
    except Exception as e:
        print ("Type error: " + str(e))
        print(traceback.format_exc()) 
        
        
        

##Function createTree creates the tree with the given file with
##words embedding. Prints the tree, number of nodes, and height.
##creates the file with all the items in the tree, and returns tree
def createTree(file):
    try:
        tree=AVLTree()
        for line in file:
            data = line.split()
            word=data[0]
            if re.match("^[a-zA-Z]*$", word):
                embed=[]
                for i in range (1,len(data)):
                    embed.append(data[i])
                tree.insert(word,embed)
        print (tree.inorder_traverse())
        print ("The number of nodes in the tree are: ",countNodes(tree))
        print ("The height of the tree is: ",treeHeight(tree),"\n")
        createFile(tree)
        embedFile=open("testembed.txt")
        print("Similarities: ")
        calcEmbed(embedFile,tree)
        return tree
    except Exception as e:
        print ("Type error: " + str(e))
        print(traceback.format_exc()) 

##Function createRBTree creates the RB tree with the given file with
##words embedding. Prints the tree, number of nodes, and height.
##creates the file with all the items in the tree, and returns tree
def createRBTree(file):
    try:
        tree=RedBlackTree()
        for line in file:
            data = line.split()
            word=data[0]
            if re.match("^[a-zA-Z]*$", word):
                embed=[]
                for i in range (1,len(data)):
                    embed.append(data[i])
                tree.insert(word,embed)
        print(tree.in_order())
        print("The number of nodes in the tree are: ",countRBNodes(tree.root))
        print("The height of the tree is: ",tree.get_height(),"\n")
        createRBFile(tree)
        embedFile=open("testembed.txt")
        print("Similarities: ")
        calcEmbedRB(embedFile,tree.root)
        return tree
    except Exception as e:
        print ("Type error: " + str(e))
        print(traceback.format_exc()) 

##Function menu is called from the main. Ask the user for a desired tree option.
##Creates the desired tree usin either createTree or createRBTree.
##Ask for the desired depth to create file with nodes at that height.
##Creates the file and calls either createFile2 or createFile2RB.
def menu(file):
    try:
        asw=input("Choose an option to create the BST, AVL(A) or RBT(B)\n")
        if asw is "A":
            tree=createTree(file)
            print("")
            asw=input("Enter height desired: ")
            newFile=open("listatd.txt","w+")
            createFile2(newFile,tree,int(asw))
        if asw is "B":
            tree=createRBTree(file)
            print("")
            asw=input("Enter height desired: ")
            newFile=open("listatd.txt","w+")
            createFile2RB(newFile,tree.root,int(asw))
    except Exception as e:
        print ("Type error: " + str(e))
        print(traceback.format_exc()) 

def main():
    try:
        path=input("Enter path: ")
        path=path[2:]
        start_path = (r""+path+"")
        file=open(start_path,"r")
        menu(file)
    except Exception as e:
        print ("Type error: " + str(e))
        print(traceback.format_exc())
    
main ()
