from cryptography.fernet import Fernet


class Security:
  
  key= b'l_2e6j1mjZslEnU_MOBBuijyR4W2niRq00FsrcPPOg4='

  
  def encrypt(self, value):
    value = bytes(value,'utf-8')
    f = Fernet(self.key)
    token = f.encrypt(value)
    return token
  
  def decrypt(self, token):
    f = Fernet(self.key)
    return f.decrypt(token)
