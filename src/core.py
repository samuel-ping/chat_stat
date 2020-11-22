import sys
import json

import config
from telegram_parser import getTelegramPhraseCounts
from messenger_parser import getMessengerPhraseCounts
from phrase_counts import combinePhraseCounts, sortPhrases, printTopPhrases
from data_processing import normalizeMessengerData
from chart_processing import generateBarChart, generatePieChart


if __name__ == "__main__":
    message_service = sys.argv[1]  # get messaging service from command line

    if message_service != "T" and message_service != "M":
        print("Don't forget to specify which messaging service you're parsing!")
        print("Usage: python core.py <message service> <message history file(s)>")
        exit()

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
    phrase_counts = sortPhrases(phrase_counts)
    # generateBarChart(phrase_counts["Samuel Ping"].getTopNWords(config.NUM_TOP_PHRASES))
    generatePieChart(phrase_counts["Samuel Ping"].getTopNWords(config.NUM_TOP_PHRASES))