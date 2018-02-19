import json
import math
import random
import requests
from Crypto.PublicKey import RSA

url = "https://api.random.org/json-rpc/1/invoke"
api_key = '7c9e75b3-07a3-4492-a465-9bb542764258'
headers = {'content-type': 'application/json'}

def get_usage():
	global api_key 
	payload = {
			"jsonrpc": "2.0",
			"method": "getUsage",
			"params": {
				"apiKey": api_key
			},
			"id": 15998
		}
	response = requests.post(url, data=json.dumps(payload), headers=headers).json()
	result = None
	try:
		result = response['result']['bitsLeft']
	except:
		print(response)
	return result

def get_random_data(num_bits,chunks):
	global api_key 
	payload = {
			"jsonrpc": "2.0",
			"method": "generateBlobs",
			"params": {
				"apiKey": api_key,
				"n": chunks,
				"size": num_bits,
				"format": "hex"
			},
			"id": 42
		}
	response = requests.post(url, data=json.dumps(payload), headers=headers).json()
	result = None
	try:
		result = response['result']['random']['data']
	except:
		print(response)
	return result

def random_dot_org(n):
	return get_random_data(n*8,1)[0].decode('hex')

def generate_rsa_key(bits):
	if bits%256 != 0 or bits < 1024:
		return
	keys = RSA.generate(bits,randfunc=random_dot_org) 
	public_key = keys.publickey().exportKey("PEM") 
	private_key = keys.exportKey("PEM") 
	return private_key, public_key

def write_rsa_key(priv,pub):
	f = open('private_key.pem','wb')
	f.write(priv)
	f.close()
	f = open('public_key.pub','wb')
	f.write(pub)
	f.close()

bits = 1024
priv,pub = generate_rsa_key(bits)
write_rsa_key(priv,pub)
