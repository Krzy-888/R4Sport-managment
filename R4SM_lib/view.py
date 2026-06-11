import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import tkintermapview
import model


class View(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        # main view
        self.header = tk.Frame(parent, bg="#000000")
        self.header.pack(side='top', fill='x')
        self.Header_Label = ttk.Label(self.header,text='R4Sport managment',foreground='#FF0000',background='#000000', font=tkFont.Font(family="Arial", size=25))
        self.Header_Label.grid(column=0,row=0,rowspan=2)
        self.container = tk.Frame(parent)
        self.container.pack(fill='both',expand=True)
        self.left_sidebar = tk.Frame(self.container,bg="#242424", width=200)
        self.left_sidebar.pack(side="left",fill="y")
        self.right_sidebar = tk.Frame(self.container,bg="#242424", width=200)
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

    def display_Headquarters_datatype_menu(self):
        ttk.Label(self.leftbar_filtering_and_list_frame,text='Filter:',foreground="#ffffff",background='#242424').pack()
        # ttk.Label(self.leftbar_filtering_and_list_frame,text='Headquarters',foreground="#ffffff",background='#242424').pack()
        self.filterin_frame = tk.Frame(self.leftbar_filtering_and_list_frame,background='#242424')
        self.filterin_frame.pack(expand=True)
        self.filtering_field = tk.StringVar(value='id')
        self.filter_field_dropdown = tk.OptionMenu(
            self.filterin_frame,
            self.filtering_field,
            "id",
            "name",
            "city")
        self.filter_field_dropdown.config(bg="#ff0000", fg="#ffffff")
        self.filter_field_dropdown.grid(row=0,column=0)
        self.filtering_var = tk.StringVar()
        self.filtering_entry = ttk.Entry(self.filterin_frame, textvariable=self.filtering_var, width=30)
        self.filtering_entry.grid(row=0,column=1)
        self.filtering_var.trace_add("write", lambda *args: self.controller.get_filtred_dictionarys_list())
        self.list_box = tk.Listbox(self.leftbar_filtering_and_list_frame, height=15, width=30)
        self.list_box.pack(padx=10,pady=10)
        self.controller.get_dictionarys_list()
        self.buttons_frame = tk.Frame(self.leftbar_filtering_and_list_frame,background='#242424')
        self.buttons_frame.pack(expand=True)
        self.show_details_button = tk.Button(self.buttons_frame,text='Show details')
        self.show_details_button.grid(row=0,column=0)

    def display_Rental_datatype_menu(self):
        ttk.Label(self.leftbar_filtering_and_list_frame,text='Filter:',foreground="#ffffff",background='#242424').pack()
        ttk.Label(self.leftbar_filtering_and_list_frame,text='Rental',foreground="#ffffff",background='#242424').pack()
        self.filterin_frame = tk.Frame(self.leftbar_filtering_and_list_frame,background='#242424')
        self.filterin_frame.pack(expand=True)
        self.filtering_field = tk.StringVar(value='id')
        self.filter_field_dropdown = tk.OptionMenu(
            self.filterin_frame,
            self.filtering_field,
            "id",
            "name",
            "city")
        self.filter_field_dropdown.config(bg="#ff0000", fg="#ffffff")
        self.filter_field_dropdown.grid(row=0,column=0)
        self.filtering_var = tk.StringVar()
        self.filtering_entry = ttk.Entry(self.filterin_frame, textvariable=self.filtering_var, width=30)
        self.filtering_entry.grid(row=0,column=1)
        self.filtering_var.trace_add("write", lambda *args: self.controller.get_filtred_dictionarys_list())
        self.list_box = tk.Listbox(self.leftbar_filtering_and_list_frame, height=15, width=30)
        self.list_box.pack(padx=10,pady=10)
        self.controller.get_dictionarys_list()
    def display_Employee_datatype_menu(self):
        ttk.Label(self.leftbar_filtering_and_list_frame,text='Filter:',foreground="#ffffff",background='#242424').pack()
        ttk.Label(self.leftbar_filtering_and_list_frame,text='Employee',foreground="#ffffff",background='#242424').pack()
        self.filterin_frame = tk.Frame(self.leftbar_filtering_and_list_frame,background='#242424')
        self.filterin_frame.pack(expand=True)
        self.filtering_field = tk.StringVar(value='id')
        self.filter_field_dropdown = tk.OptionMenu(
            self.filterin_frame,
            self.filtering_field,
            "id",
            "name",
            "city")
        self.filter_field_dropdown.config(bg="#ff0000", fg="#ffffff")
        self.filter_field_dropdown.grid(row=0,column=0)
        self.filtering_var = tk.StringVar()
        self.filtering_entry = ttk.Entry(self.filterin_frame, textvariable=self.filtering_var, width=30)
        self.filtering_entry.grid(row=0,column=1)
        self.filtering_var.trace_add("write", lambda *args: self.controller.get_filtred_dictionarys_list())
        self.list_box = tk.Listbox(self.leftbar_filtering_and_list_frame, height=15, width=30)
        self.list_box.pack(padx=10,pady=10)
        self.controller.get_dictionarys_list()
        
    
    def change_data_view(self,*args):
        choice = self.data_type_selected.get()
        for widget in self.leftbar_filtering_and_list_frame.winfo_children():
            widget.destroy()
        if choice =="Headquarters":
            self.display_Headquarters_datatype_menu()
        if choice =="Rental":
            self.display_Rental_datatype_menu()
        if choice =="Employee":
            self.display_Employee_datatype_menu()
    
    def show_dashboard(self,username):
        self.username = username
        self.Username_Labe = ttk.Label(self.header,text=f'User:\t{username}',foreground='#FFFFFF',background='#000000').grid(column=1,row=0)
        self.form.destroy()
        self.data_type_selected = tk.StringVar(value='Headquarters')
        self.leftbar_datatype_dropdown = tk.OptionMenu(
            self.left_sidebar,
            self.data_type_selected,
            "Headquarters",
            "Rental",
            "Employee")
        self.leftbar_datatype_dropdown.config(bg="#ff0000", fg="#ffffff")
        self.leftbar_datatype_dropdown.pack(pady=5,padx=5)
        
        self.data_type_selected.trace_add("write", self.change_data_view)
        self.leftbar_filtering_and_list_frame = tk.Frame(self.left_sidebar,background='#242424')
        self.leftbar_filtering_and_list_frame.pack(expand=True)
        self.display_Headquarters_datatype_menu()
        ttk.Label(
        self.main_area,
        text="Witaj w aplikacji!",
        font=("Arial", 16)
        ).pack(expand=True)

    def show_success(self, username):
        self.show_dashboard(username)


    def hide_message(self):
        self.message_label['text'] = ''
    

# TEST
# Sample data:
# ABC@mail.com
# ABC
class testControler:
    def __init__(self, view,model):
        self.view = view
        self.model = model
    def login(self,login,password):
        # simpler control version
        try:
            model = self.model.user_model([login,password])
            data = model.write_user_data()
            username = f'{data[1]} {data[2]}'
            self.model_R4SDB = self.model.R4SR4SDB_model()
            self.view.show_success(username)
        except ValueError as error:
            self.view.show_error(error)

    def populate_listbox(self,list_input):
        try:
            self.view.list_box.delete(0, 'end')
        except:
            pass
        for idx,object_input in enumerate(list_input):
            self.view.list_box.insert(idx,object_input)
    
    def get_dictionarys_list(self,data_type = None):
        if data_type==None:
            data_type = self.view.data_type_selected.get()
        if data_type=="Employee":
            data_dictionary = self.model_R4SDB.get_employee_list()
        if data_type=="Headquarters":
            data_dictionary = self.model_R4SDB.get_headquaters_list()
        if data_type=="Rental":
            data_dictionary = self.model_R4SDB.get_rental_list()
        dict_keyes = list(data_dictionary.keys())
        self.populate_listbox(dict_keyes)
    
    def get_filtred_dictionarys_list(self,filter=None,value=None,data_type = None):
        if data_type==None:
            data_type = self.view.data_type_selected.get()
        if value==None:
            value = self.view.filtering_var.get()
        if filter==None:
            filter = self.view.filtering_field.get()
        if value == '':
            self.get_dictionarys_list()
        else:
            if data_type=="Employee":
                data_dictionary = self.model_R4SDB.get_filtred_employee_list(filter,value)
            if data_type=="Headquarters":
                data_dictionary = self.model_R4SDB.get_filtred_headquaters_list(filter,value)
            if data_type=="Rental":
                data_dictionary = self.model_R4SDB.get_filtred_rental_list(filter,value)
            dict_keyes = list(data_dictionary.keys())
            self.populate_listbox(dict_keyes)
        
    def get_dictionarys(self,data_type = None):
        if data_type==None:
            data_type = self.view.data_type_selected.get()
        if data_type=="Employee":
            data_dictionary = self.model_R4SDB.get_employee_list()
        if data_type=="Headquarters":
            data_dictionary = self.model_R4SDB.get_headquaters_list()
        if data_type=="Rental":
            data_dictionary = self.model_R4SDB.get_rental_list()
        dict_keyes = list(data_dictionary.keys())
        self.dict_res = [data_dictionary, dict_keyes]
    
    def get_filtred_dictionarys(self,filter=None,value=None,data_type = None):
        if data_type==None:
            data_type = self.view.data_type_selected.get()
        if value==None:
            value = self.view.filtering_var.get()
        if filter==None:
            filter = self.view.filtering_field.get()
        if value == '':
            self.get_dictionarys()
        else:
            if data_type=="Employee":
                data_dictionary = self.model_R4SDB.get_filtred_employee_list(filter,value)
            if data_type=="Headquarters":
                data_dictionary = self.model_R4SDB.get_filtred_headquaters_list(filter,value)
            if data_type=="Rental":
                data_dictionary = self.model_R4SDB.get_filtred_rental_list(filter,value)
            dict_keyes = list(data_dictionary.keys())
            self.dict_res = [data_dictionary, dict_keyes]
        
        

root = tk.Tk()
view = View(root)
controller = testControler(view,model)
view.set_controler(controller)
view.pack()
root.mainloop()