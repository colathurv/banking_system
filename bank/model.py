import os
import sys
import string
import logging

from sqlalchemy import Column, DateTime, String, Float, Integer, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def setloglevel(loglevel):
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename='bankservices.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(loglevel)

class Person(Base):
    """The object representation of the Person Table"""
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    address = Column(String(80), nullable=False)
    phone = Column(String(15), nullable=False)

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

class Bank(Base):
    """The object representation of the Bank Table"""
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    city = Column(String(15), nullable=False)

    def __init__(self, name, city):
        self.name = name
        self.city = city

class BankEmployee(Base):
    """The object representation of the Employee Table with Relational Dependencies"""
    __tablename__ = 'employee'

    id = Column(Integer, primary_key = True)
    bank_id = Column(Integer,ForeignKey('bank.id'))
    bank = relationship(Bank)
    person_id = Column(Integer,ForeignKey('person.id'))
    person = relationship(Person)
    dept = Column(String(15), nullable = False)
    title = Column(String(10), nullable=False)
    modified_on = Column(DateTime, default=func.now())

    def __init__(self, bank_id, person_id, dept, title):
        self.bank_id = bank_id
        self.person_id = person_id
        self.dept = dept
        self.title = title


class BankAccount(Base):
    """The object representation of the Account Table with Relational Dependencies"""
    __tablename__ = 'account'

    acctnum = Column(Integer, primary_key = True)
    bank_id = Column(Integer,ForeignKey('bank.id'))
    bank = relationship(Bank)
    person_id = Column(Integer,ForeignKey('person.id'))
    person = relationship(Person)
    acct_type = Column(String(10), nullable=False)
    balance = Column(Float(40), nullable=False)
    int_rate = Column(Float(40), nullable=False)
    status = Column(String(10), nullable=False)
    modified_on = Column(DateTime, default=func.now())

    def __init__(self, bank_id, person_id, acct_type, int_rate, balance,status):
        self.bank_id = bank_id
        self.person_id = person_id
        self.acct_type = acct_type
        self.int_rate = int_rate
        self.balance = balance
        self.status = status

class BankLoan(Base):
    """The object representation of the Loan Table with Relational Dependencies"""
    __tablename__ = 'loan'

    loannum = Column(Integer, primary_key = True)
    bank_id = Column(Integer,ForeignKey('bank.id'))
    bank = relationship(Bank)
    person_id = Column(Integer,ForeignKey('person.id'))
    person = relationship(Person)
    balance = Column(Float(40), nullable=False)
    int_rate = Column(Float(40), nullable=False)
    status = Column(String(10), nullable=False)
    modified_on = Column(DateTime, default=func.now())

    def __init__(self, bank_id, person_id, int_rate, balance, status):
        self.bank_id = bank_id
        self.person_id = person_id
        self.int_rate = int_rate
        self.balance = balance
        self.status = status

class BankCreditCard(Base):
    """The object representation of the Credit Card Table with Relational Dependencies"""
    __tablename__ = 'creditcard'

    ccnum = Column(Integer, primary_key = True)
    bank_id = Column(Integer,ForeignKey('bank.id'))
    bank = relationship(Bank)
    person_id = Column(Integer,ForeignKey('person.id'))
    person = relationship(Person)
    limit = Column(Float(40), nullable=False)
    balance = Column(Float(40), nullable=False)
    int_rate = Column(Float(40), nullable=False)
    status = Column(String(10), nullable=False)
    modified_on = Column(DateTime, default=func.now())

    def __init__(self, bank_id, person_id, limit,balance,int_rate,status):
        self.bank_id = bank_id
        self.person_id = person_id
        self.limit = limit
        self.balance = balance
        self.int_rate = int_rate
        self.status = status

def cleanup(engine):
    """Helper function that will drop all tables in the DB and start on a clean slate"""
    connection = engine.connect()
    print("connected")
    trans = connection.begin()
    try:
        connection.execute("drop table if exists person")
        connection.execute("drop table if exists bank")
        connection.execute("drop table if exists employee")
        connection.execute("drop table if exists account")
        connection.execute("drop table if exists loan")
        connection.execute("drop table if exists creditcard")
        trans.commit()
        connection.close()
        print("tables dropped")
        Base.metadata.create_all(engine)
        print("table created")
    except Exception as e:
        trans.rollback()
        connection.close()
        print("error encountered while dropping/creating tables ..")
        print(e.print())