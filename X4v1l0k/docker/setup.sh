#!/bin/bash

apt-get update
apt-get --yes install build-essential
apt-get --yes install gcc-multilib g++-multilib
apt-get --yes install xinetd

user=vuln2
source=vuln2.c
binary=vuln2
port=3000

useradd $user
mkdir /home/$user
gcc -fno-stack-protector -z execstack -m32 $source -o $binary
rm -rf $source
cp $binary /home/$user/
rm -rf $binary
chown -R root:root /home/$user
chown root:$user /home/$user/$binary
chmod 2755 /home/$user/$binary

echo 0 | tee /proc/sys/kernel/randomize_va_space

echo "Soy la bandera!!" > /home/$user/flag
chown root:$user /home/$user/flag && chmod 440 /home/$user/flag;

cat <<EOF > /etc/xinetd.d/$user
service $user
{
    disable = no
    socket_type = stream
    protocol    = tcp
    wait        = no
    user        = $user
    bind        = 0.0.0.0
    server      = /home/$user/$binary
    type        = UNLISTED
    port        = $port
    flags = REUSE
    per_source = 5
    rlimit_cpu = 3
    nice = 18
}
EOF

service xinetd restart
