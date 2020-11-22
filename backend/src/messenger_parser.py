from phrase_counts import (
    PhraseCounts,
    updateCounts,
    getWordCount,
    getEmojiCount,
    getProfanityCount,
)
from data_processing import processWords, cleanDictionary, removeEmptyKeys


def getMessengerPhraseCounts(message_history):
    """
    returns dictionary of people mapped to a PhraseCounts() object
    :param message_history: JSON of Facebook Messenger message history
    """
    phrase_counts = {}

    word_count = {}  # number of times every word was used in message
    emoji_count = {}  # number of times every emoji was used in message
    profanity_count = 0

    # processing each individual message
    for message_object in message_history["messages"]:
        if message_object["type"] == "Generic":
            sender_name = message_object["sender_name"]

            try:
                message = message_object["content"]
            except KeyError:
                pass

            # initializes new PhraseCounts() object for new person in chat
            if sender_name not in phrase_counts:
                phrase_counts[sender_name] = PhraseCounts(sender_name)

            message_phrase = processWords(message)

            # get word count from current message and add those on to total word count
            word_count = updateCounts(
                getWordCount(message_phrase), phrase_counts[sender_name].word_count
            )

            # get emoji count from current message and add those on to total emoji count
            emoji_count = updateCounts(
                getEmojiCount(message_phrase), phrase_counts[sender_name].emoji_count
            )

            # update profanity count
            profanity_count = getProfanityCount(message_phrase)
            phrase_counts[sender_name].profanity_count = (
                phrase_counts[sender_name].profanity_count + profanity_count
            )

            # increment total number of messages
            phrase_counts[sender_name].total_messages = (
                phrase_counts[sender_name].total_messages + 1
            )
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