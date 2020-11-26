import sys
import json

if __name__ == "__main__":
    # if "t" not in message_service and "m" not in message_service:
    if len(sys.argv) < 4:
        print(
            "Usage: python name_changer.py <name> <new name> <message history file(s)>"
        )
        exit()

    val = input(
        "WARNING: Make sure to keep a backup of the files you're modifying! To proceed, type 'y'. To exit, type 'n'.\n"
    )

    if val != "y":
        print("Exiting.")
        exit()
    else:
        print("Proceeding.")

    # get command line arguments
    old_name = sys.argv[1]
    new_name = sys.argv[2]

    index = 3
    while index < len(sys.argv):
        # open message history file(s) from command line
        with open(sys.argv[index]) as message_history_file:
            message_history = json.load(message_history_file)

        for message_object in message_history["messages"]:
            # for Messenger chat histories
            try:
                if message_object["sender_name"] == old_name:
                    message_object["sender_name"] = new_name
            except KeyError:
                pass

            # for Telegram chat histories
            try:
                if message_object["from"] == old_name:
                    message_object["from"] = new_name
            except KeyError:
                pass

        modified_message_history = json.dumps(message_history, indent=2)
        print(modified_message_history)
        with open(sys.argv[index], "w") as new_file:
            new_file.write(modified_message_history)

        index = index + 1