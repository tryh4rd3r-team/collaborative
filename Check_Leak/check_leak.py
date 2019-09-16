#!/usr/bin/env python
import requests, sys, json, os


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

os.system("clear")

Bold='\033[1m'
Red='\033[0;31m'
Magenta='\033[95m'
Green='\033[0;32m'
Blue='\033[0;94m'
Cyan='\033[0;36m'
Orange='\033[0;33m'
NC='\033[0m' # No Color

headers = {
    'Accept': 'application/json',
}

#LIST SEARCH
if (sys.argv[2] == "-l"):
	filepath = sys.argv[3]
	with open(filepath) as fp:
		line = fp.readline()
		cnt = 1
		while line:
			params = (
				('q', sys.argv[1] + ":" + line.strip()),
				('num', '1'),
				#('from', '200'),
			)

			response = requests.get('https://scylla.sh/search', headers=headers, params=params)

			json_data = json.loads(response.text)

			print(Green + Bold + "Results about " + line.strip() + ":" + NC)

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
	print(response.text.replace(',"_type":"_doc"},', '\n\n').replace('","', '"\n"'))

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
