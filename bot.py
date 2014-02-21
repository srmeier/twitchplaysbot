import time;
import socket;
import subprocess;
import win32com.client;

data     = None;
sock     = socket.socket();
channel  = "channelname";
running  = False;
buffsize = 512;
password = "oauth:code";
nickname = "twitchusername";

#DEFINE KEYPRESS
def keypress(key):
	global shell, count
	subprocess.call("autohotkey "+key+".ahk");
#END KEYPRESS

#DEFINE PARSER
def parse(line):
	global data, sock, channel, running;
	if line[0:4]=="PING":
		sock.send(data.replace("PING", "PONG"));
	if len(line.split(" "))>1:
		if line.split(" ")[1]=="376":
			sock.send("JOIN #"+channel+"\r\n");
		elif line.split(" ")[1]=="PRIVMSG":
			if len(line.split(" "))<4:
				return;
			msg  = line.split(" ")[3].strip(":");
			user = line.split(" ")[0].split("!")[0].strip(":");
			
			# example keypress
			if msg=="up":
				keypress("up");
				print(user+": up");
#END PARSER

shell = win32com.client.Dispatch("WScript.Shell");

if raw_input()=="run": running = True;

#199.9.252.26
sock.connect(("irc.twitch.tv", 6667));
sock.send("PASS "+password+"\r\n");
sock.send("NICK "+nickname+"\r\n");

while running:
	data = sock.recv(buffsize);
	if not data: break;
	lines = data.split("\r\n");
	if "" in lines:
		lines.remove("");
	for line in lines:
		parse(line);

sock.close();
print("done");
