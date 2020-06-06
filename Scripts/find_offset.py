import subprocess
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", dest="pattern_length", help="Pattern Length.", type=int)
    parser.add_argument("-e", "--eip", dest="eip", help="hex value EIP")
    options = parser.parse_args()
    if not options.pattern_length:
        parser.error("[-] Please specify the length of the payload. use -h for help.")
    if not options.fullpath:
        parser.error("[-] Please specify the full absoltu path to the binary. use -h for help.")
    return options




options = get_arguments()
len = options.length
filename = options.fullpath

p1 = subprocess.Popen(['/usr/share/metasploit-framework/tools/exploit/pattern_create.rb', '-l', len], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

pattern, err = p1.communicate()

print("\nUse this pattern in GDB: \n" + pattern)

eip = options.eip

p2 = subprocess.Popen(['/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb', '-l', len, '-q', eip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

offset, err = p2.communicate()

print(offset + "\n")
