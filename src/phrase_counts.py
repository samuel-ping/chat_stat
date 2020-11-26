from collections import Counter

import emoji
import regex

import config
from data_processing import removeEmojis


class PhraseCounts:
    def __init__(self, name):
        self.name = name
        self.word_count = {}  # number of times each word was used
        self.emoji_count = {}  # number of times each emoji was used
        self.total_messages = 0  # total number of messages sent
        self.profanity_count = 0  # total number of profane words

        self.top_words = []  # top words
        self.top_emojis = []  # top emojis

    def processTopPhrases(self):
        """
        sorts all words from most used to least used into a list
        converts dict with word count to a Counter to use its most_common() function, which returns a list of tuples
        :param num: int of number of top phrases to get
        """
        self.top_words = Counter(self.word_count).most_common(len(self.word_count))
        self.top_emojis = Counter(self.emoji_count).most_common(len(self.emoji_count))

    def getTopNWords(self, num):
        """
        returns list of top n most used words
        :param num: number of words to return in list
        """
        return self.top_words[:num]

    def getTopNEmojis(self, num):
        """
        returns list of top n most used emojis
        :param num: number of emojis to return in list
        """
        return self.top_emojis[:num]

    def getNumberOfTimesSent(self, phrase):
        """
        returns int of number of times sent phrase in a message
        :param phrase: string
        """
        return self.word_count[phrase]

    def __str__(self):
        print(self.name + "'s Top Phrases:")
        print("-------------------------------------------------------")
        print(self.top_words)
        print(self.top_emojis)
        print("Total Messages:", self.total_messages)
        return ""


def sortPhrases(phrase_counts):
    """
    iterates through dictionary and sets all top phrases
    :param phrase_counts: dictionary with strings mapping to PhraseCount() object
    :param num: int for number phrases
    """
    for name in phrase_counts:
        phrase_counts[name].processTopPhrases()
    return phrase_counts


def getWordCount(message_phrases):
    """
    returns dict of number of times each word is used from all strings in list
    :param message_phrases: list of list of strings
    """
    word_count = {}

    for phrase in message_phrases:
        word = removeEmojis(phrase)

        # increments count for this word in dict
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


def getProfanityCount(message_phrases):
    """
    returns dict of number of times each word is used from all strings in list
    :param message_phrases: list of list of strings
    """
    profanity_count = 0

    for phrase in message_phrases:
        word = removeEmojis(phrase)

        # increments count for this emoji in dict
        for profane_word in config.PROFANE_WORDS:
            if word == profane_word:
                profanity_count = profanity_count + 1

    return profanity_count


def combinePhraseCounts(temp_dict, updated_dict):
    """
    combines temp_dict into updated_dict.
    :param temp_dict: dict of strings matching to PhaseCount()s to merge into updated_dict
    :param updated_dict: dict of strings matching to PhaseCount()s
    """
    for name in temp_dict:
        # update counts of words and emojis
        if name in updated_dict:
            updated_dict[name].word_count = updateCounts(
                temp_dict[name].word_count, updated_dict[name].word_count
            )
            updated_dict[name].emoji_count = updateCounts(
                temp_dict[name].emoji_count, updated_dict[name].emoji_count
            )
        else:
            updated_dict[name] = PhraseCounts(name)  # *flashbacks to memory management*
            updated_dict[name].word_count = temp_dict[name].word_count
            updated_dict[name].emoji_count = temp_dict[name].emoji_count

        # update total number of messages
        updated_dict[name].total_messages = (
            updated_dict[name].total_messages + temp_dict[name].total_messages
        )

    return updated_dict


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


def printTopPhrases(phrase_counts):
    """
    prints out all of the top messages sent by everybody
    :param phrase_counts: dictionary of strings matching to PhraseCount() objects
    """
    for name in phrase_counts:
        print(phrase_counts[name])