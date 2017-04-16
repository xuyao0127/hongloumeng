# -*- coding: utf-8 -*-

from collections import Counter
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import tools


def tf_idf(document_list):
    'Return tf-idf weight of given document list'
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(document_list))
    return tfidf.toarray()


def chapter_cluster(chapter_list):
    'Run k-means algorithm on given chapters'
    weight = tf_idf(chapter_list)
    print('Start Kmeans:')
    clf = KMeans(n_clusters=2).fit(weight)
    num_chapters = len(chapter_list)
    # Print cluster lable of each chapter
    for chapter_index in range(num_chapters):
        print('Chapter', chapter_index + 1, ':', clf.labels_[chapter_index])
    # Cumulate percentages of different clusters in first half and second half
    first_half = Counter(clf.labels_[:tools.FIRST_HALF])
    second_half = Counter(clf.labels_[tools.FIRST_HALF:])
    # Print result
    print('Chapter 1-80:')
    print('\tClass 0:', first_half[0], '/ 80', '=', first_half[0]/80)
    print('\tClass 1:', first_half[1], '/ 80', '=', first_half[1]/80)
    print('Chapter 81-120:')
    print('\tClass 0:', second_half[0], '/ 40', '=', second_half[0]/40)
    print('\tClass 1:', second_half[1], '/ 40', '=', second_half[1]/40)

    print(clf.inertia_)


def main():
    'Program entry'
    print('Preparing data:')
    novel = tools.Novel('hongloumeng.txt')
    chapters = [' '.join(chapter.words) for chapter in novel.chapters]
    chapter_cluster(chapters)

if __name__ == '__main__':
    main()
