import json
import string

def processWords(message_phrases):
    message_phrases = [
        word.lower().strip(string.punctuation) for word in message_phrases
    ]  # turns all words lowercase, removes punctuation

    return message_phrases

# returns list of top 5 words in dictionary phrase_count
def getTopPhrases(phrase_count):
    top_phrases = []
    index = 0
    # sort phrase_count
    # get top 5 phrases from phrase_count

if __name__ == "__main__":
    file = open("data/telegram-results.json")
    data = json.load(file)

    phrase_count = {}  # number of times every word/emoji was used in message history

    # processing each individual message
    for message_object in data["messages"]:
        messages = message_object["text"]

        message_phrases = messages.split(" ")  # turns each message into list of words

        message_phrases = processWords(message_phrases)
        print(message_phrases)
        