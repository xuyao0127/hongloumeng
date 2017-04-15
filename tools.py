# -*- coding: utf-8 -*-
'''
Helper functions
'''
import re
import jieba
from collections import Counter


def isHan(text):
    'If text is contains Chinese characters only'
    return all('\u4e00' <= char <= '\u9fff' for char in text)


class Chapter():
    'Class used to store and process a chapter'
    text = ''
    words = dict()
    num_words = 0
    num_characters = 0
    word_bracket = list()

    def __init__(self, text):
        self.text = text
        self.words = self.__get_words(self.text)
        self.num_words = len(self.words)
        self.num_characters = len([x for x in text if isHan(x)])

    def __get_words(self, text):
        'split text into words and store them in a dictionary'
        word_bracket = jieba.cut(text)
        self.word_bracket = list(filter(isHan, word_bracket))
        return dict(Counter(self.word_bracket))


class Novel():
    'Class used to store and process a novel'
    text = ''
    chapters = list()
    num_chapters = 0

    def __init__(self, filename):
        f = open(filename, 'r', encoding='utf-8')
        self.text = f.read()
        self.chapters = self.__chapter_list(self.text)
        self.num_chapters = len(self.chapters)

    def __chapter_list(self, text):
        '''
        seperate text in to chapters with regular expressions
        return splitted chapters in list
        '''
        sep = re.compile(r'第.*?回\s')
        raw_chapters = sep.split(text)[1:]
        return list(map(Chapter, raw_chapters))


if __name__ == '__main__':
    n = Novel('hongloumeng.txt')
    print('Number of chapters: ', n.num_chapters)
    c = n.chapters[0]
    print('Content of first chapter')
    print(c.text)
    print('Number of unique words in first chapter: ', c.num_words)
    print('words braket', c.word_bracket)
