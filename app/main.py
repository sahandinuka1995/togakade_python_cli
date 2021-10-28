from getpass import getpass
import os
import json
import glob

__db_path__ = "db"
__users_folder__ = "db/users"
__item_folder__ = "db/items"


class Item:

    def goBack(self):
        val = input('Go Back ? (Y/N): ')
        if val == 'Y' or val == 'y':
            User().adminMenu()

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

        with open(__item_folder__ + '/' + code + '.db', 'w+') as item_folder:
            json.dump(_data_, item_folder)
            toast('Congratulations!', 'Item saved successfully')

    def viewItem(self):
        code = input('Enter Item Code: ')

        with open(__item_folder__ + '/' + code + '.db', 'r') as item_folder:
            item = json.load(item_folder)
            header('View Item: ' + item['code'])
            print('|  Code: ' + item['code']
                  + '\n|  Name: ' + item['name']
                  + '\n|  Price: ' + item['price']
                  + '\n|  Selling Price: ' + item['sellingPrice'] + '\n')
            self.goBack()

    def viewAllItem(self):
        header('View All Items')

        allItems = os.listdir(__item_folder__)
        print(allItems, '\n')

        self.viewItem()

    def deleteItem(self):
        header('Delete Item')

        item = input('Enter Item Code: ')
        os.remove(__item_folder__+'/'+item+'.db')
        toast('Congratulations!', 'Item deleted successfully')
        self.goBack()


class Order:

    def viewOrder(self):
        print('View Order')

    def viewAllOrders(self):
        print('View All Orders')

    def completeOrder(self):
        print('Complete Order')


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

    def customerMenu(self):
        header('Customer Menu')

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
                if data['role'] == 'admin':
                    self.adminMenu()
                elif data['role'] == 'customer':
                    self.customerMenu()

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

        def saveUser(un, data):
            if not os.path.exists(__db_path__):
                os.mkdir(__db_path__)

            if not os.path.exists(__users_folder__):
                os.mkdir(__users_folder__)

            with open(__users_folder__ + '/' + un + '.db', 'w+') as user_folder:
                json.dump(data, user_folder)
                return True

        return False


def toast(title, content):
    print('\n*** ' + title + ' ***\n' + content)


def header(title, subTitle=''):
    print("\n===========================================\n"
          " " + title + " \n"
                        "===========================================\n" + subTitle)


def main():
    os.system('color 2')
    header('Welcome to Thogakade')
    user = User()

    if not os.path.exists(__db_path__):
        os.mkdir(__db_path__)

    print('* To Login - (L)\n* To Register - (R)\n')
    loginType = input('Enter option: ')

    if loginType == 'L' or loginType == 'l':
        user.login()
    elif loginType == 'R' or loginType == 'r':
        user.register()
    else:
        print('Oops! Wrong command')


main()
