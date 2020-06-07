import os, re, sys
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", dest="pattern_length", help="Pattern Length.", type=int)
    parser.add_argument("-p", "--path", dest="fullpath", help="absolute path to binary")
    options = parser.parse_args()
    if not options.pattern_length:
        parser.error("[-] Please specify the length of the payload. use -h for help.")
    if not options.fullpath:
        parser.error("[-] Please specify the full absoltu path to the binary. use -h for help.")
    return options


options = get_arguments()
len = options.pattern_length
filename = options.fullpath
execute = os.popen('cyclic ' + str(len) + '|' + filename)
address = os.popen('dmesg | tail -n 2 | head -n 1 | cut -d \':\' -f 2 | cut -d \' \' -f 4').read()

offset = os.popen('cyclic -l 0x' + address).read()

sys.stdout.write("\033[F")
sys.stdout.write("\033[K")

print("\nThe offset is: " + offset)
