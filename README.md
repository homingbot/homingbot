# Homingbot

### Overview
Homingbot is a Fake SMTP Server &amp; Low-Maintenance Email Generator. Its content are set to automatically expire after a set duration. It is divided into 2 parts:
1. __Controller__ or 'API' handles all rest API calls.
2. __Nest__ or 'SMTP Server' receives incoming mails.

### Requirements
* Python3.6
* uvloop (Doesn't support windows, but works fine on [Bash On Ubuntu On Windows](https://msdn.microsoft.com/en-us/commandline/wsl/about))
* Cassandra 3+

### Running
1. Install requirements
`pip3.6 install -r requirements.txt`

2. Update `config.py`   
__Cassandra__   
Update cassandra_hosts. If cassandra has ssl enabled, you'll have to provide an ssl cert and key.   
__Nest__   
If you enable TLS, provide an ssl key and cert.

3. Launch
`python3.6 __main__.py`


### Usage
There are 3 API endpoints:

| Endpoint  | Method |  Variables |  Details |
| ------------- | ------------- | ------------- |  ------------- | 
| `/generate`  | POST  |  `count*` (INT)  |  Generates and returns `count` email accounts  |
| `/accounts`  | GET  |  NONE  |  Returns all accounts that are yet to expire  |
| `/emails`  | POST  | `account*` (TEXT), `index` (INT)  |  Returns the email-message(s) for the specified account  |

 \* - required
 
 ### License
 [MIT License](https://github.com/homingbot/homingbot/blob/master/LICENSE)
