from phrase_counts import PhraseCounts, updateCounts, getWordCount, getEmojiCount
from data_processing import processWords, cleanDictionary, removeEmptyKeys


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