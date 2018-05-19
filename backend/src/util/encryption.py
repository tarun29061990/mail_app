import base64
from Crypto import Random
from Crypto.Cipher import AES

# AES/CBC/PKCS5Padding encrypt
class EncryptionUtil(object):
    BLOCK_SIZE = 16

    @staticmethod
    def __pad(s):
        return s + (EncryptionUtil.BLOCK_SIZE - len(s) % EncryptionUtil.BLOCK_SIZE) * chr(
            EncryptionUtil.BLOCK_SIZE - len(s) % EncryptionUtil.BLOCK_SIZE)

    @staticmethod
    def __unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    @staticmethod
    def aes_encrypt(raw, key, replace_slashes=False):
        raw = EncryptionUtil.__pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        output = base64.b64encode(iv + cipher.encrypt(raw))
        if replace_slashes:
            output = output.replace(b'+', b'-').replace(b'/', b'_')
        return output

    @staticmethod
    def aes_decrypt(enc, key, replace_slashes=False):
        if replace_slashes:
            enc = enc.replace('-', '+').replace('_', '/')
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return EncryptionUtil.__unpad(cipher.decrypt(enc[16:]))
