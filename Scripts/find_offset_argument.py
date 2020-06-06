import os, re, sys

len = raw_input("\nEnter the pattern length: ")

filename = raw_input("\nEnter the absolute binary pathname: ")

execute = os.popen(filename + '$(cyclic ' + len + ')')

address = os.popen('dmesg | tail -n 2 | head -n 1 | cut -d ' ' -f 6').read()

#address = re.search('%s(.*)%s' % ('segfault at ', ' ip '), err).group(1)

offset = os.popen('cyclic -l 0x' + address).read()

sys.stdout.write("\033[F")
sys.stdout.write("\033[K")

print("\nThe offset is: " + offset)