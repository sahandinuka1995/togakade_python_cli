from getpass import getpass
import os
import json

__db_path__ = "db"
__users_folder__ = "db/users"


class Item:

    def addNewItem(self):
        print('Add New Item')

    def viewItem(self):
        print('View Item')

    def viewAllItem(self):
        print('View All Item')

    def deleteItem(self):
        print('Delete Item')


class Order:

    def viewOrder(self):
        print('View Order')

    def viewAllOrders(self):
        print('View All Orders')

    def completeOrder(self):
        print('Complete Order')


def adminMenu():
    header('Admin Menu')
    print('-+-+-+-+-+- Item -+-+-+-+-+-\n* Add New - (NI)\n* View - (VI)\n* View All - (AI)\n* Delete - (DI)\n\n')
    print('-+-+-+-+-+- Order -+-+-+-+-+-\n* View - (VO)\n* View All - (AO)\n* Mark Complete - (CO)\n')

    option = input('Enter option: ')
    item = Item()
    order = Order()

    if option == 'NI':
        item.addNewItem()
    elif option == 'VI':
        item.viewItem()
    elif option == 'AI':
        item.viewAllItem()
    elif option == 'DI':
        item.deleteItem()
    elif option == 'VO':
        order.viewOrder()
    elif option == 'AO':
        order.viewAllOrders()
    elif option == 'CO':
        order.completeOrder()


def customerMenu():
    header('Customer Menu')


def login():
    username = validateInput(input('Username: '), 'username')
    password = validateInput(getpass('Password: '), 'password')

    try:
        with open(__users_folder__ + '/' + username + '.db', 'r') as user_folder:
            data = json.load(user_folder)
    except FileNotFoundError:
        toast('Oops!', '-> User not found')
    else:
        if data['password'] != password:
            toast('Oops!', 'Wrong password')
        else:
            if data['role'] == 'admin':
                adminMenu()
            elif data['role'] == 'customer':
                customerMenu()


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
        main()
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
