from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
import mysql.connector
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
import threading
from plyer import notification
import yagmail


database = mysql.connector.connect(host='localhost', user='root', password='root', database='data') #set name of database of yours

cursor = database.cursor()

root = Tk()

root.geometry('500x367')

root.resizable(False, False)

root.iconbitmap('main.ico')

root.title('Watch List')

bg= Canvas(root)

bgImage= ImageTk.PhotoImage(Image.open('cart.jpg'))

bg.create_image(0, 0, anchor=NW, image=bgImage)

bg.place(x=0, y=0, relwidth=1, relheight=1)

theme= ThemedStyle(root).set_theme('aquativo')

style = ttk.Style().configure('W.TButton', font=('Helvetica', 10, 'bold'),  background='grey', bd=10, focuscolor= root.cget('background'))

menu_style= ttk.Style().configure('TMenubutton', font=('Helvetica', 10, 'bold'), background='grey', bd=10)


def P_List():

    root1 = Toplevel()

    root1.title('Product List')

    root1.iconbitmap('add.ico')

    root1.configure(bg='lightcyan2')

    cursor.execute('SHOW TABLES')

    product_data = cursor.fetchall()

    product_list = []

    for x in range(len(product_data)):

        product_name=product_data[x][0]
        product_list.append(product_name)

    product_link_lists=[]

    for name in product_list:

        cursor.execute('SELECT Product_Link_Data FROM {table}'.format(table=name))
        product_link_lists.append(cursor.fetchone()[0])

    Dict = dict(zip(product_list , product_link_lists))

    def Get_Info(event=None):

        Dict.update({None: None})

        link = Dict[var.get() if bool(var.get()) else None]
        try:
            source0 = requests.get(link, headers={'User-agent': 'Chrome'})

            source = source0.text

            data = BeautifulSoup(source, 'lxml')

            if 'amazon.in' in link:

                title0 = data.find('span', class_='a-size-large product-title-word-break').text

                title = title0.lstrip('\n').rstrip('\n').replace('()', '')

                price0 = data.find('span', class_='a-size-medium a-color-price priceBlockBuyingPriceString').text

                price = int(price0[2:].replace(',', '').replace('.', '')) / 100

                try:

                    availability0 = data.find('span', class_='a-size-medium a-color-success').text

                    availability = availability0.lstrip('\n').rstrip('\n')
                    
                except:

                    availability0 = data.find('span', class_='a-size-medium a-color-state').text

                    availability = availability0.lstrip('\n').rstrip('\n')

            if 'flipkart.com' in link:

                price0 = data.find('div', class_='_1vC4OE').text

                price = price0[1:].replace(',', '')


                title0 = data.find('span', class_='_35KyD6').text

                title = title0.replace('\xa0', '')

                availability = 'In stock.'

            info_list = [title , price , availability]

            for i in range(3):
                label = ttk.Label(root1 , text=info_list[i] , style='W.TButton')

                label.grid(row=i+3 , column=0, pady=5)
        except:
            if requests.status_codes != 200:

                messagebox.showerror('Error', 'Url Does Not Exist OR Product Is Currently Unavailable.')


    var=StringVar()

    menu= ttk.Combobox(root1, textvariable=var)

    menu['values']=product_list

    menu.grid(row=0 , column=0, ipadx=5, pady=10, padx=5)

    button_enter = ttk.Button(root1 , text='Enter' , command=Get_Info, style='W.TButton')

    root1.bind('<Return>', Get_Info)

    button_enter.grid(row=2 , column=0, pady=10)
def AddItem():
    root2 = Toplevel()

    root2.configure(bg='lightcyan2')

    root2.iconbitmap('add.ico')

    root2.title('Add Product')

    label = ttk.Label(root2, text='Enter Product Link:-', style='W.TButton')

    label1 = ttk.Label(root2, text='Enter Product Name:-', style='W.TButton')

    label.grid(row=0 , column=0, ipadx=5, ipady=5, pady=10, padx=5)

    label1.grid(row=0, column=4, ipadx=5, ipady=5, pady=10, padx=5)

    entry = ttk.Entry(root2, )

    entry.grid(row=1, column=0, columnspan=4, sticky='W', ipadx=10, ipady=5, padx=5)

    entry1 = ttk.Entry(root2, )

    entry1.grid(row=1, column=4, columnspan=4, sticky='W', ipadx=15, ipady=5, padx=5)
    def ItemLink(event=None):
        link0 = entry.get()

        link = f'"{link0}"'

        pname0 = entry1.get()

        pname = pname0.replace(' ', '')

        if bool(link0):
            try:
                source0 = requests.get(link0, headers={'User-agent': 'Chrome'})

                source = source0.text

                data = BeautifulSoup(source, 'lxml')

                if 'amazon.in' in link0:

                    price0 = data.find('span', class_='a-size-medium a-color-price priceBlockBuyingPriceString').text

                    price = int(price0[2:].replace(',', '').replace('.', '')) / 100

                    cursor.execute(
                        'CREATE TABLE {tname} (Product_Link_Data VARCHAR(1000),Price INT)'.format(tname=pname))

                    cursor.execute(
                        'INSERT INTO {tname} VALUES({plink},{price})'.format(tname=pname, plink=link, price=price))

                    database.commit()

                    messagebox.showinfo('Saved', 'Product Saved Successfully!')

                if 'flipkart.com' in link0:

                    price0 = data.find('div', class_='_1vC4OE').text

                    price = int(price0[1:].replace(',', ''))

                    cursor.execute('CREATE TABLE {tname} (Product_Link_Data VARCHAR(1000),Price INT)'.format(tname=pname))

                    cursor.execute('INSERT INTO {tname} VALUES({plink},{price})'.format(tname=pname , plink=link, price=price))

                    database.commit()

                    messagebox.showinfo('Saved', 'Product Saved Successfully!')
            except:

                if requests.status_codes!=200:
                    messagebox.showerror('Error', 'Url Does Not Exist Or Not Reachable At The Moment.')

                if not bool(pname0):
                    messagebox.showwarning('Warning', 'Enter Product Name!')


    button_save= ttk.Button(root2, text='Save', command=ItemLink, style='W.TButton')

    button_save.grid(row=2, column=3, ipadx=5, ipady=5, pady=20)

    root2.bind('<Return>' , ItemLink)

