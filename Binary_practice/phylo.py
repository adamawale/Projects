from genome import *
from tree import *
'''

File: phylo.py
Author: Adam Awale
Puprose: ReadInput, Make N-grams, Make similarity tree
'''
#from genome.genome import GenomeData
#from tree.tree import Tree
def ReadInputFile():
    '''Reads input lines, make a list of GENOMES
       calls ProcessNGrams
       precondition: filename is correct or error handling
       postcondition: fasta file properly parsed through
       returns -1 if error
    '''
    filename = input('FASTA file: ')
    try:
        org_list = []
        prev_line = ''
        inFile = open(filename)
        for line in inFile:
            if line[0] == '>':
                id = line[1:line.find(' ')]
                name = line[line.find(' ') + 1 :line.find(',')]
                seq = ''
                prev_line = ' '
                
            elif line == '\n' and prev_line != '\n':
                organism = GenomeData(name,id,seq)
                org_list.append(organism)
                prev_line = '\n'
                
            else:
                seq += line[:-1]
        
        #PrintOrganisms(org_list)
        if ProcessNGrams(org_list) == -1:
            return -1
            
    except IOError:
        print("ERROR: could not open file " + filename)
        return -1
    
    
def ProcessNGrams(list):
    '''Asks for N for ngrams, error handle N, compute similarity, initialize tree, construct tree
       Parameter: list, list of objects of class Genome
       Precondition: N is correct or error handled, list is a list of organisms(Genome)
       Returns: -1 if error
       Postcondtion: output correct, tree constructed properly
    '''
    try:
        N = input('n-gram size: ')
        N = int(N)
        for o in list:
            o.add_ngram(get_ngrams(o.sequence(), N))
            
        #PrintOrganisms(list)
        similarity_dict = ComputeSimilarity(list)
        tree_list = InitializeTree(list)
        tree_list = ConstructTree(similarity_dict, tree_list)
        print(tree_list[0])
        
    except (ValueError, IOError):
        print("ERROR: Bad value for N")
        return -1

def FindMaxSim(d):
    '''finds max similarity in dictionary
    '''
    max = 0
    for i in d.keys():
        for j in d[i].keys():
            if d[i][j] > max:
                (max_i, max_j) = (i,j)
                max = d[i][j]
                
    return (max_i, max_j)

def FindTreeNode(id, list):
    '''finds tree node with id from list
    '''
    for i in range(len(list)):
        if  list[i].id() == None:
            leaves = list[i].get_leaves_id(list[i])
            #print('leaves: ', end=' ')
            #print(leaves)
            if id in leaves:
                return i
            
        elif list[i].id() == id:
            return i
    
#def DeleteNode(id, list):
#    for i in range(len(list)):
#        if i.id() == id
    
def ConstructTree(dict, list):
    '''Constructs the tree, calls appropriate functions
       Parameter: dict - dictionary of similarities, list - tree list
       Returns: list of len 1
       Precondition: dict, list correct types
       Postcondition: list of len 1, theres is only one tree, with all subtrees under it
    '''

    while len(list) > 1:
        (max_t1, max_t2) = FindMaxSim(dict)
        #gets maximum similarity tree id
        
        #finds index of max
        index_t1 = FindTreeNode(max_t1, list)
        index_t2 = FindTreeNode(max_t2, list)
        
 
        #as long as not equal index
        #equal implies both id(organisms) already under same tree
        
        if index_t1 != index_t2:
            t0 = Tree(None, None)
            
            
            #list is ordered in descending similarity finals
            if index_t1 > index_t2:
                t0.add_tree(list[index_t1], list[index_t2])
                
            else:
                t0.add_tree(list[index_t2], list[index_t1])
            
            t0.set_min_sim(dict[max_t1][max_t2])
            t0.set_max_sim(dict[max_t1][max_t2])

            
            #deletes old trees
            del list[index_t1]
            index_t2 = FindTreeNode(max_t2, list)
            del list[index_t2]
            
            list.append(t0)
            
            #sets to zero because already compared
            dict[max_t1][max_t2] = 0
            
        else:
            dict[max_t1][max_t2] = 0
            

    return list
    
def InitializeTree(list):
    #initializes tree with name and id
    tree_list = []
    for o in list:
        leaf = Tree(o.name(), o.id())
        tree_list.append(leaf)
        
    return tree_list

def PrintOrganisms(list):
    #for testing purposes, prints genome list
    for o in list:
        print(o)
        
def PrintDictionary(dict):
    #prints dictionary of similarity with keys
    #for testing puproses
    for k1 in dict.keys():
        for k2 in dict[k1].keys():
            print(k1 + ' : ' + k2 + ' : ' + str(dict[k1][k2]))
            
def PrintTreeList(list):
    #prints tree list
    #for testing purposes
    for t in list:
        if t.id() == None:
            print(t.get_leaves_id(t), end = ' ')
        else:
            print(t.id(), end=' ')

def ComputeSimilarity(list):
    '''Constructs dictionary of similarity'''
    sim_dict = {}
    for i in range(len(list)):
        for j in range(i+1,len(list)):

            try:
                sim_dict[list[i].id()][list[j].id()] = Similarity(list[i].ngram(), list[j].ngram())
            except KeyError:
                sim_dict[list[i].id()] = {list[j].id() : Similarity(list[i].ngram(), list[j].ngram())}
                
    #PrintDictionary(sim_dict)
    return sim_dict
        

def Similarity(ngram1, ngram2):
    #gets similarity based on piccard index
    #calculates similarity 
    return float(len(ngram1.intersection(ngram2)))/float(len(ngram1.union(ngram2)))


def get_ngrams(seq, n):
    # your code here
    '''list comprehension ngrams
       Parameters: seq, n
       Precondition: seq: string, n, integer
       Returns: set of ngrams
    '''
    #checks if 1+n > len
    return set([seq[i:i+n] for i in range(0,len(seq)) if i + n <= len(seq)])
        

def main():
    if ReadInputFile() == -1:
        return

main()