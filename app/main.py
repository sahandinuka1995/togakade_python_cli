from getpass import getpass
import os
import json

__db_path__ = "db"
__users_folder__ = "db/users"


def login():
    print('Login def')


def register():
    header('New user registration', 'Please fill all details')
    username = validateInput(input('Username: '), 'username')
    password = validateInput(getpass('Password: '), 'password')
    role = validateInput(input('Role: '), 'role')

    _data_ = {
        "username": username,
        "password": password,
        "role": role
    }

    if saveUser(username, _data_):
        toast('Congratulations!', '-> User account successfully created')
    else:
        toast('Oops!', '-> Something went wrong')


def toast(title, content):
    print('\n*** ' + title + ' ***\n' + content)


def saveUser(username, data):
    if not os.path.exists(__db_path__):
        os.mkdir(__db_path__)

    if not os.path.exists(__users_folder__):
        os.mkdir(__users_folder__)

    with open(__users_folder__ + '/' + username + '.db', 'w+') as user_folder:
        json.dump(data, user_folder)
        return True

    return False


def validateInput(val, text):
    if val == '':
        print('Please enter ' + text)
        register()
        return ''
    else:
        return val


def header(title, subTitle=''):
    print("\n===========================================\n"
          " " + title + " \n"
                        "===========================================\n" + subTitle + '\n')


def main():
    os.system('color 2')
    header('Welcome to Thogakade')
    print('* To Login - (L)\n* To Register - (R)\n')
    loginType = input('Enter option: ')

    if loginType == 'L':
        login()
    elif loginType == 'R':
        register()
    else:
        print('Oops! Wrong command')


main()

# username = input('Enter username: ')
# password = getpass('Enter password: ')
