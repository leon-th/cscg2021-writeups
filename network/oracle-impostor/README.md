# Oracle Impostor

## Information
**Category**: Network  
**Difficulty**: Medium    
**Author:** w4rum  
**Points:**
- **Junior:**   ?  
- **Senior:**   ?    
- **Earth:**    ?   

**First Blood:**    
- **Junior:**   Jasper  
- **Senior:**   Yannik
- **Earth:**    adragos

**Description:**
>Whether it's ancient Greek politics or cryptography, oracles make life a lot easier.   
>Except that you don't have one.   
>And this isn't about cryptography either.   
>You can start a local version of the challenge on your own system by starting server.py.   
>Once you know how to solve it, connect to our service via TCP at oracle-impostor.cscg.live:1024.     

**Challenge Files:**   
- `server.py`   
- `handler.py`   

## Overview
---
You have to enter the secret at the beginning, this is then compared with the real secret.   
If the entered secret is the right one, you will get the flag. 
If the secret is wrong there is a "drum roll", then the secret is sent and after that a new one is created.   

## Solution   
---
The goal is to receive the TCP packet with the secret but not to ack it, so that the socket gets timeouted and no new secret is created.   
I created a (not so nice) script that manually acks the packages.   
The secret package is not acked. In Wireshark I then could see the Secret and pass it to the script. The Secret is then sent and you get the flag.   
The script is not the nicest/best/most effective/fastest, but it works.

## Mitigation    
---
The new creation of the secret should happen independently of the socket state.   
For example you could put this at the beginning of the function.   

Leon T.