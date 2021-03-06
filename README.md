# PythonTCPServer

Simple Python 3 TCP Server

## Features
* easy to extend
* YAML configuration
* Implement commands or scripts via configuration
* simple authentication
* simple brute force protection
* server logging
* client timeout
* dynamic help (list commands from config)
* passthrough command output to client

## Requirements 

[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/downloads/)
[![pyyaml](https://img.shields.io/badge/pyyaml-5.x-green)](https://pyyaml.org/wiki/PyYAMLDocumentation)

(tested with python 3.9 and pyyaml 5.1)

## Configuration

Just adjust the config.yaml, make sure the port is open in your firewall

In the commands section of the file you can simply add commands that the server will provide and run
```sh
call: the program or script which will be called
arg: comma seperated list of arguments
```

## Security

The login token is the current date in format "dd.mm.yyyy" (not very save, in production you should replace that part of code).

Make sure to restrict the edit permissions of the configuration file, otherwise the server functionality could be extend to run any command from remote.

The brute force protection will only set a sleep time, in production maybe this should extend with client disconnection and ip blocking. 

## Usage

you can use ncat (https://nmap.org/ncat/) or telenet to connect to your tcp server (from mobile device you can use tmux with ncat) or write your own frontend client or app.

to start the server just run the tcpServer.py, on windows if you want to run it as service just use https://nssm.cc/usage


## Example

<img src="https://github.com/secure-77/PythonTCPServer/blob/master/Example.png?raw=true" width="500">

### Sources

https://pymotw.com/3/socket/tcp.html

https://hackersandslackers.com/simplify-your-python-projects-configuration/

