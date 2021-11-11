from getpass import getpass
import os
import json
import glob
import sys
import string
import random

__db_path__ = "db"
__users_folder__ = "db/users"
__item_folder__ = "db/items"
__order_folder__ = "db/order"


class Item:

    def addNewItem(self):
        code = input('Item Code: ')
        name = input('Item Name: ')
        price = input('Item Price: ')
        sellingPrice = input('Item Selling Price: ')

        if not os.path.exists(__item_folder__):
            os.mkdir(__item_folder__)

        _data_ = {
            "code": code,
            "name": name,
            "price": price,
            "sellingPrice": sellingPrice
        }

        try:
            with open(__item_folder__ + '/' + code + '.db', 'w+') as item_folder:
                json.dump(_data_, item_folder)
            toast('Congratulations!', 'Item saved successfully\n')
        except:
            toast('Oops!', 'Can\'t save Item\n')

        User().adminMenu()

    def viewItem(self):
        print('* To Exit - (exit)')
        code = input('Enter Item Code: ')

        if code == 'exit' or code == 'Exit' or code == 'EXIT':
            sys.exit()
        else:
            try:
                with open(__item_folder__ + '/' + code + '.db', 'r') as item_folder:
                    item = json.load(item_folder)
                header('View Item: ' + item['code'])
                print('|  Code: ' + item['code']
                      + '\n|  Name: ' + item['name']
                      + '\n|  Price: ' + item['price']
                      + '\n|  Selling Price: ' + item['sellingPrice'] + '\n')
                User().adminMenu()
            except:
                toast('Oops!', 'No item found with "' + code + '"')
                self.viewItem()

    def viewAllItem(self):
        header('View All Items')
        allItems = os.listdir(__item_folder__)
        print(allItems, '\n')
        self.viewItem()

    def deleteItem(self):
        header('Delete Item')
        print('* Go Back - (B)\n')
        item = input('Enter Item Code: ')

        if item == 'b' or item == 'B':
            User().adminMenu()
        else:
            try:
                os.remove(__item_folder__ + '/' + item + '.db')
                toast('Congratulations!', 'Item deleted successfully')
                User().adminMenu()
            except:
                print('Can\'t delete "' + item + '" or item not found')
                Item().deleteItem()

    def viewAllCustomerItem(self, type):
        header('View All Items')
        allItems = os.listdir(__item_folder__)
        print(allItems, '\n')
        User().customerMenu()


class Order:
    itemList = []

    def pickItem(self):
        header('View All Items')
        allItems = os.listdir(__item_folder__)
        print(allItems, '\n')
        print('* Go Back - (B)\n')

        code = input('Enter item name: ')
        if code == 'b' or code == 'B':
            self.saveList(self.itemList)
        else:
            try:
                with open(__item_folder__ + '/' + code + '.db', 'r') as item_folder:
                    item = json.load(item_folder)
                self.addToList(item)
            except:
                print("Can\'t pick item " + code)
                self.pickItem()

    def viewOrder(self):
        try:
            with open(__order_folder__ + '/' + getCurrentUser() + '.db', 'r') as order_folder:
                orderList = json.load(order_folder)
                for item in orderList:
                    print(item)
        except:
            print("Can\'t view orders")

    def viewAllOrders(self):
        print('View All Orders')

    def completeOrder(self):
        print('Complete Order')

    def addToList(self, item):
        self.itemList.append(item)
        toast('Success!', 'Item added to list')
        self.pickItem()

    def saveList(self, itemList):
        if not os.path.exists(__order_folder__):
            os.mkdir(__order_folder__)

        try:
            with open(__order_folder__ + '/' + getCurrentUser() + '.db', 'w+') as order_folder:
                json.dump(itemList, order_folder)
            toast('Congratulations!', 'Order saved successfully\n')
            User().customerMenu()
        except:
            print("Can\'t save Order")