def Remove():
    try:
        root3= Toplevel()

        root3.configure(bg='lightcyan2')

        root3.title('Remove Product')

        root3.iconbitmap('remove.ico')

        cursor.execute('SHOW TABLES')

        product_data = cursor.fetchall()

        product_list = []

        for x in range(len(product_data)):

            product_name=product_data[x][0]
            product_list.append(product_name)

        def Del(event=None):

            if bool(var.get()):

                if var.get()!='Remove All Products':

                    warn = messagebox.askquestion('Removing', f'Do you want to remove {var.get()}?' )

                    if warn=='yes':

                        cursor.execute('DROP TABLE {table}'.format(table=var.get()))

                        messagebox.showinfo('Removed', 'Removed Successfully!')

                if var.get() == 'Remove All Products':

                    sure = messagebox.askquestion('Remove All Products?', 'All Products Will be Removed. Are you sure?')

                    if sure == 'yes':

                        for table in product_list:

                            if table!= 'Remove All Products':

                                cursor.execute(f'DROP TABLE {table}')

                        messagebox.showinfo('Removed', 'Removed Successfully!')
    except:

        messagebox.showinfo('No Product Found!', 'No Product Found!')

    var = StringVar()

    menu = ttk.Combobox(root3, textvariable=var)

    product_list.append('Remove All Products') if bool(product_list) else None

    menu['values'] = product_list

    menu.grid(row=0, column=0, ipadx=5, pady=10, padx=5)

    button_enter = ttk.Button(root3, text='Enter', command=Del , style='W.TButton')

    root3.bind('<Return>', Del)

    button_enter.grid(row=1, column=0, pady=10)

button_add= ttk.Button(root, text='Add Product', command=AddItem, style='W.TButton')

button_add.pack(pady=8 , ipadx=10, ipady=5)

button_products= ttk.Button(root , text='Product List' , command=P_List, style='W.TButton')

button_products.pack(pady=8, ipadx=10 , ipady=5)

button_remove = ttk.Button(root , text='Delete Product' , command=Remove, style='W.TButton')

button_remove.pack(pady=8 , ipadx=2, ipady=5)

def Price():
    try:

        cursor.execute('SHOW TABLES')

        product_data = cursor.fetchall()

        product_list = []

        for x in range(len(product_data)):
            product_name = product_data[x][0]
            product_list.append(product_name)

        product_Price_lists = []

        for name in product_list:
            cursor.execute('SELECT Price FROM {table}'.format(table=name))
            product_Price_lists.append(cursor.fetchone()[0])

        Dict = dict(zip(product_list, product_Price_lists))

        product_link_lists = []

        for name in product_list:
            cursor.execute('SELECT Product_Link_Data FROM {table}'.format(table=name))
            product_link_lists.append(cursor.fetchone()[0])

        for link in product_link_lists:

            source0 = requests.get(link, headers={'User-agent': 'Chrome'})

            source = source0.text

            data = BeautifulSoup(source, 'lxml')

            if 'amazon.in' in link:

                price0 = data.find('span', class_='a-size-medium a-color-price priceBlockBuyingPriceString').text

                price = int(price0[2:].replace(',', '').replace('.', '')) / 100

            if 'flipkart.com' in link:

                price0 = data.find('div', class_='_1vC4OE').text

                price = int(price0[1:].replace(',', ''))

            for product in Dict:

                if Dict[product] != price:

                    notification.notify(title='Price Changed!',
                                        message=f'Price of {product} changed ,Go Check It Out!.', app_icon='main.ico',
                                        timeout=10)

                    '''sender = "notifier@gmail.com"  #MAKE A TEMP GMAIL NOTIFIER ACCOUNT AND TURN "ALLOW LESS SECURE APP-OFF"

                    receiver = "your_mail_address" #ON WHICH YOU WANT TO GET NOTIFIED

                    mail = yagmail.SMTP(user = sender, password = "Your password")

                    mail.send (to = receiver, content = f'Price of {product} changed ,Go Check It Out!.', subject = 'Price Changed!')'''

                    cursor.execute(f'UPDATE {product} SET Price={price}')

                    database.commit()



                else:
                    return
    except:
        return

p1 = threading.Thread(target=Price)
p1.start()
root.mainloop()
