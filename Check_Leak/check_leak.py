#!/usr/bin/env python
import requests
import json
import os
import argparse
import sys
import re


#AVAILABLE SEARCH
# - IP
# - PassSalt
# - UserId
# - Name
# - Email
# - User
# - Password
# - Username
# - PassHash
# - Domain


HASH_TYPE_REGEX = {
    re.compile(r"^[a-f0-9]{32}(:.+)?$", re.IGNORECASE):  ["MD5", "MD4", "MD2", "Double MD5",
                                                          "LM", "RIPEMD-128", "Haval-128",
                                                          "Tiger-128", "Skein-256(128)", "Skein-512(128",
                                                          "Lotus Notes/Domino 5", "Skype", "ZipMonster",
                                                          "PrestaShop"],
    re.compile(r"^[a-f0-9]{64}(:.+)?$", re.IGNORECASE):  ["SHA-256", "RIPEMD-256", "SHA3-256", "Haval-256",
                                                          "GOST R 34.11-94", "GOST CryptoPro S-Box",
                                                          "Skein-256", "Skein-512(256)", "Ventrilo"],
    re.compile(r"^[a-f0-9]{128}(:.+)?$", re.IGNORECASE): ["SHA-512", "Whirlpool", "Salsa10",
                                                          "Salsa20", "SHA3-512", "Skein-512",
                                                          "Skein-1024(512)"],
    re.compile(r"^[a-f0-9]{56}$", re.IGNORECASE):        ["SHA-224", "Haval-224", "SHA3-224",
                                                          "Skein-256(224)", "Skein-512(224)"],
    re.compile(r"^[a-f0-9]{40}(:.+)?$", re.IGNORECASE):  ["SHA-1", "Double SHA-1", "RIPEMD-160",
                                                          "Haval-160", "Tiger-160", "HAS-160",
                                                          "LinkedIn", "Skein-256(160)", "Skein-512(160)",
                                                          "MangoWeb Enhanced CMS"],
    re.compile(r"^[a-f0-9]{96}$", re.IGNORECASE):        ["SHA-384", "SHA3-384", "Skein-512(384)",
                                                          "Skein-1024(384)"],
    re.compile(r"^[a-f0-9]{16}$", re.IGNORECASE):        ["MySQL323", "DES(Oracle)", "Half MD5",
                                                          "Oracle 7-10g", "FNV-164", "CRC-64"],
    re.compile(r"^\*[a-f0-9]{40}$", re.IGNORECASE):      ["MySQL5.x", "MySQL4.1"],
    re.compile(r"^[a-f0-9]{48}$", re.IGNORECASE):        ["Haval-192", "Tiger-192", "SHA-1(Oracle)",
                                                          "XSHA (v10.4 - v10.6)"]
}


def obtain_hash_type(check_hash):
    found = False
    for algorithm in HASH_TYPE_REGEX:
        if algorithm.match(check_hash):
            found = True
            return enumerate_hash_types(HASH_TYPE_REGEX[algorithm])
    if found is False:
        return 0


def enumerate_hash_types(items):
    count = 0
    for item in items:
        count += 1
        if count <= 1:
            return format(item)


def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--field", dest="Field", help="Field to search in.")
	parser.add_argument("-q", "--query", dest="Query", help="Query to look for")
	parser.add_argument("-n", "--num", dest="Num", help="Number of results to display", default=100)
	parser.add_argument("-s", "--start", dest="Start", help="Number of start to display", default=0)
	parser.add_argument("-o", "--out-file", dest="OutFile", help="specify a file to save data to", default=False)
	options = parser.parse_args()
	if not options.Field:
		parser.error("[-] Please Specify the searchfield, use -h or --help for more info")
	if not options.Query:
		parser.error("[-] Please specify a value to look for, use -h or --help for more info")
	return options


def set_para(options):
	parameters = (
		('q', options.Field + ":" + options.Query),
		('num', options.Num),
		# ('from', options.From),
	)
	return parameters


def save_result(data_json):
	filePath = Options.OutFile
	sys.stdout = open(filePath, 'w')
	for i in range(len(data_json)):
		if 'Email' in data_json[i]["_source"]:
			source = Red + "Email: " + Blue + data_json[i]["_source"]["Email"] + NC
		elif 'User' in data_json[i]["_source"]:
			source = Red + "User: " + Blue + data_json[i]["_source"]["User"] + NC
		if 'Password' in data_json[i]["_source"]:
			data = Red + "Password: " + Blue + data_json[i]["_source"]["Password"] + NC
			is_hash = obtain_hash_type(data_json[i]["_source"]["Password"])
			if is_hash != 0 and is_hash != None:
				data += Red + "\n   Hash Type: " + Blue + is_hash + NC
		elif 'PassHash' in data_json[i]["_source"]:
			data = Red + "Hash: " + Blue + data_json[i]["_source"]["PassHash"] + NC
			is_hash = obtain_hash_type(data_json[i]["_source"]["PassHash"])
			if is_hash != 0 and is_hash != None:
				data += Red + "\n   Hash Type: " + Blue + is_hash + NC
		if data_json[i]["_score"] >= 4:
			print("   " + Red + "Domain: " + Blue + data_json[i]["_source"]["Domain"] + NC + "\n" + "   " + source + "\n" + "   " + data + "\n")


