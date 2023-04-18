from Crypto.Cipher import AES
from Crypto.Random import new as Random
from hashlib import sha256
from base64 import b64encode,b64decode

class AESCipher:
  def __init__(self,key):
    self.block_size = 16
    self.key = sha256(key.encode()).digest()[:32]
    self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr (self.block_size - len(s) % self.block_size)
    self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

  def encrypt(self, data):
    plain_text = self.pad(data)
    iv = Random().read(AES.block_size)
    cipher = AES.new(self.key,AES.MODE_OFB,iv)
    return b64encode(iv + cipher.encrypt(plain_text.encode())).decode()

  def decrypt(self, data):
    cipher_text = b64decode(data.encode())
    iv = cipher_text[:self.block_size]
    cipher = AES.new(self.key,AES.MODE_OFB,iv)
    return self.unpad(cipher.decrypt(cipher_text[self.block_size:])).decode()