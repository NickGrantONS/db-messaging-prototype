import os
import uuid

from sqlalchemy import MetaData, Column, String, JSON, create_engine, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:6432')

metadata = MetaData(schema='casev4')
Base = declarative_base(metadata=metadata)


class Message(Base):
    __tablename__ = "message"

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column('topic', String(255), index=True)
    payload = Column('payload', JSON)
    do_not_process_until = Column('do_not_process_until', DateTime, index=True)

    def __repr__(self):
        return (f"Message(id={self.id!r}, topic={self.topic!r}, payload={self.payload!r}"
                f", do_not_process_until={self.do_not_process_until!r})")


class Case(Base):
    __tablename__ = "cases"

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_ref = Column('case_ref', Integer)
    receipt_received = Column('receipt_received', Boolean)
    sample = Column('sample', JSON)

    def __repr__(self):
        return (f"Message(id={self.id!r}, case_ref={self.case_ref!r}, receipt_received={self.receipt_received!r}"
                f", sample={self.sample!r})")


if __name__ == '__main__':
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    metadata.create_all(engine)
