import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
import tkintermapview
import sqlite3
import regex as re
from geopy.geocoders import Nominatim

class Controler:
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
        self.view.map_widget.delete_all_marker()
        for item in self.view.table.get_children():
            self.view.table.delete(item)
        if data_type==None:
            data_type = self.view.data_type_selected.get()

        if data_type=="Employee":
            data_dictionary = self.model_R4SDB.get_employee_list()              
            for k,dat in data_dictionary.items():
                self.view.table.insert("", "end", iid=k, values=dat)
                self.view.map_widget.set_marker(dat[6],dat[5],text=f'{dat[0]} {dat[1]}')
        if data_type=="Headquarters":
            data_dictionary = self.model_R4SDB.get_headquaters_list()
            for k,dat in data_dictionary.items():
                self.view.table.insert("", "end", iid=k, values=dat)
                self.view.map_widget.set_marker(dat[5],dat[4],text=dat[0])
        if data_type=="Rental":
            data_dictionary = self.model_R4SDB.get_rental_list()            
            for k,dat in data_dictionary.items():
                self.view.table.insert("", "end", iid=k, values=dat)
                self.view.map_widget.set_marker(dat[5],dat[4],text=dat[0])
            
        dict_keyes = list(data_dictionary.keys())
        self.populate_listbox(dict_keyes)
    
    def get_filtred_dictionarys_list(self,filter=None,value=None,data_type = None):
        self.view.map_widget.delete_all_marker()
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
                    self.view.map_widget.set_marker(dat[6],dat[5],text=f'{dat[0]} {dat[1]}')
            if data_type=="Headquarters":
                data_dictionary = self.model_R4SDB.get_filtred_headquaters_list(filter,value)
                for k,dat in data_dictionary.items():
                    self.view.table.insert("", "end", iid=k, values=dat)
                    self.view.map_widget.set_marker(dat[5],dat[4],text=dat[0])
            if data_type=="Rental":
                data_dictionary = self.model_R4SDB.get_filtred_rental_list(filter,value)
                for k,dat in data_dictionary.items():
                    self.view.table.insert("", "end", iid=k, values=dat)
                    self.view.map_widget.set_marker(dat[5],dat[4],text=dat[0])
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
                self.view.add_confirm_button.config(text='Add',command=self.add_to_db)
            except ValueError as error:
                self.view.show_error_location(error)
        if data_type=="Rental":
            name = self.view.name.get()
            print(kay,[name,city,road,number])
            try:
                Headquarters_id = self.view.head_id.get()
                self.get_filtred_dictionarys('id',Headquarters_id,'Headquarters')
                if self.dict_res[0]:
                    print(kay,[name,city,road,number,Headquarters_id])
                else:
                    self.view.show_error_location('Invalid headqoters id')
            except:
                self.view.show_error_location('Invalid ID Datatype')
            try:
                Headquarters_id = self.view.head_id.get()
                self.get_filtred_dictionarys('id',Headquarters_id,'Headquarters')
                if self.dict_res[0]:
                    self.model_R4SDB.update_rental(kay,[name,city,road,number,Headquarters_id])
                    self.view.clean_inputs()
                    self.view.add_confirm_button.config(text='Add',command=self.add_to_db)
                else:
                    self.view.show_error_location('Invalid headqoters id')
            except ValueError as error:
                self.view.show_error_location(error)
        if data_type=="Employee":
            first_name = self.view.first_name.get()
            family_name = self.view.family_name.get()
            name = self.view.name.get()
            try:
                rental_id = self.view.rent_id.get()
            except:
                self.view.show_error_location('Invalid ID Datatype')
            try:
                rental_id = self.view.rent_id.get()
                self.get_filtred_dictionarys('id',rental_id,'Rental')
                if self.dict_res[0]:
                    self.model_R4SDB.update_employee(kay,[first_name,family_name,city,road,number,rental_id])
                    self.view.clean_inputs()
                    self.view.add_confirm_button.config(text='Add',command=self.add_to_db)
                else:
                    self.view.show_error_location('invalid Rental ID')
            except ValueError as error:
                self.view.show_error_location(error)
        
        self.get_dictionarys_list()
        
    def remove_from_db(self):
        data_type = self.view.data_type_selected.get()
        res, kay = self.view.extract_active_from_list_bx()
        kay = self.dict_res[1][0]
        id = int(kay.split('#')[-1])
        if data_type=="Headquarters":
                self.get_filtred_dictionarys('headqoters_id',id,'Rental')
                if  len(self.dict_res[1]) >0:
                    messagebox.showwarning("Warning", "There are related Rentals to this Headquarters, remove or edit them first")
                else:
                    self.model_R4SDB.remove_headquater(kay)
        if data_type=="Rental":
                self.get_filtred_dictionarys('rental_id',id,'Employee')
                if  len(self.dict_res[1]) >0:
                    messagebox.showwarning("Warning", "There are related Employees to this Rental, remove or edit them first")
                else:
                    self.model_R4SDB.remove_rental(kay)
        if data_type=="Employee":
                self.model_R4SDB.remove_employee(kay)
        self.get_dictionarys_list()
