import json
import string
import regex
from collections import Counter

import emoji


class PhraseCounts:
    def __init__(self):
        self.word_count = {}
        self.emoji_count = {}


def getPhraseCounts(data):
    """
    returns dictionary of number of times every phrase or emoji was used in messaging history
    :param data: JSON of message history
    """
    phrase_counts = PhraseCounts()

    word_count = {}  # number of times every word was used in message history
    emoji_count = {}  # number of times every emoji was used in message history

    # processing each individual message
    for message_object in data["messages"]:
        messages = message_object["text"]

        message_phrases = processWords(messages)

        # get word count from current message and add those on to total word count
        word_count = updateCounts(getWordCount(message_phrases), word_count)
        # get emoji count from current message and add those on to total emoji count
        emoji_count = updateCounts(getEmojiCount(message_phrases), emoji_count)

    word_count = removeEmptyKeys(word_count)
    emoji_count = removeEmptyKeys(emoji_count)

    phrase_counts.word_count = word_count
    phrase_counts.emoji_count = emoji_count

    return phrase_counts


def processWords(message_phrases):
    """
    removes punctuation and lowercases all words in list
    :param message_phrases: list of strings
    """

    # turns each message into list of words
    message_phrases = message_phrases.split(" ")

    message_phrases = [
        word.lower().strip(string.punctuation) for word in message_phrases
    ]  # turns all words lowercase, removes punctuation

    return message_phrases


def removeEmojis(phrase):
    """
    removes all emojis from string
    :param phrase: a string
    """
    # replaces all emoji unicode with empty string
    return emoji.get_emoji_regexp().sub(r"", phrase)


def removeEmptyKeys(dict):
    """
    trims empty keys from dictionary
    :param dict: dictionary which needs empty keys to be removed
    """
    new_dict = {}
    for key, value in dict.items():
        if key != "":
            new_dict[key] = value

    return new_dict


def getWordCount(message_phrases):
    """
    returns dict of number of times each word is used from all strings in list
    :param message_phrases: list of list of strings
    """
    word_count = {}

    for phrase in message_phrases:
        word = removeEmojis(phrase)

        # increments count for this emoji in dict
        if word in word_count:
            word_count[word] = word_count.get(word) + 1
        else:
            word_count[word] = 1

    return word_count


def getEmojiCount(message_phrases):
    """
    returns dict of number of times each emoji is used from all strings in list
    :param message_phrases: list of list of strings
    """
    emoji_count = {}

    for phrase in message_phrases:
        # groups unicode for emojis that use multiple unicode sequences
        words = regex.findall(r"\X", phrase)

        for word in words:
            if any(char in emoji.UNICODE_EMOJI for char in word):
                # increments count for this emoji in dict
                if word in emoji_count:
                    emoji_count[word] = emoji_count.get(word) + 1
                else:
                    emoji_count[word] = 1

    return emoji_count


def updateCounts(temp_dict, updated_dict):
    """
    updates updated_dict with temp_dict's values
    :param temp_dict: dictionary to add to updated_dict
    :param updated_dict: dictionary that will be combined with temp_dict's values
    """
    for phrase in temp_dict:
        if phrase in updated_dict:
            updated_dict[phrase] = updated_dict[phrase] + temp_dict[phrase]
        else:
            updated_dict[phrase] = temp_dict[phrase]

    return updated_dict


def getTopPhrases(phrase_count):
    """
    returns list of top 5 phrases in input dictionary
    :param phrase_count: dictionary of phrase counts
    """
    # top_phrases = []
    # index = 0

    # for phrase in phrase_count:
    #     if len(top_phrases) == 0:
    #         top_phrases.append(phrase)
    #     else:
    #         for top_phrase in top_phrases:
    #             if phrase_count.get(top_phrase) < phrase_count.get(phrase):
    #                 temp = top_phrase
    #                 top_phrases[index] = phrase
    #                 index = index + 1

    #                 while index < 5 and len(top_phrases < index):
    #                     top_phrases[index] = temp
    #                     temp = top_phrases[index]
    #                     index = index + 1
    #     index = 0

    top_phrases = dict(Counter(phrase_count).most_common(5))

    return top_phrases


if __name__ == "__main__":
    file = open("data/telegram-results.json")
    data = json.load(file)

    phrase_counts = getPhraseCounts(data)
    top_phrases = getTopPhrases(phrase_counts.word_count)
    print(top_phrases)
    top_emojis = getTopPhrases(phrase_counts.emoji_count)
    print(top_emojis)

    # print(phrase_counts.word_count)
    # print (phrase_counts.emoji_count)