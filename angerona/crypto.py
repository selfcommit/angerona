from .models import Secret
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

import struct

class SecretEncrypter:
    def __init__(self):
        self.CipherText = None

    def encrypt(self, plaintext):
        if self.CipherText:
            raise RuntimeException('Instance of SecretEncrypter has already been used.')

        #get 32 long crypto-secure string using rng
        lookup = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWKYZ0123456789'
        uniqid = ''.join(lookup[ord(Random.get_random_bytes(1))%62] for _ in range(32))
        self.Nonce = Random.get_random_bytes(32)
        self.Salt = Random.get_random_bytes(32)

        #generate the hash of our UniqID (host-safing the data)
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, self.uniqid))
        self.UniqHash = hasher.digest()

        #generate the input for our key derivation formula
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, self.Nonce))
        keyhash = hasher.digest()

        #derive our AES key (aes256 wants 32bytes)
        aeskey = PBKDF2(
            password=keyhash,
            salt=self.Salt,
            dkLen=32,
            count=100000,
            )

        #derive our Iv from the UniqID (16 bytes)
        hasher = SHA256.new()
        hasher.update('{}{}'.format(uniqid, aeskey))
        aesiv = hasher.digest()[0:15]

        #pad from http://stackoverflow.com/a/12525165/274549
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        #unpad: unpad = lambda s : s[0:-ord(s[-1])]

        #encrypt it w/ padding
        cipher = AES.new(aeskey, AES.MODE_CBC, aesiv)
        self.CipherText = cipher.encrypt(pad(plaintext))

        # this is the only place the original uniqid is returned
        return uniqid

    def ret_secret(self):
        model = Secret()
        model.UniqHash = self.UniqHash
        model.Nonce = self.Nonce
        model.Salt = self.Salt
        model.Snippet = None
        model.ExpiryTime = None
        model.LifetimeReads = None
        model.CipherText = self.CipherText

        return model

class SecretDecrypter:
    def __init__(self):
        pass

