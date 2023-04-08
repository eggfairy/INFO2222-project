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
    return page_view("chat", header='header_chatting', user=username, recipient=recipient, msgs='')

#-----------------------------------------------------------------------------
# send message
#-----------------------------------------------------------------------------
def send_msg(msg, username, recipient):
    global msgs
    if msg != None:
        msgs += f'<div class="outgoing-chats">\n<div class="outgoing-msg">\n<div class="outgoing-chats-msg">\n<p class="received-msg">{msg}</p>\n</div>\n</div>\n</div>'
    return page_view('chat', header='header_chatting', user=username, recipient=recipient, msgs=msgs)


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

def logout(username):
    
    global login_status, msgs
    msgs = ''
    login_status[username] = False
    return page_view("index")


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
