#if we need to generate a real pulic and private key, we can use this part to encrypt
import Crypto.PublicKey.RSA
import Crypto.Cipher.PKCS1_v1_5
import Crypto.Random
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash

y = b"abcdefg1234567"

with open("b.pem", "rb") as x:
    b = x.read()
    cipher_public = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(b))
    cipher_text = cipher_public.encrypt(y)
with open("a.pem", "rb") as x:
    a = x.read()
    cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
    text = cipher_private.decrypt(cipher_text, Crypto.Random.new().read)  # 使用私钥进行解密
assert text == y  # 断言验证

with open("c.pem", "rb") as x:
    c = x.read()
    c_rsa = Crypto.PublicKey.RSA.importKey(c)
    signer = Crypto.Signature.PKCS1_v1_5.new(c_rsa)
    msg_hash = Crypto.Hash.SHA256.new()
    msg_hash.update(y)
    sign = signer.sign(msg_hash)
with open("d.pem", "rb") as x:
    d = x.read()
    d_rsa = Crypto.PublicKey.RSA.importKey(d)
    verifer = Crypto.Signature.PKCS1_v1_5.new(d_rsa)
    msg_hash = Crypto.Hash.SHA256.new()
    msg_hash.update(y)
    verify = verifer.verify(msg_hash, sign)
    print(verify)