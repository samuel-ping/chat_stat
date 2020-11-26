import sys
import json

from bs4 import BeautifulSoup

import config
from telegram_parser import getTelegramPhraseCounts
from messenger_parser import getMessengerPhraseCounts
from phrase_counts import combinePhraseCounts, sortPhrases, printTopPhrases
from data_processing import normalizeMessengerData
from chart_processing import generateBarChart, generatePieChart


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core.py <message history file(s)>")
        exit()

    phrase_counts = {}

    index = 1
    while index < len(sys.argv):
        # open message history file(s) from command line
        with open(sys.argv[index]) as message_history_file:
            message_history = json.load(message_history_file)

        if "title" in message_history:
            message_history = normalizeMessengerData(message_history)

            print("Parsing Messenger messages...")
            temp_phrase_counts = getMessengerPhraseCounts(message_history)
            phrase_counts = combinePhraseCounts(temp_phrase_counts, phrase_counts)
        elif "name" in message_history:
            print("Parsing Telegram messages...")
            phrase_counts = getTelegramPhraseCounts(message_history)
        else:
            print("Skipping file, that messaging service isn't supported at this time.")

        index = index + 1

    print("Analyzing messages...")
    phrase_counts = sortPhrases(phrase_counts)

    # create HTML file
    file_counter = 2
    file_name = "output/output.html"
    file_found = True

    # creates new html file
    while file_found:
        try:
            output_file = open(file_name)
        except:
            output_file_writer = open(file_name, "w")
            file_found = False
        file_name = "output/output" + str(file_counter) + ".html"
        file_counter = file_counter + 1

    html_outline = """<html>
                        <head></head>
                        <body>
                            <div id="charts"></div>
                        </body>
                    </html>"""

    soup = BeautifulSoup(html_outline, "html.parser")

    output_file_writer.write(soup.prettify(formatter=None))
    output_file_writer.close()