class User:

    def validateInput(self, val, text):
        if val == '':
            print('Please enter ' + text)
            return ''
        else:
            return val

    def adminMenu(self):
        header('Admin Menu')
        print('-+-+-+-+-+- Item -+-+-+-+-+-\n* Add New - (NI)\n* View - (VI)\n* View All - (AI)\n* Delete - (DI)\n\n')
        print('-+-+-+-+-+- Order -+-+-+-+-+-\n* View - (VO)\n* View All - (AO)\n* Mark Complete - (CO)\n')
        print('\n* To Exit - (exit)')

        option = input('Enter option: ')
        item = Item()
        order = Order()

        if option == 'NI' or option == 'ni':
            item.addNewItem()
        elif option == 'VI' or option == 'vi':
            item.viewItem()
        elif option == 'AI' or option == 'ai':
            item.viewAllItem()
        elif option == 'DI' or option == 'di':
            item.deleteItem()
        elif option == 'VO' or option == 'vo':
            order.viewOrder()
        elif option == 'AO' or option == 'ao':
            order.viewAllOrders()
        elif option == 'CO' or option == 'co':
            order.completeOrder()
        elif option == 'exit' or option == 'Exit' or option == 'EXIT':
            exitProgram()
        else:
            print('Oops! Wrong command')
            User().adminMenu()

    def customerMenu(self):
        header('Customer Menu')
        print('-+-+-+-+-+- Item -+-+-+-+-+-\n* View All - (AI)\n\n')
        print('-+-+-+-+-+- Order -+-+-+-+-+-\n* Pick Item - (PI)\n* Remove Item - (RI)\n* View Items - (VI)\n')
        print('\n* To Exit - (exit)')

        option = input('Enter option: ')
        item = Item()
        order = Order()

        if option == 'AI' or option == 'ai':
            item.viewAllCustomerItem()
        elif option == 'PI' or option == 'pi':
            order.pickItem()
        elif option == 'VI' or option == 'vi':
            order.viewOrder()
        elif option == 'exit' or option == 'Exit' or option == 'EXIT':
            exitProgram()
        else:
            print('Oops! Wrong command')
            User().adminMenu()

    def login(self):
        username = self.validateInput(input('Username: '), 'username')
        password = self.validateInput(getpass('Password: '), 'password')

        try:
            with open(__users_folder__ + '/' + username + '.db', 'r') as user_folder:
                data = json.load(user_folder)
        except FileNotFoundError:
            toast('Oops!', '-> User not found')
        else:
            if data['password'] != password:
                toast('Oops!', 'Wrong password')
            else:
                self.setSession(data)
                if data['role'] == 'admin':
                    self.adminMenu()
                elif data['role'] == 'customer':
                    self.customerMenu()

    def setSession(self, user):
        with open('db/session.db', 'w+') as db_folder:
            json.dump(user, db_folder)

    def register(self):
        header('New user registration', 'Please fill all details')
        username = self.validateInput(input('Username: '), 'username')
        password = self.validateInput(getpass('Password: '), 'password')
        role = self.validateInput(input('Role: '), 'role')

        _data_ = {
            "username": username,
            "password": password,
            "role": role
        }

        if self.saveUser(username, _data_):
            toast('Congratulations!', '-> User account successfully created')
            main()
        else:
            toast('Oops!', '-> Something went wrong')

    def saveUser(self, un, data):
        if not os.path.exists(__db_path__):
            os.mkdir(__db_path__)

        if not os.path.exists(__users_folder__):
            os.mkdir(__users_folder__)

        try:
            with open(__users_folder__ + '/' + un + '.db', 'w+') as user_folder:
                json.dump(data, user_folder)
            return True
        except:
            toast('Oops!', 'Something went wrong')

        return False


def toast(title, content):
    print('\n*** ' + title + ' ***\n' + content + '\n')


def header(title, subTitle=''):
    print("\n===========================================\n"
          " " + title + " \n"
                        "===========================================\n" + subTitle)


def getCurrentUser():
    try:
        with open('db/session.db', 'r') as session:
            session = json.load(session)
            return session["username"]
    except:
        print('Something went wrong')


def main():
    os.system('color 2')
    header('Welcome to Thogakade')
    user = User()

    if not os.path.exists(__db_path__):
        os.mkdir(__db_path__)

    print('* To Login - (L)\n* To Register - (R)\n* To Exit - (exit)\n')
    loginType = input('Enter option: ')

    if loginType == 'L' or loginType == 'l':
        user.login()
    elif loginType == 'R' or loginType == 'r':
        user.register()
    elif loginType == 'exit' or loginType == 'Exit' or loginType == 'EXIT':
        exitProgram()
    else:
        print('Oops! Wrong command')
        main()


def exitProgram():
    sys.exit()


main()
