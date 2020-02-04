'''

File: genome.py
Author: Adam Awale
Purpose: GenomeData class that stores the genome sequence and ngrams
'''
class GenomeData:
    #init the name, id sequence
    def __init__(self,name,id,sequence):
        self._name = name
        self._id = id
        self._sequence = sequence
        self._ngrams = set([])
        
    #getters
    def name(self):
        return self._name
    
    def id(self):
        return self._id
    
    def sequence(self):
        return self._sequence
    
    def ngram(self):
        return self._ngrams
    #setter
    def add_ngram(self, _set):
        self._ngrams = _set
        
    def str_ngrams(self):#returns a string of the ngrams
        _str = '['
        for o in sorted(self._ngrams):
            _str += o + ', '
        _str += ']'
        return _str
        
    def __str__(self):
        #for testinf purposes prints genome data
        return '>' + self._id + ' ' + self._name + '\n'\
            + self._sequence + '\n'\
            + self.str_ngrams()