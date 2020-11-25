from . model import (Person, Bank, BankEmployee, BankAccount, BankLoan, BankCreditCard, setloglevel, cleanup)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging

class BankingServices:
	def __init__(self, engine):
		"""Constructor to establish connection with the RDBMS (Sqllite) for persistent storage"""
		if not engine:
			raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')
		self.engine = engine
		db_engine = create_engine(engine)
		db_session = sessionmaker(bind=db_engine)
		self.session = db_session()

	## Basic Services ##
	def create_bank(self,name,city):
		"""Create a bank, passing name and city. Identifier is sequence generated"""
		new_bank =Bank(name,city)
		self.session.add(new_bank)
		self.session.commit()
		logging.info("Bank Created")

	def get_bank_info(self, id):
		bank = self.session.query(Bank).filter(Bank.id==id).one()
		if bank == None:
			raise ValueError('No such bank with this id')
		else:
			return bank

	## Person Services ##
	def create_person(self, name, address, phone):
		"""Create a person, passing name, address and Phone. Identifier is sequence generated"""
		new_person = Person(name,address, phone)
		self.session.add(new_person)
		self.session.commit()
		logging.info("Person Created")

	def get_person_info(self, id):
		person = self.session.query(Person).filter(Person.id==id).one()
		if person == None:
			raise ValueError('No such person with this id')
		else:
			return person

	## Employee Services
	def create_employee(self, bank_id, person_id, dept, title):
		"""Create an employee, by passing an already created person and bank.Identifier is sequence generated"""
		new_employee =  BankEmployee(bank_id, person_id, dept, title)
		self.session.add(new_employee)
		self.session.commit()
		logging.info("Employee Created")

	def get_employee_info(self, id):
		employee = self.session.query(BankEmployee).filter(BankEmployee.id==id).one()
		if employee == None:
			raise ValueError('No such employee with this id')
		else:
			return employee

	##  Account Services ##
	def create_customer_account(self, bank_id, person_id,acct_type,int_rate,amount):
		"""Create a customer account, by passing an already created person and bank.Identifier is sequence generated"""
		balance = round(amount * (1 + int_rate), 2)
		status = "Active"
		new_customer_account =  BankAccount(bank_id, person_id, acct_type, int_rate, balance,status)
		self.session.add(new_customer_account)
		self.session.commit()
		logging.info("Account Created")

	def deposit_amount(self, acctnum, amount):
		account = self.session.query(BankAccount).filter(BankAccount.acctnum==acctnum).one()
		if account.status == 'Active':
			if amount > 0:
				account.balance = round(account.balance + amount * (1 + account.int_rate), 2)
				self.session.commit()
			else:
				raise ValueError('Amount has to be positive')
		else:
			raise ValueError('Amount can be deposited only to an Active account')

	def withdraw_amount(self, acctnum, amount):
		account = self.session.query(BankAccount).filter(BankAccount.acctnum==acctnum).one()
		if account.status == 'Active':
			if amount <= account.balance:
				account.balance -= amount
			else:
				msgstr = 'Amount withdrawn cannot exceed the balance'
				raise ValueError(msgstr)
				logging.error(msgstr)
		else:
			msgstr = 'Amount can be deposited only to an Active account'
			raise ValueError(msgstr)
			logging.error(msgstr)

	def get_account_info(self, acctnum):
		account = self.session.query(BankAccount).filter(BankAccount.acctnum==acctnum).one()
		if account == None:
			raise ValueError('No such account with this id')
		else:
			return account

	## Loan Services ##
	def create_customer_loan(self, bank_id, person_id,int_rate,amount):
		"""Create a loan, by passing an already created person and bank.Identifier is sequence generated"""
		balance = round(amount * (1 + int_rate), 2)
		status = "Active"
		new_customer_loan =  BankLoan(bank_id, person_id, int_rate, balance, status)
		self.session.add(new_customer_loan)
		self.session.commit()
		logging.info("Loan Created")

	def pay_towards_loan(self, loannum, amount):
		loan = self.session.query(BankLoan).filter(BankLoan.loannum==loannum).one()
		if loan.status == 'Active':
			if amount <= loan.balance:
				loan.balance -= amount
			else:
				msgstr = 'You cannot pay more than loan amount'
				raise ValueError(msgstr)
			if loan.balance == 0:
				loan.status == 'Paidoff'
			self.session.commit()
		else:
			msgstr = 'You can pay only to an active loan'
			raise ValueError(msgstr)
			logging.error(msgstr)

	def get_loan_info(self, loannum):
		loan = self.session.query(BankLoan).filter(BankLoan.loannum==loannum).one()
		if loan == None:
			raise ValueError('No such loan with this id')
		else:
			return loan

	## Credit Card Services ##
	def create_customer_credit_card(self, bank_id, person_id, limit, int_rate):
		"""Create a credit card account, by passing an already created person and bank.Identifier is sequence generated"""
		if limit < 1000.0:
			raise ValueError('Limit needs to be atleast 1000 dollars')
		status = "Active"
		balance = 0.00
		new_customer_cc =  BankCreditCard(bank_id, person_id, limit,balance,int_rate,status)
		self.session.add(new_customer_cc)
		self.session.commit()
		logging.info("Credit Card Created")

	def charge_card(self, ccnum, amount):
		creditcard = self.session.query(BankCreditCard).filter(BankCreditCard.ccnum==ccnum).one()
		if creditcard.status == 'Active':
			if amount < creditcard.limit - creditcard.balance:
				creditcard.balance = round(creditcard.balance + amount * (1 + creditcard.int_rate), 2)
				self.session.commit()
			else:
				msgstr = f"The amount you are charging exceeds the limit of {creditcard.limit}"
				raise ValueError(msgstr)
				logging.error(msgstr)
		else:
			msgstr = 'Your card is not active'
			raise ValueError(msgstr)
			logging.error(msgstr)

	def pay_card(self, ccnum, amount):
		creditcard = self.session.query(BankCreditCard).filter(BankCreditCard.ccnum==ccnum).one()
		if creditcard.status == 'Active':
			if amount <= creditcard.balance:
				creditcard.balance -= amount
				self.session.commit()
			else:
				raise ValueError(f"The amount you payoff should be less than or equal to {creditcard.balance}")
		else:
			raise ValueError('Your card is not Active')

	def get_cc_info(self, ccnum):
		creditcard = self.session.query(BankCreditCard).filter(BankCreditCard.ccnum==ccnum).one()
		if creditcard == None:
			raise ValueError('No such creditcard with this id')
		else:
			return creditcard