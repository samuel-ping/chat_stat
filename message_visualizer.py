import json
import string
import regex

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

        # get emoji count from current message and add those on to total emoji count
        emoji_count = updateCounts(getEmojiCount(message_phrases), emoji_count)

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


def removeEmojis(text):
    return emoji.get_emoji_regexp().sub(r"", text.decode("utf8"))


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


# returns list of top 5 words in dictionary phrase_count
def getTopPhrases(phrase_count):
    top_phrases = []
    index = 0

    # sort phrase_count

    # get top 5 phrases from phrase_count


if __name__ == "__main__":
    file = open("data/telegram-results.json")
    data = json.load(file)

    phrase_counts = getPhraseCounts(data)

    print(phrase_counts.emoji_count)