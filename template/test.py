
import rsa
# url = 'https://httpbin.org/cookies'

# requestsJar = requests.cookies.RequestsCookieJar()
# requestsJar.set('username', 'Anna', domain='httpbin.org', path='/cookies')
# requestsJar.set('username', 'Bella', domain='httpbin.org', path='/Bella')
# r3 = requests.get(url, cookies=requestsJar)
# print(r3.text)

# with open('chat_records.json', 'r') as f:
#         data = json.load(f)
#         print(data['chat_records'][0]['user'])


#salt = model.salt_generator()
#pwd_info = model.hash_calculator('test1', salt)
#print(pwd_info)

#pwd_info = model.hash_calculator('test1', salt)
#print(pwd_info)


key_name = "demo"
(public,private) = rsa.newkeys(512)
with open("key/{}_public.pem".format(key_name),"wb") as f:
    f.write(public._save_pkcs1_pem())

with open("key/{}_private.pem".format(key_name),"wb") as f:
    f.write(private._save_pkcs1_pem())

plaintext = "jkjkjkjkjkjkjk"
public = rsa.PublicKey._load_pkcs1_pem(open("key/{}_public.pem".format(key_name), "rb").read())
encrypted = rsa.encrypt(bytes(plaintext,"utf-8"), public)
with open("data/encrypted.data", "wb") as f:
    f.write(encrypted)

private = rsa.PrivateKey._load_pkcs1_pem(open("key/{}_private.pem".format(key_name),'rb').read())
encrypted = ""
with open("data/encrypted.data", "rb") as f:
    encrypted = f.read()
decrypted = rsa.decrypt(encrypted, private)
print(decrypted)

