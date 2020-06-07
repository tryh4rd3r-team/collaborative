import os, argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", dest="pattern_length", help="Pattern Length.", type=int)
    parser.add_argument("-p", "--path", dest="fullpath", help="absolute path to binary")
    parser.add_argument("-e", "--eip", dest="eip", help="hex value EIP")
    options = parser.parse_args()
    if not options.pattern_length:
        parser.error("[-] Please specify the length of the payload. use -h for help.")
    if not options.fullpath:
        parser.error("[-] Please specify the full absoltu path to the binary. use -h for help.")
    return options




options = get_arguments()
len = options.pattern_length
filename = options.fullpath

pattern = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l ' + str(len)).read()

if not options.eip:
    print("\nUse this pattern in GDB: \n" + pattern)
else:
    eip = options.eip

    offset = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l ' + str(len) + ' -q ' + str(eip)).read()

    print(offset + "\n")
