
import model
import rsa

public = ''
private = ''


def RSA_encryption(txt, key): #seperate plaintext into several chuncks
    result = []
    for n in range(0,len(txt),245):
        chuncks = txt[n:n+245]
        result.append( rsa.encrypt(chuncks.encode(), key) )
    return b''.join(result)

def RSA_decryption(content, key):
    result = []
    for n in range(0,len(content),256):
        chuncks = content[n:n+256]
        result.append( rsa.decrypt(chuncks, key).decode() )
    return ''.join(result)

with open('key/demo_public.pem', 'rb') as f:
    public = f.read()

with open('key/demo_private.pem', 'rb') as f:
    private = f.read()

public = rsa.PublicKey._load_pkcs1_pem(public)
private = rsa.PrivateKey._load_pkcs1_pem(private)

plaintext = 'asdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgsdfbergwfsdvsdfgrdasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdgasdfgthjyhregfsdverdscverdg'

encrypt = RSA_encryption(plaintext, public)
decrypt = RSA_decryption(encrypt, private)
print(plaintext == decrypt)