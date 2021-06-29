import os
import sys
from datetime import datetime, timedelta
from time import sleep
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Message, Case

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:6432')
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)


class MessagingSession:
    def __init__(self):
        self.Session = sessionmaker(engine)
        self.session = self.Session()
        self.received_message = None

    def __enter__(self):
        self.session.begin()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not exc_type:
            self.session.commit()
        else:
            self.session.rollback()

            if self.received_message:
                self.session.begin()
                delay_until = datetime.now() + timedelta(seconds=15)
                self.received_message.do_not_process_until = delay_until
                self.session.commit()
                self.received_message = None

    def send_message(self, topic: str, payload: object):
        new_message = Message(topic=topic, payload=payload, do_not_process_until=datetime.now())
        self.session.add(new_message)

    def receive_message(self, topic: str) -> Message:
        date_now = datetime.now()

        self.received_message = self.session.query(Message).with_for_update(skip_locked=True)\
            .filter(Message.topic == topic, Message.do_not_process_until < date_now).first()

        if self.received_message:
            self.session.delete(self.received_message)

        return self.received_message

    def save_case(self, new_case: Case):
        self.session.add(new_case)

    def find_case(self, case_id: str) -> Case:
        return self.session.query(Case).get(case_id)


# noinspection PyBroadException
def start_receiving_messages(topic: str, callback: Callable[[MessagingSession, Message], None]):
    while True:
        try:
            with MessagingSession() as session:
                message = session.receive_message(topic)

                if message:
                    callback(session, message)
                else:
                    sleep(1 / 10)  # no messages, so wait 100ms before checking for another message
        except Exception:
            print(f'Error processing message: {sys.exc_info()[0]}')
