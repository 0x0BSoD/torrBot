import datetime


def log(message, answer):
    text = """
    [x] Datetime: {3}
    [x] User: {0}
    [x] Message: {1}
    [x] Answer: {2}
 ++++++++"""
    print(text.format(message.chat.username, message.text,
                      answer, datetime.datetime.now()))
