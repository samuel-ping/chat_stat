import json

import config
from telegram_parser import getTelegramPhraseCounts
from phrase_counts import processTopPhrases, printTopPhrases


if __name__ == "__main__":
    with open("data/result.json") as message_history_file:
        message_history = json.load(message_history_file)

    print("Parsing messages...")
    phrase_counts = getTelegramPhraseCounts(message_history)

    print("Analyzing messages...")
    phrase_counts = processTopPhrases(phrase_counts, config.NUM_TOP_PHRASES)

    printTopPhrases(phrase_counts)