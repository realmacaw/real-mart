#==================imports===================
import sqlite3
import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
#============================================



root = Tk()

root.geometry("1366x768")
root.title("Retail Manager")


user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()
new_user = StringVar()
new_passwd = StringVar()


cust_name = StringVar()
cust_num = StringVar()
cust_new_bill = StringVar()
cust_search_bill = StringVar()
bill_date = StringVar()


with sqlite3.connect("./Database/store.db") as db:
    cur = db.cursor()

def random_bill_number(stringLength):
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    strr=''.join(random.choice(lettersAndDigits) for i in range(stringLength-2))
    return ('BB'+strr)


def valid_phone(phn):
    if re.match(r"[789]\d{9}$", phn):
        return True
    return False

def login(Event=None):
    global username
    username = user.get()
    password = passwd.get()

    with sqlite3.connect("./Database/store.db") as db:
        cur = db.cursor()
    find_user = "SELECT * FROM employee WHERE emp_id = ? and password = ?"
    cur.execute(find_user, [username, password])
    results = cur.fetchall()
    if results:
        messagebox.showinfo("Login Page", "The login is successful")
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)
        root.withdraw()
        global biller
        global page2
        biller = Toplevel()
        page2 = bill_window(biller)
        page2.time()
        biller.protocol("WM_DELETE_WINDOW", exitt)
        biller.mainloop()

    else:
        messagebox.showerror("Error", "Incorrect username or password.")
        page1.entry2.delete(0, END)



def logout():
    sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=biller)
    if sure == True:
        biller.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Retail Manager")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/employee_login.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.373, rely=0.273, width=374, height=24)
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.373, rely=0.384, width=374, height=24)
        self.entry2.configure(font="-family {Poppins} -size 10")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)

        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#D2463E")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGIN""")
        self.button1.configure(command=login)


class Item:
    def __init__(self, name, price, qty):
        self.product_name = name
        self.price = price
        self.qty = qty

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        if len(self.items)==0:
            return True
        
    def allCart(self):
        for i in self.items:
            if (i.product_name in self.dictionary):
                self.dictionary[i.product_name] += i.qty
            else:
                self.dictionary.update({i.product_name:i.qty})
    

def exitt():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=biller)
    if sure == True:
        biller.destroy()
        root.destroy()


