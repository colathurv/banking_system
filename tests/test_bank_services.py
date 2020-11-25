# -*- coding: utf-8 -*-
from bank import services
from sqlalchemy import create_engine
import logging
import pytest

def check_bank_name(bank):
    assert bank.name == 'CitiBank', 'check bank name test failed'
    print('check bank name test passed')

def check_customer_address(person):
    assert person.address == '5670 Dewey Street', 'check customer address test failed'
    print('check customer address test passed')

def check_credit_card_balance(cc):
    assert cc.balance == 136.0, 'check customer cc balance test failed'
    print('check customer cc balance test passed')

if __name__ == '__main__':
	services.setloglevel(logging.INFO)
	enginestr = 'sqlite:///banksystem.db'
	engine = create_engine(enginestr)
	services.cleanup(engine)
	B = services.BankingServices(enginestr)
	B.create_bank("CitiBank", "Fremont")
	B.create_person("John Doe","3000 July Street","650-111-1111")
	B.create_person("Adam Doe","5670 Dewey Street","510-111-1111")
	B.create_employee(1,1,"Accounts","Manager")
	B.create_customer_account(1,2,"Savings",0.02,10.00)
	B.deposit_amount(1,100.00)
	B.withdraw_amount(1,10.00)
	B.create_customer_loan(1,2,0.12,1000.00)
	B.pay_towards_loan(1,100.00)
	B.create_customer_credit_card(1,2,2000,0.18)
	B.charge_card(1, 200.00)
	B.pay_card(1,100.00)

	bank = B.get_bank_info(1)
	person1 = B.get_person_info(1)
	person2 = B.get_person_info(2)
	employee = B.get_employee_info(1)
	account = B.get_account_info(1)
	loan = B.get_loan_info(1)
	cc = B.get_cc_info(1)

	print("===========================================")
	print("The following records have been created")
	print('Bank Info:')
	print("  ", bank.name, bank.city)
	print('Employee Info:')
	print("  ", person1.name, person1.address,person1.phone,employee.dept, employee.title)
	print('Customer Info:')
	print("  ", person2.name, person2.address,person2.phone)
	print('Customer Account Info:')
	print("  ", account.acct_type, account.balance, account.status)
	print('Customer Loan Info:')
	print("  ", loan.balance, loan.status)
	print('Customer Credit Card Info:')
	print("  ", cc.balance, cc.limit, cc.status)
	print("Pytests Commence")
	check_bank_name(bank)
	check_customer_address(person2)
	check_credit_card_balance(cc)

