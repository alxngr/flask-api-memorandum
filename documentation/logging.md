# Logging

It is important that we are accountable for our application. In other words, we need to keep track of how our application behaves. For example, we might need to keep track of errors, transactions (for legal reasons) and so on... In order to do that, we are going to keep a **log** of some crucial functinonalities of our server.

NB: If we have a lot of users, our log files are soon going to grow out of hand. To store, search and analyze our logs more efficiently we can use [Elastic Search](https://www.elastic.co/elastic-stack). In order to visualize and share our logs through a dashboard, we can use [Kibana](https://www.elastic.co/kibana). We won't go over those solutions here.

To build a simple logging system, we can use the [logging](https://docs.python.org/3/howto/logging.html) python package.

We first define where we want our logs to be stored and how our log lines are going to be formatted in our configuration:

```python
import logging
import pathlib

class Config:
    ROOT = pathlib.Path(__file__).resolve()
    LOG_DIR = ROOT / 'logs'
    LOG_DIR.mkdir(exist_ok=True)
    LOG_FILE = LOG_DIR / 'api.log'
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
```

Then we create three methods to create our logger object:

```python
def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(Config.FORMATTER)
    return console_handler

def get_file_hanlder():
    file_handler = TimedRotatingFileHandler(Config.LOG_FILE, when='midnight')
    file_handler.setFormatter(Config.FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler

def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_hanlder())
    logger.propagate = False

    return logger
```

Here we have defined two handlers, one for handling the error coming from *stdout* and the other for message coming from our application directly. Notice that we use the [TimeRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler) so that a new log file is created at midnight (UTC) in order to not create too large of a log file. We could also have defined a handler to send critical errors to an email address and so on.

Now we can instantiate our logger object whenever we need it like so:

```python
logger = get_logger(logger_name=__name__)
````

And we can use it like so:

```python
logger.debug('this is at the debug level')
logger.info('this is at the info level')
logger.warning('this is at the warning level')
logger.error('this is at the error level')
logger.critical('this is at the critical level')
```
