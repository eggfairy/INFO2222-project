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
import rsa

# Initialise our views, all arguments are defaults for the template
page_view = view.View()


login = False  # By default assume bad creds
login_status = {}
msgs = ''
#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index(username):
    '''
        index
        Returns the view for the index
    '''
    global login_status, msgs
    msgs = ''
    if username == None:
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
            if row['username'] == username and row['password'] == password: #both correct
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
    global msgs
    msgs = ''
    friends = []
    with open('info.json', 'r') as f:
        data = json.load(f)
        for row in data['user_info']:
            if row['username'] == user:
                friends = row['friends']
                break

    html_form = ''
    for f in friends:
        html_form += f'<button name="user" type="submit" value="{user} {f}">{f}</button>'
    return page_view("friend_list", header='header_in_no_pic', friends=html_form, user=user)


#-----------------------------------------------------------------------------
# Chat page
#-----------------------------------------------------------------------------
def chat(username, recipient):
    records = ''
    with open('chat_records.json', 'r') as f:
        data = json.load(f)
        for row in data['chat_records']:
            if row['username'] == username:
                records = row['records'][recipient]
    
    return page_view("chat", header='header_chatting', user=username, recipient=recipient, msgs=records)

#-----------------------------------------------------------------------------
# send message
#-----------------------------------------------------------------------------
def send_msg(msg, username, recipient):
    records = ''
    data = None
    with open('chat_records.json', 'r') as f:
        data = json.load(f)
        for i in range(len(data['chat_records'])):
            if data['chat_records'][i]['username'] == username:
                records = data['chat_records'][i]['records'][recipient]
                if msg == None or msg == '':
                    return page_view('chat', header='header_chatting', user=username, recipient=recipient, msgs=records)

                records += f'<div class="outgoing-chats">\n<div class="outgoing-msg">\n<div class="outgoing-chats-msg">\n<p class="received-msg">{msg}</p>\n</div>\n</div>\n</div>'
                data['chat_records'][i]['records'][recipient] = records
            
            if data['chat_records'][i]['username'] == recipient:
                data['chat_records'][i]['records'][username] += f'<div class="received-chats">\n<div class="received-msg">\n<div class="received-msg-inbox">\n<p class="single-msg">{msg}</p>\n</div>\n</div>\n</div>'


        # for row in data['chat_records']:
        #     if row['username'] == username:
        #         records = row['records'][recipient]
        #     if msg != None:
        #         records += f'<div class="outgoing-chats">\n<div class="outgoing-msg">\n<div class="outgoing-chats-msg">\n<p class="received-msg">{msg}</p>\n</div>\n</div>\n</div>'

    with open('chat_records.json', 'w') as f:
        json.dump(data, f, indent=2)
    return page_view('chat', header='header_chatting', user=username, recipient=recipient, msgs=records)


#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about(username):
    '''
        about
        Returns the view for the about page
    '''
    global login_status
    if username == None:
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
        Password = hash_calculator(password,salt)[0]
        info = {"username" : username, "password" : Password, "friends" : []}
        data['user_info'].append(info)

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
    
    global login_status, msgs
    msgs = ''
    login_status[username] = False
    return page_view("index")

#-----------------------------------------------------------------------------
# Show add friends page
#-----------------------------------------------------------------------------

def show_add_friends(username):
    return page_view('add_friends', header='header_in_no_pic', user=username)

def add_friends_check(username, recipient):
    data = None
    friend_exist = False
    if username == recipient:
        return page_view('invalid', header='header_in_no_pic', user=username, reason='It is user yourself!')

    with open('info.json', 'r') as f:
        data = json.load(f)

        for row in data['user_info']:
            if row['username'] == recipient:
                friend_exist = True
                break
            if row['username'] == username:
                if recipient in row['friends']:
                    return page_view('invalid', header='header_in_no_pic', user=username, reason='Username is your friend')

        if not friend_exist:
            return page_view('invalid', header='header_in_no_pic', user=username, reason='Username do not exist')

        for i in range(len(data['user_info'])):
            if data['user_info'][i]['username'] == username:
                data['user_info'][i]['friends'].append(recipient)

            if data['user_info'][i]['username'] == recipient:
                data['user_info'][i]['friends'].append(username)

    with open('info.json', 'w') as f:
        json.dump(data, f, indent=2)

    with open('chat_records.json', 'r') as f:
        data = json.load(f)

        for i in range(len(data['chat_records'])):
            if data['chat_records'][i]['username'] == username:
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

#encrypt the str with the public key, could use to encrypt the message and store in the chat_records
def rsaEncrypt(str):
    (public_key, private_key) = rsa.newkeys(512)
    message = str.encode("utf-8")
    encrypt = rsa.encrypt(message, public_key)
    return [encrypt, private_key]

#decrypt the str with private key, could use to encrypt the message and send to the reciever
def rsaDecrypt(str, pk):
    content = rsa.decrypt(str, pk)
    con = content.decode("utf-8")
    return con
