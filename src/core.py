import sys
import json

import config
from telegram_parser import getTelegramPhraseCounts
from messenger_parser import getMessengerPhraseCounts
from phrase_counts import combinePhraseCounts, processTopPhrases, printTopPhrases
from data_processing import normalizeMessengerData


if __name__ == "__main__":
    message_service = sys.argv[1]  # get messaging service from command line

    phrase_counts = {}

    index = 2
    while index < len(sys.argv):
        # open message history file(s) from command line
        with open(sys.argv[index]) as message_history_file:
            message_history = json.load(message_history_file)

        if message_service == "T":  # "T" for "Telegram"
            print("Parsing Telegram messages...")
            phrase_counts = getTelegramPhraseCounts(message_history)
        elif message_service == "M":  # "M" for "Messenger"
            message_history = normalizeMessengerData(message_history)

            print("Parsing Messenger messages...")
            temp_phrase_counts = getMessengerPhraseCounts(message_history)
            phrase_counts = combinePhraseCounts(temp_phrase_counts, phrase_counts)
        else:
            print("That messaging service isn't supported at this time.")
            exit()

        index = index + 1

    print("Analyzing messages...")
    phrase_counts = processTopPhrases(phrase_counts, config.NUM_TOP_PHRASES)

    printTopPhrases(phrase_counts)