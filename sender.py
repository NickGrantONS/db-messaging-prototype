import uuid

from messaging import MessagingSession


def send_sample():
    with MessagingSession() as session:
        sample = {
            "id": str(uuid.uuid4()),
            "sample": {
                "ADDRESS_LINE1": "123 Fake Street",
                "TOWN_NAME": "False Town",
                "POSTCODE": "AB1 2CD"
            }
        }

        for i in range(1, 1000):
            session.send_message('sampleLoader.caseProcessor.sample', sample)


def send_receipt():
    with MessagingSession() as session:
        receipt = {
            "event": {
                "type": "RESPONSE_RECEIVED",
                "source": "RH",
                "channel": "RH",
                "dateTime": "2021-06-09T14:10:11.910719Z",
                "transactionId": "730af73e-398d-41d2-893a-cd0722151f9c"
            },
            "payload": {
                "response": {
                    "caseIdxx": "22777d1d-593e-4066-bd34-4cb086d2461b"
                }
            }
        }

        session.send_message('events.caseProcessor.receipt', receipt)


if __name__ == '__main__':
    send_sample()

    # send_receipt()
