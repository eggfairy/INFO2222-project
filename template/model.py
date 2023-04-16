'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import json
import string
from hashlib import md5
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import ssl

# Initialise our views, all arguments are defaults for the template
page_view = view.View()


login = False  # By default assume bad creds
login_status = {}
#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index(username):
    '''
        index
        Returns the view for the index
    '''
    global login_status
    if username == None or username not in login_status:
        return page_view("index")
    if login_status[username]:
        return page_view("index", header='header_in', user=username)
    else:
        return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login", header='header_no_pic')

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    
    err_str = "Incorrect Username" #error massage by default is incorrect username
    login = False # By default assume bad creds
    with open('info.json', 'r') as f:
        data = json.load(f)

        for row in data['user_info']:
            if row['username'] == username: 
                pwd_hash = hash_calculator(password, row['password'][1])[0]
                if pwd_hash == row['password'][0]: #both correct
                    login = True
                    break

            if row['username'] == username:  #incorrect password
                err_str = "Incorrect Password"
            
    global login_status
    
    #if none of these if statements are executed, invalid username
    if login: 
        login_status[username] = True
        return page_view("valid", user=username,header='header_in_no_pic')
    else:
        return page_view("invalid", reason=err_str, header='header_no_pic')


#-----------------------------------------------------------------------------
# Friends
#-----------------------------------------------------------------------------

def friends(user):
    global login_status
    if user not in login_status or not login_status[user]:
        return page_view("login", header='header_no_pic')
    
    friends = []
    with open('info.json', 'r') as f:
        data = json.load(f)
        for row in data['user_info']:
            if row['username'] == user:
                friends = row['friends'] #get firends of current user
                break

    html_form = ''
    for f in friends:
        html_form += f'<button name="user" type="submit" value="{user},{f}">{f}</button>' #display user's friends as buttons
    return page_view("friend_list", header='header_in_no_pic', friends=html_form, user=user)


#-----------------------------------------------------------------------------
# Chat page
#-----------------------------------------------------------------------------
def chat(username, recipient):
    global login_status
    if username not in login_status or not login_status[username]:
        return page_view("login", header='header_no_pic')
    
    records = ''
    with open('chat_records.json', 'r') as f:
        data = json.load(f)
        for row in data['chat_records']:
            if row['username'] == username:
                records = row['records'][recipient] #display the chat records between specific users
    
    return page_view("chat", header='header_chatting', user=username, recipient=recipient, msgs=records)

#-----------------------------------------------------------------------------
# send message
#-----------------------------------------------------------------------------

def send_msg(msg, username, recipient):
    global login_status
    if username not in login_status or not login_status[username]:
        return page_view("login", header='header_no_pic')
    
    decrypt_records = ''
    data = None

    public = rsa.PublicKey._load_pkcs1_pem(open("key/{}_public.pem".format(username), "rb").read())
    encrypt_records = rsa.encrypt(bytes(msg, "utf-8"), public)
    with open("data/encrypted.data", "wb") as f:
        f.write(encrypt_records)
    private = rsa.PrivateKey._load_pkcs1_pem(open("key/{}_private.pem".format(username), 'rb').read())
    encrypted = ""
    with open("data/encrypted.data", "rb") as f:
        encrypted = f.read()
    decrypt_records = rsa.decrypt(encrypted, private)


    with open('chat_records.json', 'r') as f:
        data = json.load(f)
        for i in range(len(data['chat_records'])):
            if data['chat_records'][i]['username'] == username:
                records = data['chat_records'][i]['records'][recipient]

                if msg == None or msg == '': #if msg is null, display the same page
                    return page_view('chat', header='header_chatting', user=username, recipient=recipient, msgs=decrypt_records)

                decrypt_records += f'<div class="outgoing-chats">\n<div class="outgoing-msg">\n<div class="outgoing-chats-msg">\n<p class="received-msg">{msg}</p>\n</div>\n</div>\n</div>'

                #append latest message to records
                data['chat_records'][i]['records'][recipient] = encrypt_records
            
            if data['chat_records'][i]['username'] == recipient:
                records = b''.join(data['chat_records'][i]['records']) ###############
                decrypted_blocks = []
                for offset in range(0, len(records), 256):
                    block = records[offset:offset + 256]

                records += b'<div class="received-chats">\n<div class="received-msg">\n<div class="received-msg-inbox">\n<p class="single-msg">{msg}</p>\n</div>\n</div>\n</div>'
                data['chat_records'][i]['records'][username] = records
                #append current message to records

    with open('chat_records.json', 'w') as f:
        json.dump(data, f, indent=2) #update latest records to the file
    return page_view('chat', header='header_chatting', user=username, recipient=recipient, msgs=decrypt_records)



