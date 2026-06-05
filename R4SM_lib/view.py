import tkinter as tk
from tkinter import ttk
import tkintermapview


class View(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        
        # main view
        self.header = tk.Frame(parent, bg="#000000", height=80)
        self.header.pack(side='top', fill='x')
        self.container = tk.Frame(parent)
        self.container.pack(fill='both',expand=True)
        self.left_sidebar = tk.Frame(self.container,bg="#242424", width=250)
        self.left_sidebar.pack(side="left",fill="y")
        self.right_sidebar = tk.Frame(self.container,bg="#242424", width=250)
        self.right_sidebar.pack(side="right",fill="y")
        self.toolbar = tk.Frame(self.container, bg="#606060", height=40)
        self.toolbar.pack(side='top', fill='x')
        self.main_area = tk.LabelFrame(self.container)
        self.main_area.pack(pady=10, padx=10, fill='both',expand=True)
        
        # środkowy kontener na formularz
        self.form = tk.Frame(self.main_area)
        self.form.pack(expand=True)  

        # Login entry
        self.label_login = ttk.Label(self.form,text='Email:')
        self.label_login.grid(row=1,column=0)

        # email entry
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self.form, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # Password entry
        self.label_password = ttk.Label(self.form,text='Password:')
        self.label_password.grid(row=3,column=0)
        # Password entry
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.form, textvariable=self.password_var,show="*", width=30)
        self.password_entry.grid(row=3, column=1, sticky=tk.NSEW)
        # message
        self.message_label = ttk.Label(self.form, text='', foreground='red')
        self.message_label.grid(row=4,column=1,sticky=tk.W)

        # login button
        self.login_button = ttk.Button(self.form,text='Login',command=self.login_button_clicked)
        self.login_button.grid(row=5,column=0,columnspan=2)
        # controller
        self.controller = None

    def set_controler(self, controler):
        self.controller = controler

    def login_button_clicked(self):
        if self.controller:
            self.controller.login(self.email_var.get(),self.password_var.get())

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000,self.hide_message)
        self.email_entry['foreground'] = 'red'
        self.password_entry['foreground'] = 'red'

    def show_success(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000,self.hide_message)
        self.email_entry['foreground'] = 'black'
        self.password_entry['foreground'] = 'black'
        self.email_var.set('')
        self.password_var.set('')
    
    def hide_message(self):
        self.message_label['text'] = ''
    

# TEST
# Sample data:
# ABC@mail.com
# ABC
class testControler:
    def __init__(self, view):
        self.view = view
    def login(self,login,password):
        # simpler control version
        if  '@' in login:
            print(login)
        else:
            self.view.show_error('Error') 
        if password == 'Admin1':
            print(password)
            self.view.show_success('Loged In')
        else:
            self.view.show_error('Error')

root = tk.Tk()
view = View(root)
controller = testControler(view)
view.set_controler(controller)
view.pack()
root.mainloop()