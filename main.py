import multiprocessing
from datetime import datetime
from time import sleep
from messaging import start_receiving_messages, MessagingSession
from model import Case, Message

first_message_received = None
latest_message_received = None
total_messages_received = 0


def process_sample(session: MessagingSession, message: Message):
    global first_message_received
    global latest_message_received
    global total_messages_received
    print(f'Sample received: {message.payload}')
    new_case = Case()
    new_case.id = message.payload['id']
    new_case.case_ref = 123
    new_case.receipt_received = False
    new_case.sample = message.payload['sample']
    session.save_case(new_case)

    if not first_message_received:
        first_message_received = datetime.now()

    latest_message_received = datetime.now()
    total_messages_received += 1

    time_between_first_and_last_message = (latest_message_received - first_message_received).total_seconds()
    print(f'Average processing per message: '
          f'{time_between_first_and_last_message / total_messages_received} seconds')


def start_sample_listener():
    start_receiving_messages('sampleLoader.caseProcessor.sample', process_sample)


def process_receipt(session: MessagingSession, message: Message):
    print(f'Receipt received: {message.payload}')
    case_to_receipt = session.find_case(message.payload['payload']['response']['caseId'])
    case_to_receipt.receipt_received = True
    session.save_case(case_to_receipt)


def start_receipt_listener():
    start_receiving_messages('events.caseProcessor.receipt', process_receipt)


if __name__ == '__main__':
    process_manager = multiprocessing.Manager()
    daemons = [
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
        multiprocessing.Process(target=start_sample_listener, daemon=True),
    ]

    for daemon in daemons:
        daemon.start()

    print('Started message listeners')
    while True:
        sleep(1)
