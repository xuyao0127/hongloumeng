# -*- coding: utf-8 -*-
'''
Helper functions
'''
import re
import jieba.posseg as pseg
from collections import Counter


def stop_words():
    'Return list of Chinese stop words'
    f = open('stop_words', 'r', encoding='utf-8')
    text = f.read()
    return text.split()


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
        stop = stop_words()
        raw_list = pseg.cut(text)
        for word, flag in raw_list:
            if isHan(word) and (not word in stop)  and (flag in ['p', 'u', 'a', 'd']):
                self.word_bracket.append(word)
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
    c = n.chapters[0]
    print(len(c.word_bracket))
