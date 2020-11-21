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


def removeEmojis(phrase):
    """
    removes all emojis from string
    :param phrase: a string
    """
    # replaces all emoji unicode with empty string
    return emoji.get_emoji_regexp().sub(r"", phrase)


def cleanDictionary(input_dict):
    """
    removes empty and stopword keys from dictionary
    :param input_dict: dictionary
    """
    input_dict = removeEmptyKeys(input_dict)
    input_dict = removeStopwords(input_dict)

    return input_dict


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