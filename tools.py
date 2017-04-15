# -*- coding: utf-8 -*-
'''
Helper functions
'''
import re


def chapter_list(text):
    '''
    seperate text in to chapters with regular expressions
    return splitted chapters in list
    '''
    sep = re.compile(r'第.*?回\s')
    return sep.split(text)[1:]


if __name__ == '__main__':
    f = open('hongloumeng.txt', 'r', encoding='utf-8')
    text = f.read()
    chapters = chapter_list(text)
    print(len(chapters))
    for i in range(len(chapters)):
        print('chapter ' + str(i + 1) + ': ', len(chapters[i]), 'words')
