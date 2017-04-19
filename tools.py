# -*- coding: utf-8 -*-
'''
Helper functions
'''
import re
import jieba.posseg as pseg


STOP_WORDS = open('stop_words', 'r', encoding='utf-8').read().split()
FLAG_LIST = ['p', 'u', 'a', 'd']
FIRST_HALF = 80
SECOND_HALF = 120


def is_han(char):
    'If the given character is a Chinese character'
    return '\u4e00' <= char <= '\u9fff'


class Chapter():
    'Class used to store and process a chapter'
    def __init__(self, text):
        self.text = text
        self.words = self.__get_words(self.text)
        self.num_words = len(self.words)
        self.num_characters = len([x for x in text if is_han(x)])

    def __get_words(self, text):
        'split text into words and store them in a dictionary'
        raw_list = pseg.cut(text)
        filtered = list()
        for word, flag in raw_list:
            if (flag in FLAG_LIST) and (word not in STOP_WORDS):
                filtered.append(word)
        return filtered


class Novel():
    'Class used to store and process a novel'
    def __init__(self, filename):
        self.text = open(filename, 'r', encoding='utf-8').read()
        self.chapters = self.__chapter_list(self.text)

    def __chapter_list(self, text):
        '''
        seperate text in to chapters with regular expressions
        return splitted chapters in list
        '''
        sep = re.compile(r'第.*?回\s')
        raw_chapters = sep.split(text)[1:]
        result = list()
        length = len(raw_chapters)
        for chapter_index in range(length):
            if chapter_index % 10 == 0:
                print('Processing chapter', chapter_index + 1, '...',
                      chapter_index + 10)
            result.append(Chapter(raw_chapters[chapter_index]))
        return result
