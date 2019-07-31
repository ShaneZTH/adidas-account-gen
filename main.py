import requests
from bs4 import BeautifulSoup as bs
import json
from faker import Faker
from random import randint, choice
import string

from distutils.util import strtobool
from utils import Logger

logger = Logger()
fake = Faker()

class Generator():

	def __init__(self):
		"""
		Deals with config file
		"""
		with open('config.json') as file:
			self.config = json.load(file)
			file.close()

		"""
		Deals with user entered emails
		"""		
		with open('info.json') as file:
			self.info = json.load(file)
			file.close()
		self.count = 0


	def __generate_password(self):
		"""
		Generates a password according to the config file and returns it
		"""
		if self.config['password']['random']:
			allchar = string.ascii_letters + string.digits
			while True:
				password = "".join(choice(allchar) for x in range(randint(8, 12)))
				if any(i.isdigit() for i in password) and any(i.isupper() for i in password) and any(i.islower() for i in password):
					break
				else:
					continue
		else:
			password = self.config['password']['password']
		return password

		
	def generate(self,customize):
		"""
		Creates an account and returns email/password combination
		"""
		headers = {
			'origin': 'https://www.adidas.co.uk',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
		}
		try:
			s = requests.Session()
			r = s.get('https://www.adidas.co.uk/on/demandware.store/Sites-adidas-GB-Site/en_GB/MiAccount-Register', headers=headers)
			soup = bs(r.content, "html.parser")
			formUrl = soup.find('form')['action']
			secureKey = soup.find('input', {'name': 'dwfrm_mipersonalinfo_securekey'})['value']
			name = fake.name()
			print('name is ' + name)
			data = {
				'dwfrm_mipersonalinfo_firstname': name.split()[0],
				'dwfrm_mipersonalinfo_lastname': name.split()[1],
				'dwfrm_mipersonalinfo_customer_birthday_dayofmonth': randint(2,20),
				'dwfrm_mipersonalinfo_customer_birthday_month': randint(2,10),
				'dwfrm_mipersonalinfo_customer_birthday_year': randint(1940,1995),
				'dwfrm_mipersonalinfo_step1': 'Next',
				'dwfrm_mipersonalinfo_securekey': secureKey
			}
			headers['referer'] = 'https://www.adidas.co.uk/on/demandware.store/Sites-adidas-GB-Site/en_GB/MiAccount-Register'
			r = s.post(formUrl, data=data, headers=headers)
			headers['referer'] = formUrl
			soup = bs(r.content, "html.parser")
			formUrl = soup.find('form')['action']
			secureKey = soup.find('input', {'name': 'dwfrm_milogininfo_securekey'})['value']
			# if customize, then a read from self.info would be needed
			if customize:
				print('email is ' + self.info['emails'][self.count]) 
				email = self.info['emails'][self.count]
				self.count += 1
				# if self.count >= self.info['amount']
				# 	return False
			else:	
				email = "{}{}{}@{}".format(name.split()[0], name.split()[1], randint(111,999), self.config['domain'])
			
			password = self.__generate_password()
			data = {
				'dwfrm_milogininfo_email': email,
				'dwfrm_milogininfo_password': password,
				'dwfrm_milogininfo_newpasswordconfirm': password,
				'dwfrm_milogininfo_step2': 'Next',
				'dwfrm_milogininfo_securekey': secureKey
			}
			r = s.post(formUrl, data=data, headers=headers)
			headers['referer'] = formUrl
			soup = bs(r.content, "html.parser")
			formUrl = soup.find('form')['action']
			secureKey = soup.find('input', {'name': 'dwfrm_micommunicinfo_securekey'})['value']
			data = {
				'dwfrm_micommunicinfo_agreeterms': 'true',
				'dwfrm_micommunicinfo_step3': 'Register',
				'dwfrm_micommunicinfo_securekey': secureKey
			}
			r = s.post(formUrl, data=data, headers=headers)
		except:
			return False, None, None
		if "MiAccount-Redirect?justRegistered=true&redirect=" in str(r.content):
			return True, email, password
		else:
			return False, None, None


if __name__ == '__main__':
	generator = Generator()
	createdAccounts = []
	logger.log("Adidas Account Gen | v2.0")
	logger.log("[made by @ryan9918_]")
	logger.log("[Edit by @Shane]")
	logger.log("=============================================")
	valid = {"yes": True, "y": True,
             "no": False, "n": False}

	customize = strtobool(input("[ Source of Emails ] Customize[y/n]: "))
	# print(customize)

	num = input("[    USER    ] Number of accounts: ")
	# Customize VS Random source of emails
	if customize: 
		print('Customized process is triggered')

		for x in range(int(num)):
			success, email, password = generator.generate(True)
			if success:
				logger.success("Success creating account {}:{}".format(email, password))
				createdAccounts.append('{}:{}'.format(email, password))
			else:
				logger.error("Failed creating customized account")
	else:
		for x in range(int(num)):
			print('Random process is triggered')

			success, email, password = generator.generate(False)
			if success:
				logger.success("Success creating account {}:{}".format(email, password))
				createdAccounts.append('{}:{}'.format(email, password))
			else:
				logger.error("Failed creating random account")

	with open('accounts.txt', 'a') as file:
		for account in createdAccounts:
			file.write('{}\n'.format(account))
		file.close()