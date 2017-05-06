from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///qa.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    issue_id = Column(Integer())
    issue_subject = Column(String())
    time_issue = Column(String(50))
    day = Column(String(50))

    def __init__(self, user_name, issue_id, issue_subject, time_issue, day):
        self.user_name = user_name
        self.issue_id = issue_id
        self.issue_subject = issue_subject
        self.time_issue = time_issue
        self.day = day
