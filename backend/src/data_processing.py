import json
import string

import emoji

import config


def processWords(message_phrases):
    """
    removes punctuation and lowercases all words in list
    :param message_phrases: list of strings
    """
    try:
        # turns each message into list of words
        message_phrases = message_phrases.split(" ")
    except AttributeError:
        return ""

    message_phrases = [
        word.lower().strip(string.punctuation) for word in message_phrases
    ]  # turns all words lowercase, removes punctuation

    return message_phrases


def normalizeMessengerData(message_history):
    """
    recursively decodes Facebook Messenger chat history JSON, which when currently downloaded, is incorrectly formatted.
    code based on https://stackoverflow.com/a/62160255/13026376
    :param message_history: JSON dict
    """
    if isinstance(message_history, str):
        return message_history.encode("latin_1").decode("utf-8")

    if isinstance(message_history, list):
        return [normalizeMessengerData(message) for message in message_history]

    if isinstance(message_history, dict):
        return {
            key: normalizeMessengerData(item) for key, item in message_history.items()
        }

    return message_history


def cleanDictionary(input_dict):
    """
    removes empty and stopword keys from dictionary
    :param input_dict: dictionary
    """
    input_dict = removeEmptyKeys(input_dict)
    input_dict = removeStopwords(input_dict)

    return input_dict


def removeEmojis(phrase):
    """
    removes all emojis from string
    :param phrase: a string
    """
    # replaces all emoji unicode with empty string
    return emoji.get_emoji_regexp().sub(r"", phrase)


def removeEmptyKeys(input_dict):
    """
    trims empty keys from dictionary
    :param dict: dictionary which needs empty keys to be removed
    """
    new_dict = {}
    for key, value in input_dict.items():
        if key != "":
            new_dict[key] = value

    return new_dict


def removeStopwords(input_dict):
    """
    removes stopword keys from dictionary
    :param input_dict: dictionary
    """
    for stopword in config.STOPWORDS:
        if stopword in input_dict:
            input_dict.pop(stopword)

    return input_dict