def print_result(data_json):
	for i in range(len(data_json)):
		if 'Email' in data_json[i]["_source"]:
			source = Red + "Email: " + Blue + data_json[i]["_source"]["Email"] + NC
		elif 'User' in data_json[i]["_source"]:
			source = Red + "User: " + Blue + data_json[i]["_source"]["User"] + NC
		if 'Password' in data_json[i]["_source"]:
			data = Red + "Password: " + Blue + data_json[i]["_source"]["Password"] + NC
			is_hash = obtain_hash_type(data_json[i]["_source"]["Password"])
			if is_hash != 0 and is_hash != None:
				data += Red + "\n   Hash Type: " + Blue + is_hash + NC
		elif 'PassHash' in data_json[i]["_source"]:
			data = Red + "Hash: " + Blue + data_json[i]["_source"]["PassHash"] + NC
			is_hash = obtain_hash_type(data_json[i]["_source"]["PassHash"])
			if is_hash != 0 and is_hash != None:
				data += Red + "\n   Hash Type: " + Blue + is_hash + NC
		if data_json[i]["_score"] >= 4:
			print("   " + Red + "Domain: " + Blue + data_json[i]["_source"]["Domain"] + NC + "\n" + "   " + source + "\n" + "   " + data + "\n")


os.system("clear")

Bold = '\033[1m'
Red = '\033[0;31m'
Magenta = '\033[95m'
Green = '\033[0;32m'
Blue = '\033[0;94m'
Cyan = '\033[0;36m'
Orange = '\033[0;33m'
NC = '\033[0m'    # No Color

headers = {
	'Accept': 'application/json',
}

Options = get_arguments()

params = set_para(Options)
response = requests.get('https://scylla.sh/search', headers=headers, params=params)
if Options.OutFile != False:
    sys.stdout = open(Options.OutFile, 'w')
print(Green + Bold + "Results about " + Options.Field + ":" + NC)
json_data = json.loads(response.text)
print_result(json_data)
sys.stdout = sys.__stdout__
if Options.OutFile != False:
    f = open(Options.OutFile, 'r')
    print f.read()
    f.close()
			for i in range(len(json_data)):
				if 'Email' in json_data[i]["_source"]:
					source = Red + "Email: " + Blue + json_data[i]["_source"]["Email"] + NC
				elif 'User' in json_data[i]["_source"]:
					source = Red + "User: " + Blue + json_data[i]["_source"]["User"] + NC
				if 'Password' in json_data[i]["_source"]:
					data = Red + "Password: " + Blue + json_data[i]["_source"]["Password"] + NC
				elif 'PassHash' in json_data[i]["_source"]:
					data = Red + "Hash: " + Blue + json_data[i]["_source"]["PassHash"] + NC

				if json_data[i]["_score"] >= 4:
					print("   " + Red + "Domain: " + Blue + json_data[i]["_source"]["Domain"] + NC + "\n" + "   " + source + "\n" + "   " + data + "\n")
				
			line = fp.readline()
			cnt += 1
else:

	#INDIVIDUAL SEARCH
	params = (
		('q', sys.argv[1] + ":" + sys.argv[2]),
		('num', '1'),
		#('from', '200'),
	)

	response = requests.get('https://scylla.sh/search', headers=headers, params=params)

	json_data = json.loads(response.text)

	#This print is to get all data and test the output
	#print(response.text.replace(',"_type":"_doc"},', '\n\n').replace('","', '"\n"'))

	print(Green + Bold + "Results about " + sys.argv[2] + ":" + NC)

	for i in range(len(json_data)):
		if 'Email' in json_data[i]["_source"]:
			source = Red + "Email: " + Blue + json_data[i]["_source"]["Email"] + NC
		elif 'User' in json_data[i]["_source"]:
			source = Red + "User: " + Blue + json_data[i]["_source"]["User"] + NC
		if 'Password' in json_data[i]["_source"]:
			data = Red + "Password: " + Blue + json_data[i]["_source"]["Password"] + NC
		elif 'PassHash' in json_data[i]["_source"]:
			data = Red + "Hash: " + Blue + json_data[i]["_source"]["PassHash"] + NC
		if 'Domain' in json_data[i]:
			domain = "Domain: " + Blue + json_data[i]["_source"]["Domain"] + NC + "\n"
		else:
			domain = ""

		if json_data[i]["_score"] >= 4:
			print("   " + Red + domain + "   " + source + "\n" + "   " + data + "\n")
