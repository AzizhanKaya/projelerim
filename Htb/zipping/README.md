# Machine

![image](https://github.com/AzizhanKaya/projelerim/assets/149832485/e02ac32f-58ff-4ed2-a959-2556ef62a15c)

# Enumeration

We can enumerate open ports of the system with nmap.

![Image 2-1](images/2-1.png)

![Image 2-2](images/2-2.png)

Looking at the results, we have just 2 ports open:
- SSH on port 22
- HTTP server on port 80

So we know we are dealing with a web application.

Scan version of open protocols with Nmap:

![Image 2-3](images/2-3.png)

Results:

![Image 2-4](images/2-4.png)

We have confirmed that it is a Linux server using the Apache web server.

# Web Application

![Image 3-1](images/3-1.png)

This is what the webpage looks like.

Discovering directories with ZAP:

![Image 3-2](images/3-2.png)

We have a zip file upload directory and a shop page.

Upload page:

![Image 3-3](images/3-3.png)

Shop page:

![Image 3-4](images/3-4.png)

## LFI

Testing LFI.

![Image 4-1](images/4-1.png)

It seems vulnerable. We'll come back to this later

## File Upload

The website only allows PDF files which are zipped to upload.

![Image 5-1](images/5-1.png)

So let's test to upload and capture the request with BurpSuite.

![Image 5-2](images/5-2.png)

Then send to the repeater tab. Also forward the request and look at the result at the web page.

![Image 5-3](images/5-3.png)

PDF File is being uploaded into directory named with hash of the file, and they have the PDF extension. So we have to find a way to RCE via uploading insecure files. The first idea is to get rid of the .pdf extension.

![Image 5-4](images/5-4.png)

Let's change the extension with Burp to .php.

![Image 5-5](images/5-5.png)

Response:

![Image 5-6](images/5-6.png)

We can't pass the firewall.

Let's try something else.

![Image 5-7](images/5-7.png)

Copy PHP reverse shell and edit our IP and listening port.

![Image 5-8](images/5-8.png)

Let's zip PHP reverse shell file.

![Image 5-9](images/5-9.png)

And rename .zip to .pdf.

![Image 5-10](images/5-10.png)

And zip again with .pdf.

![Image 5-11](images/5-11.png)

Upload reverse shell.

## RCE

It's time to use LFI. This phar is a PHP wrapper. Let's send our payload to run our PHP reverse shell.

![Image 6-1](images/6-1.png)

Don't forget to listen :)

![Image 6-2](images/6-2.png)

Finally, we have our shell.

## Privesc

As usual:

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
stty raw -echo; fg
TERM=xterm
```
Let's see what sudo tells us:

![Image 8-1](images/8-1.png)

We can do sudo stock without a password.

![Image 8-2](images/8-2.png)

Ohh.. Always think twice.

![Image 8-3](images/8-3.png)

Good news, we have permission to read.

![Image 8-4](images/8-4.png)

Let's grep the password.

![Image 8-5](images/8-5.png)

There you are.

![Image 8-6](images/8-6.png)

But the program doesn't give much.

So let's dive deeper and do some reverse engineering.

![Image 8-7](images/8-7.png)

Use strace to see what the program is doing

![Image 8-8](images/8-8.png)

*No such file or directory*

It happens when the program tries to include a library but couldn't. So we can add our payload to execute with the program and we can get root.

![Image 8-9](images/8-9.png)

Using msfvenom to create our payload.

![Image 8-10](images/8-10.png)

Start a web server to upload the payload file.

![Image 8-11](images/8-11.png)

Also download in .config directory.

Now listen and execute the program with sudo.

![Image 8-12](images/8-12.png)

We are root!

![Image 8-13](images/8-13.png)

And here is the flag!!
