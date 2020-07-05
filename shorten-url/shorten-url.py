# URL Shorten Tool
# Technical Details:
# The main goal of this app is to shorten the URL and when the user visits the shorten URL,
# he/she must be redirected to the original URL.
# To generate the characters for shortened URL you can use the combination of the random and string modules.
# You need to save the original and shortened URLs in the database,
# so whenever a user visits the shortened URL (days, months, or even years after) the application checks the database,
# if the URL exists, it redirects to the original, or else it redirects to a 404 page.

# Additional Challenge: You can make this tool more user friendly by adding the feature of custom URL option
# for user. It will be easier for a user to remember the custom URL generated by themselves.

import random
import string
import sqlite3
import webbrowser

conn = sqlite3.connect('smallify.sqlite')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS smalify(
    to_short TEXT UNIQUE,
    original TEXT UNIQUE
    )''')


def make_it_short():
    new_url = 'www.small.fy/'
    length = ''
    try:
        length = int(input('Enter the length of the address URL or (type 0 for Default) - '))
    except TypeError:
        print('Try Again Please...')
        exit(0)
    if length == 0:
        print('Set Length to DEFAULT - 7')
        length = 7
    elif 1 <= length <= 4:
        print('Minimum 5 Characters long Required.\nSet Length to DEFAULT - 7')
        length = 7
    elif length >= 15:
        print('C\'mon, you wanted to reduce the Length of the URL')
        print('Set Length to DEFAULT - 7')
        length = 7
    new_url += generate_random(length)
    return new_url


def generate_random(length):
    all_chars = string.ascii_letters + string.digits
    address = ''
    for value in range(length):
        address += random.choice(all_chars)
    return address


def open_web(link_search):
    found = None
    cur.execute('SELECT * FROM smalify')
    for short_check in cur.fetchall():
        if short_check[0] == link_search:
            found = short_check[1]
    if found is None:
        print('Not Registered in DataBase...\nOpening Google Instead.')
        found = 'https://www.google.com/'
    return found


option = None
try:
    option = int(input('Choose -\n1. Convert your URL\n2. Open Shortened URL in Browser\nEnter - '))
except TypeError:
    print('Enter Only Numbers...!!!')
    exit(-1)
if option == 1:
    link = input('\nEnter URL to Shorten - ')
    short = make_it_short()
    print('Shortened URL -> ', short)
    cur.execute('INSERT OR IGNORE INTO smalify(to_short, original) VALUES (?, ?)', (short, link))
    conn.commit()
link = input('\nEnter short-URL you Received to OPEN in Browser - ')
result = open_web(link)
print('Redirecting to -> ', result)
conn.commit()
print('Opening the WebSite....')
webbrowser.open_new_tab(result)
print('THAT\'S A SUCCESS..CELEBRATE.')