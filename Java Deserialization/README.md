# RCE - Java Deserialization

Exploit developed by: **X4v1l0k** and **Rival23**

This exploit is designed to be able to inject "cmd", "powershell" and "bash" commands, therefore it is compatible to take advantage of Java deserialization vulnerabilities in both Windows and Linux systems.

In order to use it, we need to have certain information such as Java's vulnerable payload such as "CommonsCollections1", the HMAC key for encrypting our load, the key for SSL encryption, the type of shell we are going to inject, the command that we want to inject and a valid URL.

The structure of the command should be similar to:
- python RCE-Java_Deserialization.py -u websiteurl/serializatedjava.faces -t cmd -k sslkey -m hmackey -p CommonsCollections1 -c "cmd command"

The exploit parameters are:
* "**-u**", "**--targetURL**": A vulnerable serializad java URL.
* "**-t**", "**--shellType**": The shell type to be injected (cmd, powershell, bash or none).
* "**-c**", "**--command**": The command to be injected.
* "**-m**", "**--hmacKey**": The HMAC key for encoding the HMAC payload.
* "**-p**", "**--payload-type**": The vulnerable Java payload.
* "**-x**", "**--testrce**": The test has been added in order to get a proof of concept. with the -x in place the -c "command" will be replaced by 3 pings to our own computer. While the pings will execute on the remote system our script starts listening on own computer for ping requests. The captured ping request will provide proof of remote code execution.
