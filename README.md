Angerona
========

**Looking for a quick-start guide?  Try Angerona now using Docker!   [Click here](http://github.com/nextraztus/angerona/blob/master/Docker.md) for details.**
[![Install on DigitalOcean](http://installer.71m.us/button.svg)](http://installer.71m.us/install?url=https://github.com/selfcommit/angerona.git)

(After Build, navigate to http**s**://$IP-of_Droplet (The link from the builder will point you to htt**p**))

Angerona in mythology was the deity which protected Rome by keeping the sacred name of the city from its enemies; aptly-named, this project is a keeper of secrets. Unlike its namesake, these secrets are only protected for a finite amount of time or shares, after which they evaporate into the nether that is the ones and zeros of the modern world.  

Angerona is designed to allow the safe transfer of sensitive information over an insecure (but not real-time) attackable channel. This not the first project built to do this, but it is our spin on the idea. The main use-cases we find this useful for are also most obvious:

  - Passwords over email
  - Passwords over logging chat
  - One-off passwords to other employees that may or may not access to a particular team's password vault but don't need continued access

We threw the syntax highlighter piece in for the potential it had to be a nice way to quickly ship sensitive code back and forth.

Credits
-------
Angerona.pw takes its inspiration from [Password Pusher](www.pwpush.com) and adds a minor feature (syntax hilighting), many thanks them and projects like it.

Special thanks to Peter Grace for making deployment via docker possible and his expertise with Python/Pyramid!

Notes on Usage
--------------
Under no circumstances should both pieces of a credential (for example: username &amp; password) be sent in the same link or two links sent over the same channel. Real-time adversary would then have everything they needed. If, in the case of usernames and passwords, only the password was compromised but no other information, there's still plenty of other sleuthing and work that needs to be done.

Security Considerations
-----------------------
Obviously, sending passwords over insecure channels is never a good idea.  Anyone with the link can view the information contained within, after-all. So how is this any better?

* A current "secure" channel might later have unintentional audiences, by then, the Angerona link is invalid and the sensitive information lost
* The Angerona links show how many times a particular link has been viewed, if you were expecting just your recipient to view it once and it had evaporated when they clicked it within the expiry timeframe, you know your channel is being intercepted in real-time
* The information in Angerona is stored encrypted and with appropriate configuration of the forward-facing proxy is secured from even the host seeing the information contained

Installation
------------
Angerona is written in Python with the Pylons/Pyramid framework. It deploys like any standard Python web application using setuptools. It is also available as a self-contained Docker image. Out of the gate it will use an SQLite database that is local to the hosting computer.

You must provide a reverse-proxy in front of it and that proxy should use SSL. **The proxy should also be configured to discard anything sent to "/retr/"** for an ideal security standpoint. Angerona is designed to run in this configuration and may work poorly in any other. Besides, why would you want something designed to store passwords allow non-encrypted web traffic?

General steps for Pyramid app listed below:

- cd <directory containing this file>
- $VENV/bin/python setup.py develop
- $VENV/bin/initialize_angerona_db development.ini
- $VENV/bin/pserve development.ini

Encryption Scheme
-----------------
Angerona uses SHA256 and AES256, both considered secure for the time being. Even if someone were to somehow gain access to the backend database, there isn't much they could do with it. Here's why;

1. Alice sends plaintext, expiry data, and maximum views to Angerona over an encrypted channel (HTTPS)  
  *  let plaintext be "P"
  *  let expiry data and maximum views is considered insecure "metadata"
2. Angerona then generates several random numbers using a cryptographic-strength RNG
  * let random 32-character [a-zA-Z0-9] string be known as "uid"
  * let random 32-byte binary nonce [0x00 - 0xff] be known as "nonce"
  * let random 32-byte binary salt [0x00 - 0xff] be known as "salt"
  * let H1 be binary representation of SHA256(uid + uid) where '+' is concatenation operator
  * let H2 be binary representation of SHA256(uid + nonce) where '+' is the concatenation operator
3. Angerona then derives the appropriate information necessary to perform an AES256_CBC encryption of the data
  * let "key" be PBKDF2(H2, salt, 10k rounds)
  * let "iv" be first 16 bytes of SHA256(uid + key) where '+' is the concatenation operator
4. Angerona now has all the information necessary to encrypt the data; which is then padded with 0x00 bytes to be align with the 16-byte boundary imposed by CBC
5. Angerona encrypts the data
  * let ciphertext be "C"
6. Angerona then stores certain information in the database
  * INSERT (H1, nonce, salt, c, metadata)
7. Angerona returns a URL with "uid" to Alice
  * Alice may then transmit this URL to Bob

Note above, Angerona stores only the hash of the generated 32-character uid. Without the original uid data, we are unable to derive the appropriate AES key and IV used for the ciphertext.

