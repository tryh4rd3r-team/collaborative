import subprocess

len = raw_input("\nEnter the pattern length: ")

p1 = subprocess.Popen(['/usr/share/metasploit-framework/tools/exploit/pattern_create.rb', '-l', len], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

pattern, err = p1.communicate()

print("\nUse this pattern in GDB: \n" + pattern)

eip = raw_input("Enter the $eip response address: ").replace("0x", "")

p2 = subprocess.Popen(['/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb', '-l', len, '-q', eip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

offset, err = p2.communicate()

print(offset + "\n")