# -*- coding: utf-8 -*-

from collections import Counter
from os import path
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster import hierarchy
from sklearn.decomposition import IncrementalPCA
import matplotlib
import matplotlib.pyplot as plt
import tools


def tf_idf(document_list):
    'Return tf-idf weight of given document list'
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(document_list))
    return tfidf.toarray()


def kmeans(chapter_list):
    'Run k-means algorithm on given chapters'
    weight = tf_idf(chapter_list)
    result = KMeans(n_clusters=2).fit(weight)
    num_chapters = len(chapter_list)
    # Print cluster lable of each chapter
    for chapter_index in range(num_chapters):
        print('Chapter', chapter_index + 1, ':', result.labels_[chapter_index])
    # Cumulate percentages of different clusters in first half and second half
    first_half = Counter(result.labels_[:tools.FIRST_HALF])
    second_half = Counter(result.labels_[tools.FIRST_HALF:])
    # Print result
    print('Chapter 1-80:')
    print('\tClass 0:', first_half[0], '/ 80', '=', first_half[0]/80)
    print('\tClass 1:', first_half[1], '/ 80', '=', first_half[1]/80)
    print('Chapter 81-120:')
    print('\tClass 0:', second_half[0], '/ 40', '=', second_half[0]/40)
    print('\tClass 1:', second_half[1], '/ 40', '=', second_half[1]/40)
    print('Plotting clusters in 2D graph:')
    ipca = IncrementalPCA(n_components=2)
    ipca.fit(weight)
    reduction = ipca.transform(weight)
    colors = ['c', 'orangered']
    for chapter_index in range(num_chapters):
        plt.scatter(reduction[chapter_index, 0], reduction[chapter_index, 1],
                    c=colors[int(result.labels_[chapter_index])], marker='x')
    plt.show()


def hierarchical(chapter_list):
    'Run hierarchical algorithm on given chapters'
    weight = tf_idf(chapter_list)
    result = AgglomerativeClustering(n_clusters=2).fit(weight)

    num_chapters = len(chapter_list)
    # Print cluster lable of each chapter
    for chapter_index in range(num_chapters):
        print('Chapter', chapter_index + 1, ':', result.labels_[chapter_index])
    # Cumulate percentages of different clusters in first half and second half
    first_half = Counter(result.labels_[:tools.FIRST_HALF])
    second_half = Counter(result.labels_[tools.FIRST_HALF:])
    # Print result
    print('Chapter 1-80:')
    print('\tClass 0:', first_half[0], '/ 80', '=', first_half[0]/80)
    print('\tClass 1:', first_half[1], '/ 80', '=', first_half[1]/80)
    print('Chapter 81-120:')
    print('\tClass 0:', second_half[0], '/ 40', '=', second_half[0]/40)
    print('\tClass 1:', second_half[1], '/ 40', '=', second_half[1]/40)
    print('Plotting clusters in 2D graph:')
    ipca = IncrementalPCA(n_components=2)
    ipca.fit(weight)
    reduction = ipca.transform(weight)
    colors = ['c', 'orangered']
    for chapter_index in range(num_chapters):
        plt.scatter(reduction[chapter_index, 0], reduction[chapter_index, 1],
                    c=colors[int(result.labels_[chapter_index])], marker='x')
    plt.show()


def dendrogram(chapter_list):
    'Run hierarchical algorithm on given chapters with graph'
    weight = tf_idf(chapter_list)
    result = hierarchy.linkage(weight, 'ward')
    hierarchy.set_link_color_palette(['c', 'orangered'])
    hierarchy.dendrogram(result, color_threshold=2, above_threshold_color='c')
    plt.show()


def main():
    'Program entry'
    print('Preparing data:')
    novel = tools.Novel('hongloumeng.txt')
    chapters = [' '.join(chapter.words) for chapter in novel.chapters]
    # EDA
    # Number of function words
    num_words_list = [len(Counter(x.split(' '))) for x in chapters]
    plt.plot(range(1, 121), num_words_list, marker='x', color='c',
             label='Duplicate')
    num_words_list = [len(x.split(' ')) for x in chapters]
    plt.plot(range(1, 121), num_words_list, marker='x', color='orangered',
             label='Unique')
    plt.grid(True)
    plt.xlabel('Chapter Index')
    plt.ylabel('Words')
    plt.title('Number of Function Words in Each Chapter')
    plt.legend()
    plt.show()
    # number of characters
    num_chars_list = [x.num_characters for x in novel.chapters]
    plt.plot(range(1, 121), num_chars_list, marker='x', color='c')
    plt.xlabel('Chapter Index')
    plt.ylabel('Characters')
    plt.title('Number of Characters in Each Chapter')
    plt.grid(True)
    plt.show()
    # Clusters
    print('Start Kmeans:')
    kmeans(chapters)
    print('Start hierarchical clustering:')
    hierarchical(chapters)
    print('Generating dendrogram:')
    dendrogram(chapters)


if __name__ == '__main__':
    main()
