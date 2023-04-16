import rsa
def encryptInput(username, msg):

    public = rsa.PublicKey._load_pkcs1_pem(open("key/{}_public.pem".format(username), "rb").read())
    encrypted = rsa.encrypt(bytes(msg, "utf-8"), public)
    with open("data/encrypted.data", "wb") as f:
        f.write(encrypted)

    return encrypted
