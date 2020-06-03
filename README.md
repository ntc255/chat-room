## Introduction
It's a worker-client communication system.

## Start
```
pip uninstall pycrypto
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

## Working 
**Here it will be explained how this system works.**
### Steps
- Running `initialize.py` will generate RSA keys 
- `server.py` will start server and now you can receive new client requests
- for each client run `client.py` and give command or text for others, it's described in the command line
  - you can send command to individual user , server will check if any user by such name exits.
  - text will be broadcasted to all users.
- write quit() to exit. 

## Future Plans
- Add acknowledgement
- username and password system
- public keys exchange system
- Prevention from DDOS attack
