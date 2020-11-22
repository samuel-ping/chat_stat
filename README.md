# chat_stat

## Usage

```python
python src/core.py <messaging service> <path to message history file> <(Optional) additional paths to message history files...>
```

Example for opening Telegram file:

```python
python src/core.py T data/result.json
```

Example for opening Messenger file:

```python
python src/core.py M data/message-1.json
```

You can parse multiple files:

```python
python src/core.py M data/message-1.json data/message-2.json
```
