# chat_stat

## Usage

Output HTML file will be found in output/

```bash
$ python src/core.py <messaging service> <path to message history file> <(Optional) additional paths to message history files...>
```

Example for opening Telegram file:

```bash
$ python src/core.py T data/result.json
```

Example for opening Messenger file:

```bash
$ python src/core.py M data/message-1.json
```

You can parse multiple files:

```bash
$ python src/core.py M data/message-1.json data/message-2.json
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

(To be continued)
