//gcc -fno-stack-protector -z execstack -m32 vuln2.c -o vuln2

#include <stdio.h>
#include <string.h>

int	vuln()
{
	char	buf[32];
	puts("\nPlease, tell me something:");
    fgets(buf,500,stdin);
	printf("\nYou told: %s\n", buf);
	return (0);
}

int	main()
{
	vuln();
	return (0);
}