#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about(username):
    '''
        about
        Returns the view for the about page
    '''
    global login_status
    if username == None or username not in login_status:
        return page_view("index")
    if login_status[username]:
        return page_view("about", garble=about_garble(), header='header_in', user=username)
    else:
        return page_view("about", garble=about_garble())

#-----------------------------------------------------------------------------
# Sign up
#-----------------------------------------------------------------------------

def show_sign_up_page():
    return page_view("sign_up", header='header_no_pic')

#-----------------------------------------------------------------------------
# Sign up check
#-----------------------------------------------------------------------------

def sign_up_check(username, password, password_2):
    if password != password_2:
        return page_view("invalid", reason="Two passwords are different", header='header_no_pic')
    
    data = None
    with open('info.json', 'r') as f:
        data = json.load(f)

        for row in data['user_info']:
            if row['username'] == username:
                return page_view("invalid", reason="Username already exists", header='header_no_pic')
            
        salt = salt_generator()
        Password = hash_calculator(password,salt) ###
        get_key(username)
        info = {"username" : username, "password" : Password, "friends" : []}
        data['user_info'].append(info) #add new user info the file

    with open('info.json', 'w') as f:
        json.dump(data, f, indent=2)

    records_info = {"username" : username, "records" : {}}

    with open('chat_records.json', 'r') as f:
        data = json.load(f)
        data['chat_records'].append(records_info)

    with open('chat_records.json', 'w') as f:
        json.dump(data, f, indent=2)

    return page_view("sign_up_valid", header='header_no_pic')

#-----------------------------------------------------------------------------
# logout
#-----------------------------------------------------------------------------

def logout(username):
    
    global login_status
    login_status[username] = False
    return page_view("index")

#-----------------------------------------------------------------------------
# Show add friends page
#-----------------------------------------------------------------------------

def show_add_friends(username):
    global login_status
    if username not in login_status or not login_status[username]:
        return page_view("login", header='header_no_pic')
    
    return page_view('add_friends', header='header_in_no_pic', user=username)

def add_friends_check(username, recipient):
    data = None
    friend_exist = False #by default user do not exist
    if username == recipient:
        return page_view('invalid', header='header_in_no_pic', user=username, reason='It is user yourself!')

    with open('info.json', 'r') as f:
        data = json.load(f)

        for row in data['user_info']:
            if row['username'] == recipient: 
                friend_exist = True
                break
            if row['username'] == username:
                if recipient in row['friends']: #if the recipient is already user's friend
                    return page_view('invalid', header='header_in_no_pic', user=username, reason='Username is your friend')

        if not friend_exist: #if the recipient do not exist
            return page_view('invalid', header='header_in_no_pic', user=username, reason='Username do not exist')

        for i in range(len(data['user_info'])): #no error
            if data['user_info'][i]['username'] == username:
                data['user_info'][i]['friends'].append(recipient)

            if data['user_info'][i]['username'] == recipient:
                data['user_info'][i]['friends'].append(username)

    with open('info.json', 'w') as f:
        json.dump(data, f, indent=2)

    with open('chat_records.json', 'r') as f:
        data = json.load(f)

        for i in range(len(data['chat_records'])):
            if data['chat_records'][i]['username'] == username: #create an empty chat records on both sides
                data['chat_records'][i]['records'][recipient] = ""
            if data['chat_records'][i]['username'] == recipient:
                data['chat_records'][i]['records'][username] = ""
    
    with open('chat_records.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    return page_view('add_valid', header='header_in_no_pic', user=username)

# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)


def salt_generator():
    random_str = " "
    base_str = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789"
    i = 0
    ls1 = []

    while i <= 49:
        ls1.append(random.choice(base_str))
        i += 1
    random_str = "".join(ls1)
    return random_str

def hash_calculator(msg,salt):
    obj = md5(salt.encode("utf-8"))
    obj.update(msg.encode("utf-8"))

    bs = obj.hexdigest()
    ls1 = [bs,salt]
    return ls1

def get_key(username):
    key_name = username
    (public, private) = rsa.newkeys(512)
    with open("key/{}_public.pem".format(key_name), "wb") as f:
        f.write(public._save_pkcs1_pem())

    with open("key/{}_private.pem".format(key_name), "wb") as f:
        f.write(private._save_pkcs1_pem())
