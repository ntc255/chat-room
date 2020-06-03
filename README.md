## Introduction
It's a sockets based chat server that can be used for exchanging text messages as well as running system commands on the other machine (linux). Using TCP a protocol to identify the type of incoming data and correspondingly treat it like a text message or an instruction to run a command.


# Clone project
```
git clone https://github.com/ntc255/chat-room.git
```

## Start
```
pip install -r requirement.txt
python initialize.py
```

**Now you machine is ready!**

## Run
### Open server
```
python server.py
```
### Open client
```
python client.py
```

## Error handeling
- **Plain Text too long**
- **Unauthorized user**
- **No acknowledgement received**


## Working 
**Here it will be explained how this system works.**
### Steps
- Running `initialize.py` will generate RSA keys 
- `server.py` will start server and now you can receive new client requests
- for each client run `client.py` and give command or text for others, it's described in the command line
  - you can send command to individual user , server will check if any user by such name exits.
  - text will be broadcasted to all users.
- write quit() to exit. 

### Con: you have to enter to receive others response

## Future Plans
- Create a gui.
- username and password system
- public keys exchange system
- Prevention from DDOS attack
