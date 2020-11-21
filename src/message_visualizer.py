import json
import string
import regex
from collections import Counter

import emoji


class PhraseCounts:
    def __init__(self):
        self.name = ""
        self.word_count = {}  # number of times each word was used
        self.emoji_count = {}  # number of times each emoji was used
        self.total_messages = 0  # total number of messages sent

        self.top_words = []  # top words
        self.top_emojis = []  # top emojis

    def processTopNPhrases(self, num):
        """
        sets list of top N phrases in PhraseCount() object
        :param num: int of number of top phrases to get
        """
        self.top_words = dict(Counter(self.word_count).most_common(num))
        self.top_emojis = dict(Counter(self.emoji_count).most_common(num))

    def __str__(self):
        output = ""
        print(self.name, "'s Top Phrases:")
        print("-------------------------------------------------------")
        print(self.top_words)
        print(self.top_emojis)
        return output


def getTelegramPhraseCounts(message_history):
    """
    returns dictionary of people mapped to a PhraseCounts() object
    :param message_history: JSON of Telegram message history
    """
    phrase_counts = {}

    word_count = {}  # number of times every word was used in message
    emoji_count = {}  # number of times every emoji was used in message
    # processing each individual message
    for message_object in message_history["messages"]:
        if message_object["type"] == "message":
            sender_name = message_object["from"]
            message = message_object["text"]

            # initializes new PhraseCounts() object for new person in chat
            if sender_name not in phrase_counts:
                phrase_counts[sender_name] = PhraseCounts()
                phrase_counts[sender_name].name = sender_name

            message_phrase = processWords(message)

            # get word count from current message and add those on to total word count
            word_count = updateCounts(
                getWordCount(message_phrase), phrase_counts[sender_name].word_count
            )
            # get emoji count from current message and add those on to total emoji count
            emoji_count = updateCounts(
                getEmojiCount(message_phrase), phrase_counts[sender_name].emoji_count
            )
        elif message_object["type"] == "service":  # for calls and stuff
            continue
        else:
            continue

    # clean up phrase counts for every person
    for sender_name in phrase_counts:
        phrase_counts[sender_name].word_count = cleanDictionary(
            phrase_counts[sender_name].word_count
        )
        phrase_counts[sender_name].emoji_count = removeEmptyKeys(
            phrase_counts[sender_name].emoji_count
        )

    return phrase_counts


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
    for stopword in STOPWORDS:
        if stopword in input_dict:
            input_dict.pop(stopword)

    return input_dict


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


def processTopPhrases(phrase_counts, num):
    """
    iterates through dictionary and sets all top phrases
    :param phrase_counts: dictionary with strings mapping to PhraseCount() object
    :param num: int for number phrases
    """
    for name in phrase_counts:
        phrase_counts[name].processTopNPhrases(num)
    return phrase_counts


def printTopPhrases(phrase_counts):
    for name in phrase_counts:
        print(phrase_counts[name])


if __name__ == "__main__":
    with open("data/telegram-results.json") as message_history_file:
        message_history = json.load(message_history_file)

    # loading stopwords into global "constant" list
    global STOPWORDS
    STOPWORDS = []
    with open(
        "nltk_english_stopwords"
    ) as stopwords_file:  # stopwords retrieved from http://nltk.org/nltk_data/, "70. Stopwords Corpus" on 11/18/2020
        stopwords_lines = stopwords_file.readlines()
        for line in stopwords_lines:
            STOPWORDS.append(line.strip())

    print("Parsing messages...")
    phrase_counts = getTelegramPhraseCounts(message_history)

    print("Analyzing messages...")
    phrase_counts = processTopPhrases(phrase_counts, 10)

    printTopPhrases(phrase_counts)