class bill_window:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Billing System")

        self.label = Label(biller)
        self.label.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/bill_window.png")
        self.label.configure(image=self.img)

        self.message = Label(biller)
        self.message.place(relx=0.038, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text=username)
        self.message.configure(anchor="w")

        self.clock = Label(biller)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(biller)
        self.entry1.place(relx=0.509, rely=0.23, width=240, height=24)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=cust_name)

        self.entry2 = Entry(biller)
        self.entry2.place(relx=0.791, rely=0.23, width=240, height=24)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(textvariable=cust_num)

        self.entry3 = Entry(biller)
        self.entry3.place(relx=0.102, rely=0.23, width=240, height=24)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(textvariable=cust_search_bill)

        self.button1 = Button(biller)
        self.button1.place(relx=0.031, rely=0.104, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Logout""")
        self.button1.configure(command=logout)

        self.button2 = Button(biller)
        self.button2.place(relx=0.315, rely=0.234, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Search""")
        self.button2.configure(command=self.search_bill)

        self.button3 = Button(biller)
        self.button3.place(relx=0.048, rely=0.885, width=86, height=25)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 10")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""Total""")
        self.button3.configure(command=self.total_bill)

        self.button4 = Button(biller)
        self.button4.place(relx=0.141, rely=0.885, width=84, height=25)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 10")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""Generate""")
        self.button4.configure(command=self.gen_bill)

        self.button5 = Button(biller)
        self.button5.place(relx=0.230, rely=0.885, width=86, height=25)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#CF1E14")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#CF1E14")
        self.button5.configure(font="-family {Poppins SemiBold} -size 10")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""Clear""")
        self.button5.configure(command=self.clear_bill)

        self.button6 = Button(biller)
        self.button6.place(relx=0.322, rely=0.885, width=86, height=25)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Poppins SemiBold} -size 10")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""Exit""")
        self.button6.configure(command=exitt)

        self.button7 = Button(biller)
        self.button7.place(relx=0.098, rely=0.734, width=86, height=26)
        self.button7.configure(relief="flat")
        self.button7.configure(overrelief="flat")
        self.button7.configure(activebackground="#CF1E14")
        self.button7.configure(cursor="hand2")
        self.button7.configure(foreground="#ffffff")
        self.button7.configure(background="#CF1E14")
        self.button7.configure(font="-family {Poppins SemiBold} -size 10")
        self.button7.configure(borderwidth="0")
        self.button7.configure(text="""Add To Cart""")
        self.button7.configure(command=self.add_to_cart)

        self.button8 = Button(biller)
        self.button8.place(relx=0.274, rely=0.734, width=84, height=26)
        self.button8.configure(relief="flat")
        self.button8.configure(overrelief="flat")
        self.button8.configure(activebackground="#CF1E14")
        self.button8.configure(cursor="hand2")
        self.button8.configure(foreground="#ffffff")
        self.button8.configure(background="#CF1E14")
        self.button8.configure(font="-family {Poppins SemiBold} -size 10")
        self.button8.configure(borderwidth="0")
        self.button8.configure(text="""Clear""")
        self.button8.configure(command=self.clear_selection)

        self.button9 = Button(biller)
        self.button9.place(relx=0.194, rely=0.734, width=68, height=26)
        self.button9.configure(relief="flat")
        self.button9.configure(overrelief="flat")
        self.button9.configure(activebackground="#CF1E14")
        self.button9.configure(cursor="hand2")
        self.button9.configure(foreground="#ffffff")
        self.button9.configure(background="#CF1E14")
        self.button9.configure(font="-family {Poppins SemiBold} -size 10")
        self.button9.configure(borderwidth="0")
        self.button9.configure(text="""Remove""")
        self.button9.configure(command=self.remove_product)

        text_font = ("Poppins", "8")
        self.combo1 = ttk.Combobox(biller)
        self.combo1.place(relx=0.035, rely=0.408, width=477, height=26)

        find_category = "SELECT product_cat FROM raw_inventory"
        cur.execute(find_category)
        result1 = cur.fetchall()
        cat = []
        for i in range(len(result1)):
            if(result1[i][0] not in cat):
                cat.append(result1[i][0])


        self.combo1.configure(values=cat)
        self.combo1.configure(state="readonly")
        self.combo1.configure(font="-family {Poppins} -size 8")
        self.combo1.option_add("*TCombobox*Listbox.font", text_font)
        self.combo1.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")


        self.combo2 = ttk.Combobox(biller)
        self.combo2.place(relx=0.035, rely=0.479, width=477, height=26)
        self.combo2.configure(font="-family {Poppins} -size 8")
        self.combo2.option_add("*TCombobox*Listbox.font", text_font) 
        self.combo2.configure(state="disabled")


        self.combo3 = ttk.Combobox(biller)
        self.combo3.place(relx=0.035, rely=0.551, width=477, height=26)
        self.combo3.configure(state="disabled")
        self.combo3.configure(font="-family {Poppins} -size 8")
        self.combo3.option_add("*TCombobox*Listbox.font", text_font)

        self.entry4 = ttk.Entry(biller)
        self.entry4.place(relx=0.035, rely=0.629, width=477, height=26)
        self.entry4.configure(font="-family {Poppins} -size 8")
        self.entry4.configure(foreground="#000000")
        self.entry4.configure(state="disabled")

        self.Scrolledtext1 = tkst.ScrolledText(top)
        self.Scrolledtext1.place(relx=0.439, rely=0.586, width=695, height=275)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

        self.combo1.bind("<<ComboboxSelected>>", self.get_category)
        
    def get_category(self, Event):
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        find_subcat = "SELECT product_subcat FROM raw_inventory WHERE product_cat = ?"
        cur.execute(find_subcat, [self.combo1.get()])
        result2 = cur.fetchall()
        subcat = []
        for j in range(len(result2)):
            if(result2[j][0] not in subcat):
                subcat.append(result2[j][0])
        
        self.combo2.configure(values=subcat)
        self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
        self.combo3.configure(state="disabled")

    def get_subcat(self, Event):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        find_product = "SELECT product_name FROM raw_inventory WHERE product_cat = ? and product_subcat = ?"
        cur.execute(find_product, [self.combo1.get(), self.combo2.get()])
        result3 = cur.fetchall()
        pro = []
        for k in range(len(result3)):
            pro.append(result3[k][0])

        self.combo3.configure(values=pro)
        self.combo3.bind("<<ComboboxSelected>>", self.show_qty)
        self.entry4.configure(state="disabled")

    def show_qty(self, Event):
        self.entry4.configure(state="normal")
        self.qty_label = Label(biller)
        self.qty_label.place(relx=0.033, rely=0.664, width=82, height=26)
        self.qty_label.configure(font="-family {Poppins} -size 8")
        self.qty_label.configure(anchor="w")

        product_name = self.combo3.get()
        find_qty = "SELECT stock FROM raw_inventory WHERE product_name = ?"
        cur.execute(find_qty, [product_name])
        results = cur.fetchone()
        self.qty_label.configure(text="In Stock: {}".format(results[0]))
        self.qty_label.configure(background="#ffffff")
        self.qty_label.configure(foreground="#333333")
    
    cart = Cart()
    def add_to_cart(self):
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total')==-1:
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = mrp*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)
        else:
            self.Scrolledtext1.delete('1.0', END)
            new_li = []
            li = strr.split("\n")
            for i in range(len(li)):
                if len(li[i])!=0:
                    if li[i].find('Total')==-1:
                        new_li.append(li[i])
                    else:
                        break
            for j in range(len(new_li)-1):
                self.Scrolledtext1.insert('insert', new_li[j])
                self.Scrolledtext1.insert('insert','\n')
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock, product_id FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = results[0][0]*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)

    def remove_product(self):
        if(self.cart.isEmpty()!=True):
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.Scrolledtext1.configure(state="normal")
                    get_all_bill = (self.Scrolledtext1.get('1.0', END).split("\n"))
                    new_string = get_all_bill[:len(get_all_bill)-3]
                    self.Scrolledtext1.delete('1.0', END)
                    for i in range(len(new_string)):
                        self.Scrolledtext1.insert('insert', new_string[i])
                        self.Scrolledtext1.insert('insert','\n')
                    
                    self.Scrolledtext1.configure(state="disabled")
            else:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.Scrolledtext1.delete('1.0', END)
                    new_li = []
                    li = strr.split("\n")
                    for i in range(len(li)):
                        if len(li[i])!=0:
                            if li[i].find('Total')==-1:
                                new_li.append(li[i])
                            else:
                                break
                    new_li.pop()
                    for j in range(len(new_li)-1):
                        self.Scrolledtext1.insert('insert', new_li[j])
                        self.Scrolledtext1.insert('insert','\n')
                    self.Scrolledtext1.configure(state="disabled")

        else:
            messagebox.showerror("Oops!", "Add a product.", parent=biller)

    def wel_bill(self):
        self.name_message = Text(biller)
        self.name_message.place(relx=0.514, rely=0.452, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(biller)
        self.num_message.place(relx=0.894, rely=0.452, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(biller)
        self.bill_message.place(relx=0.499, rely=0.477, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(biller)
        self.bill_date_message.place(relx=0.852, rely=0.477, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")
    
    def total_bill(self):
        if self.cart.isEmpty():
            messagebox.showerror("Oops!", "Add a product.", parent=biller)
        else:
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                self.Scrolledtext1.configure(state="normal")
                divider = "\n\n\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider)
                total = "\nTotal\t\t\t\t\t\t\t\t\t\t\tRs. {}".format(self.cart.total())
                self.Scrolledtext1.insert('insert', total)
                divider2 = "\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider2)
                self.Scrolledtext1.configure(state="disabled")
            else:
                return

    state = 1
    def gen_bill(self):

        if self.state == 1:
            strr = self.Scrolledtext1.get('1.0', END)
            self.wel_bill()
            if(cust_name.get()==""):
                messagebox.showerror("Oops!", "Please enter a name.", parent=biller)
            elif(cust_num.get()==""):
                messagebox.showerror("Oops!", "Please enter a number.", parent=biller)
            elif valid_phone(cust_num.get())==False:
                messagebox.showerror("Oops!", "Please enter a valid number.", parent=biller)
            elif(self.cart.isEmpty()):
                messagebox.showerror("Oops!", "Cart is empty.", parent=biller)
            else: 
                if strr.find('Total')==-1:
                    self.total_bill()
                    self.gen_bill()
                else:
                    self.name_message.insert(END, cust_name.get())
                    self.name_message.configure(state="disabled")
            
                    self.num_message.insert(END, cust_num.get())
                    self.num_message.configure(state="disabled")
            
                    cust_new_bill.set(random_bill_number(8))

                    self.bill_message.insert(END, cust_new_bill.get())
                    self.bill_message.configure(state="disabled")
                
                    bill_date.set(str(date.today()))

                    self.bill_date_message.insert(END, bill_date.get())
                    self.bill_date_message.configure(state="disabled")

                    

                    with sqlite3.connect("./Database/store.db") as db:
                        cur = db.cursor()
                    insert = (
                        "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details) VALUES(?,?,?,?,?)"
                    )
                    cur.execute(insert, [cust_new_bill.get(), bill_date.get(), cust_name.get(), cust_num.get(), self.Scrolledtext1.get('1.0', END)])
                    db.commit()
                    #print(self.cart.items)
                    print(self.cart.allCart())
                    for name, qty in self.cart.dictionary.items():
                        update_qty = "UPDATE raw_inventory SET stock = stock - ? WHERE product_name = ?"
                        cur.execute(update_qty, [qty, name])
                        db.commit()
                    messagebox.showinfo("Success!!", "Bill Generated", parent=biller)
                    self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.state = 0
        else:
            return
                    
    def clear_bill(self):
        self.wel_bill()
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.name_message.configure(state="normal")
        self.num_message.configure(state="normal")
        self.bill_message.configure(state="normal")
        self.bill_date_message.configure(state="normal")
        self.Scrolledtext1.configure(state="normal")
        self.name_message.delete(1.0, END)
        self.num_message.delete(1.0, END)
        self.bill_message.delete(1.0, END)
        self.bill_date_message.delete(1.0, END)
        self.Scrolledtext1.delete(1.0, END)
        self.name_message.configure(state="disabled")
        self.num_message.configure(state="disabled")
        self.bill_message.configure(state="disabled")
        self.bill_date_message.configure(state="disabled")
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1

    def clear_selection(self):
        self.entry4.delete(0, END)
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        try:
            self.qty_label.configure(foreground="#ffffff")
        except AttributeError:
            pass
             
    def search_bill(self):
        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [cust_search_bill.get().rstrip()])
        results = cur.fetchall()
        if results:
            self.clear_bill()
            self.wel_bill()
            self.name_message.insert(END, results[0][2])
            self.name_message.configure(state="disabled")
    
            self.num_message.insert(END, results[0][3])
            self.num_message.configure(state="disabled")
    
            self.bill_message.insert(END, results[0][0])
            self.bill_message.configure(state="disabled")

            self.bill_date_message.insert(END, results[0][1])
            self.bill_date_message.configure(state="disabled")

            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")

            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

            self.state = 0

        else:
            messagebox.showerror("Error!!", "Bill not found.", parent=biller)
            self.entry3.delete(0, END)
            
    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


page1 = login_page(root)
root.bind("<Return>", login)
root.mainloop()

