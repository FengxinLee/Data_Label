#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# @Author  : lifx
# @Time    : 2021/04/14 21:17
#
# @Class:
#   Trie
# @Function:
#   get_dictionary
#

# Building Trie & Persistence
from tqdm import tqdm
import threading
import sys
sys.setrecursionlimit(1000000)


class Trie:
    """
    Your Trie object will be instantiated and called as such:
        obj = Trie()
        obj.insert(word)
        param_2 = obj.search(word)
        param_3 = obj.startsWith(prefix)
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = {}
        self.end = -1

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """

        curNode = self.root
        for c in word:
            if not c in curNode:
                curNode[c] = {}
            curNode = curNode[c]
        curNode[self.end] = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        curNode = self.root
        for c in word:
            if not c in curNode:
                return False
            curNode = curNode[c]

        # Doesn't end here
        if not self.end in curNode:
            return False

        return True

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        curNode = self.root
        for c in prefix:
            if not c in curNode:
                return False
            curNode = curNode[c]

        return True

def get_dictionary(filename):
    """
    Getting the dictionary from txt file

    Args:
        filename (str): the dictionary of entities. The structure is shwon as:
            entityA
            entityB
            entityC
            ...
    Return:
        set: 
            {entityA, entityB, rntityC, ...}
    """
    entity_set = set()
    with open(filename, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '')
            if len(line) > 0:
                entity_set.add(str(line))

    return entity_set


def build_trie(entity_set):
    """
    Building the Trie using the dictionary of entity

    Args:
        entity_set (set): dictionary of entity. A set of string

    Return:
        trie:

    """
    trie = Trie()

    for entity in tqdm(entity_set):
        trie.insert(entity)

    return trie


import pickle


def persist_trie(trie, filename):
    """
    Persistence of the Trie

    Args:
        trie (Trie): 
        filename (str): filename of pickle

    """
    pickle.dump(trie, open(filename, 'wb'))


def get_trie_from_pickle(filename):
    """
    Loading the Trie from pickle file

    Args:
        filename (str): filename of pickle

    Return:
        tire

    """
    return pickle.load(open(filename, 'rb'))

def build_all_entity():
    dict_pk = {
        'dictionary/text/功效.txt': 'dictionary/trie/function.pk',
        'dictionary/text/手法.txt': 'dictionary/trie/operation.pk',
        'dictionary/text/症状.txt': 'dictionary/trie/symptom.pk',
        'dictionary/text/穴位.txt': 'dictionary/trie/xuewei.pk',
        'dictionary/text/身体部位.txt': 'dictionary/trie/body.pk',
        'dictionary/text/疾病.txt': 'dictionary/trie/disease.pk',
    }
    for (key, value) in dict_pk.items():
        trie = build_trie(get_dictionary(key))
        persist_trie(trie, value)
        print(key + ' is finished.')

def main_test():

    trie = get_trie_from_pickle('dictionary/trie/body.pk')

    print(trie.root)
    print(trie.search('脑勺'))

if __name__ == '__main__':
    # build_all_entity()
    trie = build_trie(get_dictionary('dictionary/text/穴位.txt'))
    persist_trie(trie, 'dictionary/trie/xuewei.pk')