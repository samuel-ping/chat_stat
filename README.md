# chat_stat

## Usage

Output HTML file will be found in output/

```bash
$ python src/core.py <path to message history file> <(Optional) additional paths to message history files...>
```

Example for parsing single file:

```bash
$ python src/core.py
```

You can parse multiple files, as well as files from different messaging services:

```bash
$ python src/core.py M data/message-1.json data/message-2.json data/result.json
```

## Installation

First, create a virtual environment and enter it to isolate 3rd party packages for this program. There are multiple ways to do this.

```bash
$ python -m venv venv
$ . venv/bin/activate
```

Install the required packages in requirements.txt, and you're done!

```bash
$ pip install -r requirements.txt
```

## How to Use

To download Facebook Messenger chat history, go to https://www.facebook.com/dyi and request a copy of your messages in JSON format. It can take several hours before you can download your data.
