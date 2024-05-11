# mp4.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created Fall 2018: Margaret Fleck, Renxuan Wang, Tiantian Fang, Edward Huang (adapted from a U. Penn assignment)
# Modified Spring 2020: Jialu Li, Guannan Guo, and Kiran Ramnath
# Modified Fall 2020: Amnon Attali, Jatin Arora
# Modified Spring 2021 by Kiran Ramnath
"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    word_tag_counts = {}
    most_frequent_tag_by_word = {}
    overall_most_frequent_tag = None
    tag_count = {}

    # Step 1: Build the word_tag_counts dictionary
    for sentence in train:
        for word, tag in sentence:
            if word not in word_tag_counts:
                word_tag_counts[word] = {}
            if tag not in word_tag_counts[word]:
                word_tag_counts[word][tag] = 0
            word_tag_counts[word][tag] += 1
            
            # Count overall tag frequencies to determine the most common tag
            if tag not in tag_count:
                tag_count[tag] = 0
            tag_count[tag] += 1

    # Determine the overall most frequent tag
    overall_most_frequent_tag = max(tag_count, key=tag_count.get)

    # Step 2: Determine the most frequent tag for each word
    for word, tags in word_tag_counts.items():
        most_frequent_tag_by_word[word] = max(tags, key=tags.get)

    # Step 3: Tag the test data
    result = []
    for sentence in test:
        tagged_sentence = []
        for word in sentence:
            # Use the learned tags or the default tag for unseen words
            tag = most_frequent_tag_by_word.get(word, overall_most_frequent_tag)
            tagged_sentence.append((word, tag))
        result.append(tagged_sentence)

    return result
