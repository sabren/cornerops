"""
Uses GPG to encrypt credit card information
"""
from strongbox import *
from pytypes import Date
from GnuPG import *

def xor(a,b):
    return (a and not b) or (b and not a)

class EncryptedCard(Strongbox):

    owner = attr(str)
    number = attr(str)
    expire = attr(Date)
    _cipher = attr(str)

    def __init__(self, cipher=None, **kwargs):
        assert not (cipher and kwargs), "cipher/kwargs mutually exclusive"
        super(EncryptedCard, self).__init__(**kwargs)
        self.private.encrypted = bool(cipher)
        self._cipher = cipher

    def onGet(self, slot):
        if ((slot in ["owner", "number", "expire"]) 
            and (self.private.encrypted)):
            raise AttributeError("Data is encrypted. Call .decrypt() first.")

    def onSet(self, slot, value):
        if slot == "_cipher":
            pass
        else:
            self._cipher = None

    def isEncrypted(self):
        return self.private.encrypted

    def decrypt(self, passphrase):
        assert self.private.encrypted, "already decrypted"
        gpg = GnuPG()
        data = gpg.decrypt_string(self._cipher, passphrase)
        self.owner, self.number, self.expire = data.split("|")
        self.private.encrypted = False

    def encrypt(self, recipient=None):
        import duckbill.config
        if recipient is None:
            recipient = duckbill.config.GNUPG_RECIPIENT
        gpg = GnuPG()
        data = "|".join([self.owner, self.number, self.expire.toSQL()])
        self._cipher = gpg.encrypt_string(data, [recipient])
        return self._cipher

    def __str__(self):
        if self._cipher:
            return self._cipher
        elif (self.owner and self.number and self.expire):
            return self.encrypt()
        elif (self.owner or self.number or self.expire):
            raise AssertionError("invalid state: (only partial data)")
        else:
            return ""


