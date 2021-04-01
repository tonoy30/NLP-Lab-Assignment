import operator
import re
import sys

import pandas as pd
from tabulate import tabulate

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def load_data():
    df = pd.read_csv("data/eng_to_bang_data.csv")
    return df.iloc[:, 0], df.iloc[:, 1]


def corpus_size_words(data):
    size = 0
    for single_data in data:
        size += len(re.split('[; |,]+', single_data))
    return size


def corpus_size_lines(data):
    size = 0
    for single_data in data:
        sentences = re.split(r'[!?.।]+ +', single_data)
        size += len(sentences)
    return size


def corpus_size_chars(data):
    size = 0
    for single_data in data:
        size += len(single_data)-single_data.count(" ")
    return size


def avg_sen_len(total_words, total_sentences):
    return total_words/total_sentences


def vocabulary_size(data):
    unique_words = set()
    for single_data in data:
        sentences = re.split(r'\s', single_data)
        for sen in sentences:
            unique_words.add(sen)

    return unique_words


def lex_div(data):
    all_words = []
    for single_data in data:
        sentences = re.split(r'\s', single_data)
        for sen in sentences:
            all_words.append(sen)

    unique_words = vocabulary_size(data)
    word_freq = []
    for uni_word in unique_words:
        word_freq.append(all_words.count(uni_word))

    return sum(word_freq)/len(word_freq)


def top_ten_freq_words(data):
    all_words = []
    words_freq = {}

    for single_data in data:
        sentences = re.split(r'\s', single_data)
        for sen in sentences:
            all_words.append(sen)

    unique_words = vocabulary_size(data)
    total_words = len(all_words)

    for uni_word in unique_words:
        unit_word_freq = all_words.count(uni_word)
        word_percentage = (unit_word_freq/total_words)*100
        words_freq[uni_word] = [unit_word_freq, word_percentage]

    sorted_dic = sorted(words_freq.items(),
                        key=operator.itemgetter(1), reverse=True)
    return sorted_dic[:10]


def get_word_list_from_tuple(words):
    return [[words[i][0], words[i][1][0], round(words[i][1][1], 2)] for i in range(len(words))]


def histogram_table(bangle, english):
    table = [["Corpus size (in words) excluding punctuation", english[0], bangle[0]],
             ["Corpus size (in chars) excluding spaces",
              english[1], bangle[1]],
             ["Average sentence length (in words)", english[2], bangle[2]],
             ["Vocabulary size (no. of unique words)", english[3], bangle[3]],
             ["Lexical diversity*", english[4], bangle[4]],
             ["Corpus size (in lines)", english[5], bangle[5]]]
    headers = ["", "English side", "Bangle side"]
    print(tabulate(table, headers, tablefmt="pretty"))


def frequent_words_table(used_for, words):
    print(f"Top ten frequent words in the parallel corpusare ({used_for}): ")
    table = [[words[i][0], words[i][1], words[i][2]]
             for i in range(len(words))]
    headers = ["Words", "Frequency", "%"]
    print(tabulate(table, headers=headers, tablefmt="pretty"))


if __name__ == "__main__":
    eng, bd = load_data()
    bangle_results = [
        corpus_size_words(bd),
        corpus_size_chars(bd),
        avg_sen_len(corpus_size_words(bd), corpus_size_lines(bd)),
        len(vocabulary_size(bd)),
        lex_div(bd),
        corpus_size_lines(bd)
    ]
    english_results = [
        corpus_size_words(eng),
        corpus_size_chars(eng),
        avg_sen_len(corpus_size_words(eng), corpus_size_lines(eng)),
        len(vocabulary_size(eng)),
        lex_div(eng),
        corpus_size_lines(eng)
    ]
    print("Statistics from the parallel corpus:")
    histogram_table(bangle_results, english_results)

    ban_freq_words = top_ten_freq_words(bd)
    eng_freq_words = top_ten_freq_words(eng)
    print("Top ten frequent words in your parallel corpus:")
    frequent_words_table(
        "Bangle Side", get_word_list_from_tuple(ban_freq_words))
    frequent_words_table(
        "English Side", get_word_list_from_tuple(eng_freq_words))
