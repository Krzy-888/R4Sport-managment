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
        
        # Table view
        self.table_frame = tk.Frame(self.main_area)
        self.table_frame.pack(expand=True)
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.table = ttk.Treeview(self.table_frame,show='headings',
                                  columns=('Name','City','Road','Building No.','Lat','Lon'),
                                   yscrollcommand=self.scrollbar.set)
        for col in ('Name','City','Road','Building No.','Lat','Lon'):
            self.table.column(col, width=120, anchor="center")
        
        self.scrollbar.config(command=self.table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)
        self.table.heading("#0",text='Label')
        self.table.heading("Name",text='Name')
        self.table.heading("City",text='City')
        self.table.heading("Road",text='Road')
        self.table.heading("Building No.",text='Building No.')
        self.table.heading("Lat",text='Lat')
        self.table.heading("Lon",text='Lon')
        self.table.pack()
        
        # left side bar
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
            "city",
            "road")
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
        self.update_button = tk.Button(self.buttons_frame,text='Update',command=self.fill_in_inputs)
        self.update_button.grid(row=0,column=1)
        self.remove_button = tk.Button(self.buttons_frame,text='Remove',command=self.controller.remove_from_db)
        self.remove_button.grid(row=0,column=2)

        # right side bar
        self.input_form_frame = tk.Frame(self.rightbar_form_input_frame,background='#242424')
        self.input_form_frame.pack(expand=True)
        tk.Label(self.input_form_frame,text='Name:',foreground="#ffffff",background='#242424').grid(row=0,column=0)
        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self.input_form_frame, textvariable=self.name, width=30)
        self.name_entry.grid(row=0,column=1)
        tk.Label(self.input_form_frame,text='City:',foreground="#ffffff",background='#242424').grid(row=1,column=0)
        self.city = tk.StringVar()
        self.city_entry = ttk.Entry(self.input_form_frame, textvariable=self.city, width=30)
        self.city_entry.grid(row=1,column=1)
        tk.Label(self.input_form_frame,text='Road:',foreground="#ffffff",background='#242424').grid(row=2,column=0)
        self.road = tk.StringVar()
        self.road_entry = ttk.Entry(self.input_form_frame, textvariable=self.road, width=30)
        self.road_entry.grid(row=2,column=1)
        tk.Label(self.input_form_frame,text='No.:',foreground="#ffffff",background='#242424').grid(row=3,column=0)
        self.number = tk.StringVar()
        self.number_entry = ttk.Entry(self.input_form_frame, textvariable=self.number, width=30)
        self.number_entry.grid(row=3,column=1)
        self.message_label_location = tk.Label(self.input_form_frame,text='',foreground="#ffffff",background='#242424')
        self.message_label_location.grid(row=4,column=0)
        self.add_confirm_button = tk.Button(self.input_form_frame,text='Add',command=self.controller.add_to_db)
        self.add_confirm_button.grid(row=5,column=0)
        
        
        



    def display_Rental_datatype_menu(self):

        # Table view
        self.table_frame = tk.Frame(self.main_area)
        self.table_frame.pack(expand=True)
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.table = ttk.Treeview(self.table_frame,show='headings',
                                  columns=('Name','City','Road','Building No.','Lat','Lon','Headquoters','Dsitance'),
                                   yscrollcommand=self.scrollbar.set)
        for col in ('Name','City','Road','Building No.','Lat','Lon', 'Headquoters', 'Dsitance'):
            self.table.column(col, width=100, anchor="center")
        
        self.scrollbar.config(command=self.table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)
        self.table.heading("#0",text='Label')
        self.table.heading("Name",text='Name')
        self.table.heading("City",text='City')
        self.table.heading("Road",text='Road')
        self.table.heading("Building No.",text='Building No.')
        self.table.heading("Lat",text='Lat')
        self.table.heading("Lon",text='Lon')
        self.table.heading("Headquoters",text='Headquoters')
        self.table.heading("Dsitance",text='Dsitance')
        self.table.pack()


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
            "city",
            "road",
            "headqoters_id"
            )
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
        self.update_button = tk.Button(self.buttons_frame,text='Update',command=self.fill_in_inputs)
        self.update_button.grid(row=0,column=1)
        self.remove_button = tk.Button(self.buttons_frame,text='Remove',command=self.controller.remove_from_db)
        self.remove_button.grid(row=0,column=2)


        # right side bar
        self.input_form_frame = tk.Frame(self.rightbar_form_input_frame,background='#242424')
        self.input_form_frame.pack(expand=True)
        tk.Label(self.input_form_frame,text='Name:',foreground="#ffffff",background='#242424').grid(row=0,column=0)
        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self.input_form_frame, textvariable=self.name, width=30)
        self.name_entry.grid(row=0,column=1)
        tk.Label(self.input_form_frame,text='City:',foreground="#ffffff",background='#242424').grid(row=1,column=0)
        self.city = tk.StringVar()
        self.city_entry = ttk.Entry(self.input_form_frame, textvariable=self.city, width=30)
        self.city_entry.grid(row=1,column=1)
        tk.Label(self.input_form_frame,text='Road:',foreground="#ffffff",background='#242424').grid(row=2,column=0)
        self.road = tk.StringVar()
        self.road_entry = ttk.Entry(self.input_form_frame, textvariable=self.road, width=30)
        self.road_entry.grid(row=2,column=1)
        tk.Label(self.input_form_frame,text='No.:',foreground="#ffffff",background='#242424').grid(row=3,column=0)
        self.number = tk.StringVar()
        self.number_entry = ttk.Entry(self.input_form_frame, textvariable=self.number, width=30)
        self.number_entry.grid(row=3,column=1)
        self.number = tk.StringVar()
        self.number_entry = ttk.Entry(self.input_form_frame, textvariable=self.number, width=30)
        self.number_entry.grid(row=3,column=1)
        tk.Label(self.input_form_frame,text='Headquarters ID:',foreground="#ffffff",background='#242424').grid(row=4,column=0)
        self.head_id = tk.StringVar()
        self.head_id_entry = ttk.Entry(self.input_form_frame, textvariable=self.head_id, width=30)
        self.head_id_entry.grid(row=4,column=1)
        self.message_label_location = tk.Label(self.input_form_frame,text='',foreground="#ffffff",background='#242424')
        self.message_label_location.grid(row=5,column=0)
        self.add_confirm_button = tk.Button(self.input_form_frame,text='Add',command=self.controller.add_to_db)
        self.add_confirm_button.grid(row=6,column=0)

    def display_Employee_datatype_menu(self):
        # Table view
        self.table_frame = tk.Frame(self.main_area)
        self.table_frame.pack(expand=True)
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.table = ttk.Treeview(self.table_frame,show='headings',
                                  columns=('Name','City','Road','Building No.','Lat','Lon', 'Headquoters', 'Rental', 'Distance'),
                                   yscrollcommand=self.scrollbar.set)
        for col in ('Name','City','Road','Building No.','Lat','Lon', 'Headquoters', 'Rental', 'Distance'):
            self.table.column(col, width=100, anchor="center")
        
        self.scrollbar.config(command=self.table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)
        self.table.heading("#0",text='Label')
        self.table.heading("Name",text='Name')
        self.table.heading("City",text='City')
        self.table.heading("Road",text='Road')
        self.table.heading("Building No.",text='Building No.')
        self.table.heading("Lat",text='Lat')
        self.table.heading("Lon",text='Lon')
        self.table.heading("Headquoters",text='Headquoters')
        self.table.heading("Rental",text='Rental')
        self.table.heading("Distance",text='Distance')
        self.table.pack()

        ttk.Label(self.leftbar_filtering_and_list_frame,text='Filter:',foreground="#ffffff",background='#242424').pack()
        ttk.Label(self.leftbar_filtering_and_list_frame,text='Employee',foreground="#ffffff",background='#242424').pack()
        self.filterin_frame = tk.Frame(self.leftbar_filtering_and_list_frame,background='#242424')
        self.filterin_frame.pack(expand=True)
        self.filtering_field = tk.StringVar(value='id')
        self.filter_field_dropdown = tk.OptionMenu(
            self.filterin_frame,
            self.filtering_field,
            "id",
            "firstname",
            "familyname",
            "city",
            "road",
            "rental_id",
            "headqoters_id")
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
        self.update_button = tk.Button(self.buttons_frame,text='Update',command=self.fill_in_inputs)
        self.update_button.grid(row=0,column=1)
        self.remove_button = tk.Button(self.buttons_frame,text='Remove',command=self.controller.remove_from_db)
        self.remove_button.grid(row=0,column=2)


        # right side bar
        self.input_form_frame = tk.Frame(self.rightbar_form_input_frame,background='#242424')
        self.input_form_frame.pack(expand=True)
        tk.Label(self.input_form_frame,text='First Name:',foreground="#ffffff",background='#242424').grid(row=0,column=0)
        self.first_name = tk.StringVar()
        self.first_name_entry = ttk.Entry(self.input_form_frame, textvariable=self.first_name, width=30)
        self.first_name_entry.grid(row=0,column=1)
        tk.Label(self.input_form_frame,text='Family Name:',foreground="#ffffff",background='#242424').grid(row=1,column=0)
        self.family_name = tk.StringVar()
        self.family_name_entry = ttk.Entry(self.input_form_frame, textvariable=self.family_name, width=30)
        self.family_name_entry.grid(row=1,column=1)
        tk.Label(self.input_form_frame,text='City:',foreground="#ffffff",background='#242424').grid(row=2,column=0)
        self.city = tk.StringVar()
        self.city_entry = ttk.Entry(self.input_form_frame, textvariable=self.city, width=30)
        self.city_entry.grid(row=2,column=1)
        tk.Label(self.input_form_frame,text='Road:',foreground="#ffffff",background='#242424').grid(row=3,column=0)
        self.road = tk.StringVar()
        self.road_entry = ttk.Entry(self.input_form_frame, textvariable=self.road, width=30)
        self.road_entry.grid(row=3,column=1)
        tk.Label(self.input_form_frame,text='No.:',foreground="#ffffff",background='#242424').grid(row=4,column=0)
        self.number = tk.StringVar()
        self.number_entry = ttk.Entry(self.input_form_frame, textvariable=self.number, width=30)
        self.number_entry.grid(row=4,column=1)
        self.number = tk.StringVar()
        self.number_entry = ttk.Entry(self.input_form_frame, textvariable=self.number, width=30)
        self.number_entry.grid(row=4,column=1)
        tk.Label(self.input_form_frame,text='Rental ID:',foreground="#ffffff",background='#242424').grid(row=5,column=0)
        self.rent_id = tk.StringVar()
        self.rent_id_entry = ttk.Entry(self.input_form_frame, textvariable=self.rent_id, width=30)
        self.rent_id_entry.grid(row=5,column=1)
        self.message_label_location = tk.Label(self.input_form_frame,text='',foreground="#ffffff",background='#242424')
        self.message_label_location.grid(row=6,column=0)
        self.add_confirm_button = tk.Button(self.input_form_frame,text='Add',command=self.controller.add_to_db)
        self.add_confirm_button.grid(row=7,column=0)
        
    
    def change_data_view(self,*args):
        choice = self.data_type_selected.get()
        for widget in self.leftbar_filtering_and_list_frame.winfo_children():
            widget.destroy()
        for widget in self.rightbar_form_input_frame.winfo_children():
            widget.destroy()
        for widget in self.main_area.winfo_children():
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
        self.rightbar_form_input_frame = tk.Frame(self.right_sidebar,background='#242424')
        self.rightbar_form_input_frame.pack(expand=True)
        self.display_Headquarters_datatype_menu()
        

    def show_success(self, username):
        self.show_dashboard(username)


    def hide_message(self):
        self.message_label['text'] = ''
        
    def hide_message_location(self):
        self.message_label_location['text'] = ''

    def clean_inputs(self,datatype=None):
        if datatype==None:
            datatype = self.data_type_selected.get()
        if datatype=='Headquarters':
            self.name.set('')
        if datatype=='Rental':
            self.name.set('')
            self.head_id.set('')
        if datatype=='Employee':
            self.first_name.set('')
            self.family_name.set('')
            self.rent_id.set('')
        self.filtering_var.set('')
        self.number_entry['foreground'] = 'black'
        self.road_entry['foreground'] = 'black'
        self.city_entry['foreground'] = 'black'
        self.number.set('')
        self.road.set('')
        self.city.set('')
    
    def extract_active_from_list_bx(self):
        i = self.list_box.index(tk.ACTIVE)
        kay = self.list_box.get(i)
        id = kay.split('#')[-1]
        self.controller.get_filtred_dictionarys('id',int(id))
        kay = self.controller.dict_res[1]
        res = self.controller.dict_res[0]
        res = res[kay[0]]
        return res, kay
    def fill_in_inputs(self,datatype=None):
        res, kay = self.extract_active_from_list_bx()
        if datatype==None:
            datatype = self.data_type_selected.get()
        if datatype=='Headquarters':

            self.name.set(res[0])
            self.city.set(res[1])
            self.road.set(res[2])
            self.number.set(res[3])            

        if datatype=='Rental':

            self.name.set(res[0])
            self.city.set(res[1])
            self.road.set(res[2])
            self.number.set(res[3])    
            self.head_id.set(res[7].split('#')[-1])
        if datatype=='Employee':
            self.first_name.set(res[0])
            self.family_name.set(res[1])
            self.city.set(res[2])
            self.road.set(res[3])
            self.number.set(res[4])
            self.rent_id.set(res[8].split('#')[-1])
        self.add_confirm_button.config(text='Confirm', command=self.controller.update_to_db)

    
    def show_error_location(self, message,datatype=None):
        if datatype==None:
            datatype = self.data_type_selected.get()
        self.message_label_location['text'] = message
        self.message_label_location['foreground'] = 'red'
        self.message_label_location.after(3000,self.hide_message)
        if datatype=='Rental':
            self.head_id_entry['foreground'] = 'red'
        self.number_entry['foreground'] = 'red'
        self.road_entry['foreground'] = 'red'
        self.city_entry['foreground'] = 'red'
    

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
        for item in self.view.table.get_children():
            self.view.table.delete(item)
        if data_type==None:
            data_type = self.view.data_type_selected.get()

        if data_type=="Employee":
            data_dictionary = self.model_R4SDB.get_employee_list()              
            for k,dat in data_dictionary.items():
                self.view.table.insert("", "end", iid=k, values=dat)
        if data_type=="Headquarters":
            data_dictionary = self.model_R4SDB.get_headquaters_list()
            for k,dat in data_dictionary.items():
                self.view.table.insert("", "end", iid=k, values=dat)
        if data_type=="Rental":
            data_dictionary = self.model_R4SDB.get_rental_list()            
            for k,dat in data_dictionary.items():
                self.view.table.insert("", "end", iid=k, values=dat)
            
        dict_keyes = list(data_dictionary.keys())
        self.populate_listbox(dict_keyes)
    
    def get_filtred_dictionarys_list(self,filter=None,value=None,data_type = None):
        
        for item in self.view.table.get_children():
            self.view.table.delete(item)
        if data_type==None:
            data_type = self.view.data_type_selected.get()
        if value==None:
            value = f'%{self.view.filtering_var.get()}%'
        if filter==None:
            filter = self.view.filtering_field.get()
        if value == '':
            self.get_dictionarys_list()
        else:
            if data_type=="Employee":
                data_dictionary = self.model_R4SDB.get_filtred_employee_list(filter,value)
                for k,dat in data_dictionary.items():
                    self.view.table.insert("", "end", iid=k, values=dat)
            if data_type=="Headquarters":
                data_dictionary = self.model_R4SDB.get_filtred_headquaters_list(filter,value)
                for k,dat in data_dictionary.items():
                    self.view.table.insert("", "end", iid=k, values=dat)
            if data_type=="Rental":
                data_dictionary = self.model_R4SDB.get_filtred_rental_list(filter,value)
                for k,dat in data_dictionary.items():
                    self.view.table.insert("", "end", iid=k, values=dat)
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
            value = f'%{self.view.filtering_var.get()}%'
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
    
    def add_to_db(self):
        data_type = self.view.data_type_selected.get()            
        city = self.view.city.get()
        road = self.view.road.get()
        number = self.view.number.get()
        if data_type=="Headquarters":
            name = self.view.name.get()
            try:
                self.model_R4SDB.add_headquaters_list([name,city,road,number])
                self.view.clean_inputs()
            except ValueError as error:
                self.view.show_error_location(error)
        if data_type=="Rental":
            name = self.view.name.get()
            try:
                Headquarters_id = int(self.view.head_id.get())
            except:
                self.view.show_error_location('Invalid ID Datatype')
            try:
                self.model_R4SDB.add_rental_list([name,city,road,number,Headquarters_id])
                self.view.clean_inputs()
            except ValueError as error:
                self.view.show_error_location(error)
        if data_type=="Employee":
            first_name = self.view.first_name.get()
            family_name = self.view.family_name.get()
            name = self.view.name.get()
            try:
                rental_id = int(self.view.rent_id.get())
            except:
                self.view.show_error_location('Invalid ID Datatype')
            try:
                self.model_R4SDB.add_employee_list([first_name,family_name,city,road,number,rental_id])
                self.view.clean_inputs()
            except ValueError as error:
                self.view.show_error_location(error)
        self.get_dictionarys_list()

    def update_to_db(self):
        data_type = self.view.data_type_selected.get()
        city = self.view.city.get()
        road = self.view.road.get()
        number = self.view.number.get()
        kay = self.dict_res[1][0]
        if data_type=="Headquarters":
            name = self.view.name.get()
            try:
                self.model_R4SDB.update_headquater(kay,[name,city,road,number])
                self.view.clean_inputs()
            except ValueError as error:
                self.view.show_error_location(error)
        if data_type=="Rental":
            name = self.view.name.get()
            try:
                Headquarters_id = int(self.view.head_id.get())
            except:
                self.view.show_error_location('Invalid ID Datatype')
            try:
                self.model_R4SDB.update_rental(kay,[name,city,road,number,Headquarters_id])
                self.view.clean_inputs()
            except ValueError as error:
                self.view.show_error_location(error)
        if data_type=="Employee":
            first_name = self.view.first_name.get()
            family_name = self.view.family_name.get()
            name = self.view.name.get()
            try:
                rental_id = int(self.view.rent_id.get())
            except:
                self.view.show_error_location('Invalid ID Datatype')
            try:
                self.model_R4SDB.update_employee(kay,[first_name,family_name,city,road,number,rental_id])
                self.view.clean_inputs()
            except ValueError as error:
                self.view.show_error_location(error)
        self.view.add_confirm_button.config(text='Add',command=self.add_to_db)
        self.get_dictionarys_list()
        
    def remove_from_db(self):
        data_type = self.view.data_type_selected.get()
        res, kay = self.view.extract_active_from_list_bx()
        kay = self.dict_res[1][0]
        id = int(kay.split('#')[-1])
        if data_type=="Headquarters":
                self.get_filtred_dictionarys('headqoters_id',id,'Rental')
                if  len(self.dict_res[1]) >0:
                    print('Są')
                else:
                    print('Nie ma')
                    self.model_R4SDB.remove_headquater(kay)
        if data_type=="Rental":
                self.get_filtred_dictionarys('rental_id',id,'Employee')
                if  len(self.dict_res[1]) >0:
                    print('Są')
                else:
                    print('Nie ma')
                    self.model_R4SDB.remove_rental(kay)
        if data_type=="Employee":
                self.model_R4SDB.update_employee(kay)
        self.get_dictionarys_list()

root = tk.Tk()
view = View(root)
controller = testControler(view,model)
view.set_controler(controller)
view.pack()
root.mainloop()