# Messaging via a database table: a prototype
Using a message-oriented-middleware product, like ActiveMQ, Kafka, RabbitMQ, SQS, Google PubSub or any of the many others, is total overkill for most applications. As such, why not just use a database table as a kind of persistent queue? Well, because there are other problems to solve.

## What problems is this project solving?
The messaging platform of your choice offers a mechanism of easily setting up queue consumers, such that your application can scale. Using a queue would cause contention between the consumers, which could result in messages being processed more than once. Also, how do you run multiple instances? How do you deal with failures?

This prototype demonstrates how to listen to multiple queues, with guaranteed once and once only message delivery, no message loss, and a retrying mechanism.

## How does it work?
Fundamentally, it's using the power of the database to take care of transactions and row locking, to produce the desirable messaging behaviour, without the heavyweight messaging middleware.

## I want to consume messages. How do I do it?
Like this:
```python
from messaging import start_receiving_messages, MessagingSession
from model import Message

def process_my_message(session: MessagingSession, message: Message):
    # TODO: here's where you do stuff with the message

start_receiving_messages('myTopic', process_my_message)
```

## I want to send messages. How do I do it?
Like this:
```python
from messaging import MessagingSession

with MessagingSession() as session:
    my_message = {"foo": "bar"}
    session.send_message('myTopic', my_message)
```

## I want to consume messages, do CRUD stuff in the DB, and then send messages. How?
Like this:
```python
from messaging import start_receiving_messages, MessagingSession
from model import Message

def process_my_message(session: MessagingSession, message: Message):
    new_thing = MyThing()
    new_thing.foo = "bar"
    session.save_thing(new_thing)

    my_message = {"yin": "yang"}
    session.send_message('myOtherTopic', my_message)

start_receiving_messages('myTopic', process_my_message)
```
