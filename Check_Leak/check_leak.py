#!/usr/bin/env python
import requests
import json
import os
import argparse


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

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "-field", dest="Field", help="Field to search in.")
	parser.add_argument("-q", "--query", dest="Query", help="Query to look for")
	parser.add_argument("-n", "--num", dest="Num", help="Number of results to display")
	parser.add_argument("-s", "--start", dest="Start", help="Number of start to display")
	parser.add_argument("-o", "--out-file", dest="OutFile", help="specify a file to save data to")
	options = parser.parse_args()
	if not options.Field:
		parser.error("[-] Please Specify the searchfield, use -h or --help for more info")
	if not parser.Query:
		parser.error("[-] Please specify a value to look for, use -h or --help for more info")
	if not parser.Num:
		parser.Num = '100'
	if not parser.Start:
		parser.Start = '0'
	if not parser.OutFile: #if the outfile is specified we can do it all in here because of our OO code ;)
		parser.OutFile = False
	return options

def set_para(options):
	params = (
		('q', options.Field + ":" + options.Query),
		('num', options.Num),
		# ('from', options.From),
	)
	return params

def Save_Result(json_data, line, cnt, fp):
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

def Print_Result(data_json):
	for i in range(len(data_json)):
		if 'Email' in data_json[i]["_source"]:
			source = Red + "Email: " + Blue + data_json[i]["_source"]["Email"] + NC
		elif 'User' in data_json[i]["_source"]:
			source = Red + "User: " + Blue + data_json[i]["_source"]["User"] + NC
		if 'Password' in data_json[i]["_source"]:
			data = Red + "Password: " + Blue + data_json[i]["_source"]["Password"] + NC
		elif 'PassHash' in data_json[i]["_source"]:
			data = Red + "Hash: " + Blue + data_json[i]["_source"]["PassHash"] + NC

		if data_json[i]["_score"] >= 4:
			print("   " + Red + "Domain: " + Blue + data_json[i]["_source"]["Domain"] + NC + "\n" + "   " + source + "\n" + "   " + data + "\n")

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

Options = get_arguments()
if Options.OutFile != False:
	filepath = Options.OutFile
	with open(filepath) as fp:
		line = fp.readline()
		cnt = 1
		while line:
			params = set_para(Options)
			response = requests.get('https://scylla.sh/search', headers=headers, params=params)
			print(Green + Bold + "Results about " + line.strip() + ":" + NC)
			json_data = json.loads(response.text)
			Save_Result(json_data, line, fp)

else:
	params = set_para(Options)
	response = requests.get('https://scylla.sh/search', headers=headers, params=params)
	print(Green + Bold + "Results about " + Options.Field + ":" + NC)
	json_data = json.loads(response.text)
	Print_Result(json_data)
