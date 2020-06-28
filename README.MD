

# Telegram Social Engineering Tool (TSET)

Since Telegram is getting popular and most usabale instant message communication platform new attack vectors are appearing. This tool is dedicated to enchance and test information security mostly of first grade company employees.

### Disclaimer

This work is merely a demonstration of what adept attackers can do. It is the defender's responsibility to take such attacks into consideration and find ways to protect their users against this type of phishing attacks. TSET should be used only in legitimate penetration testing assignments with written permission from to-be-phished parties.

### Requirements

* Python >3.5
* MongoDB
* Tor
* Nginx

For python modules see requirements.txt file

### Installation

1. Install python3, nginx, supervisor, mongodb, tor
2. Install python modules from requirements
3. Create app and get Telegram API key and hash from https://my.telegram.org/auth  
4. Setup /config/main.txt
5. Setup /extensions/hello.py for penetration tester Telegram account 
6. Setup /templates/oauth for link to mimic
7. Gather scope of phones to test

### Usage

1. Run webserver with python script start.py at your domain.tld. You need at least 2 workers.
2. Generate and spread testing link: domain.tld?phone=XXXXXXXXXXX (only digits)
3. Read logs and receive notifications from /extensions/hello.py to find social weak points.

