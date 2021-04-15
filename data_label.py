#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# @Author  : lifx
# @Time    : 2021/04/14 21:17
# @Function:
#

import Trie_Build
from Trie_Build import Trie
import os
from tqdm import tqdm


def split_text(text, title):
    """Split the text to samples. The length of the sample is less than 500.

    Args:
        text: string. The source text
        title: string. The prefix of the sample

    Returns:
        sample_list: a list of sample(:string)

    """
    title_len = len(title)
    max_len = 500 - title_len - 1  # The max length is 500
    # remove the blank and split the essay needed
    text = text.replace(' ', '')
    text = text.replace(' ', '')

    sample_list = []

    if len(text) < 500:
        sample_list.append(text)
        return sample_list

    text = text[title_len:]
    # split by sentence
    sentences = text.split('。')
    now_str = ''

    for sentence in sentences:
        now_len = len(now_str)
        sen_len = len(sentence)
        if now_len + sen_len >= max_len:
            sample_list.append(title + '。' + now_str)
            now_str = sentence
        else:
            now_str = now_str + sentence
        # to do list
        # if sen_len > 500:

    if len(title + '。' + now_str) < 500:
        sample_list.append(title + '。' + now_str)
        # print(now_str)  参考文献过多可能导致长度超过500

    return sample_list


def read_data_from_dir(folder):
    """Read text data for txt files
    The test data downloading from web is saved in the txt file.
    Each txt file contents one line -->  one essay

    Args:
        folder: string. the data dir

    Returns:
        str_list: The list of sample. The length of the sample is less than 500.
    """
    str_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            # find the txt file

            if os.path.split(file)[1][-4:] == '.txt':
                filename = os.path.join(root, file)
                # print('processing: ' + filename)
                # read the txt
                with open(filename, mode='r', encoding='utf-8') as f:
                    for line in f:
                        line = line.replace('\n', '')
                        line = line.strip()
                        if len(line) == 0:
                            continue
                        # find the title of the essay
                        title = line.split(' ')[0]
                        if len(title) == 0 or len(title) > 20:
                            title = line[:10]
                        # print('    title is ' + title)
                        # split the text
                        str_list = str_list + split_text(line, title)
    for sample in str_list:
        if len(sample) > 500:
            str_list.remove(sample)

    return str_list


def read_data_from_text(filename):
    """Read text data for txt files
    Each line is a sample
    Args:
        filename: string. The file storing data

    Returns:
        A list of sample(:string)
    """
    str_list_file = []
    with open(filename, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '')
            str_list_file.append(line)
    return str_list_file


def get_trie():
    """Load the Trie from json

    Returns:
        A dictionary of Trie
    """
    dict_pk = {
        'function': 'dictionary/trie/function.pk',
        'operation': 'dictionary/trie/operation.pk',
        'symptom': 'dictionary/trie/symptom.pk',
        'xuewei': 'dictionary/trie/xuewei.pk',
        'body': 'dictionary/trie/body.pk',
        'disease': 'dictionary/trie/disease.pk',
    }
    dict_trie = {}
    for (key, value) in dict_pk.items():
        t = Trie_Build.get_trie_from_pickle(value)
        dict_trie[key] = t
    print('Building Trie is finished.')
    return dict_trie


def data_label(data_list, dict_trie):

    # All entity kind
    key_list = ['function', 'operation', 'symptom', 'xuewei', 'body', 'disease']
    # The number of the entity
    label_total = {
        'function': 0,
        'operation': 0,
        'symptom': 0,
        'xuewei': 0,
        'body': 0,
        'disease': 0,
    }
    # The label of the entity
    label_dict = {
        'function': 'FUN',
        'operation': 'OPE',
        'symptom': 'SYM',
        'xuewei': 'XW',
        'body': 'BOD',
        'disease': 'DIS',
    }

    print('Labeling start.')
    for data_string in tqdm(data_list):
        


if __name__ == '__main__':
    str_list_1 = read_data_from_text('data.txt')
    dict_trie = get_trie()


