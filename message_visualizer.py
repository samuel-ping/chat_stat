import json
import string
import re

import emoji


def processWords(message_phrases):
    """
    removes punctuation and lowercases all words in list
    :param message_phrases: list of strings
    """
    message_phrases = [
        word.lower().strip(string.punctuation) for word in message_phrases
    ]  # turns all words lowercase, removes punctuation

    return message_phrases


def filterEmojis(message_phrases):
    """
    returns dict of number of times each emoji is used from all strings in list
    :param message_phrases: list of list of strings
    """
    emoji_count = {}

    for word in message_phrases:
        for letter in word:
            # splits string into list of single letters/emojis
            letter_list = emoji.get_emoji_regexp().split(letter)

            # removes trailing and leading empty strings from emoji lists
            while "" in letter_list:
                letter_list.remove("")
            letter = letter_list[0]

            # checks if letter is emoji
            if re.match(r"[\W]", letter):
                # increments count for this emoji in dict
                if letter in emoji_count:
                    emoji_count[letter] = emoji_count.get(letter) + 1
                else:
                    emoji_count[letter] = 1

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

    phrase_count = {}  # number of times every word/emoji was used in message history
    emoji_count = {}  # number of times every emoji was used in message history

    # processing each individual message
    for message_object in data["messages"]:
        messages = message_object["text"]

        message_phrases = messages.split(" ")  # turns each message into list of words

        message_phrases = processWords(message_phrases)
        # print(message_phrases)
        emoji_count = updateCounts(filterEmojis(message_phrases), emoji_count)

    # emoji_count.pop("\uFE0F")
    print(emoji_count)