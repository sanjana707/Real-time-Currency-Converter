#This is a realtime currency converter which uses the request library to call the api for getting realtime currency rates
#This data is further manipulated to convert it into desired currency and rate according to user input
#It uses the tkinter library for graphics
#Make sure to install it

import tkinter as tk
import requests
from tkinter import ttk
from tkinter import *

class CurrencyConverter():
    def __init__(self, url):
        #Calls the api which returns a dictionary with currency rates in terms of USD
        #From this dictionary the rates are extracted
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']
        
    def convert(self, from_currency, to_currency, amount):
        initial_amt = amount
        if from_currency!='USD':
            amount = amount/self.currencies[from_currency]
            
        amount = round(amount * self.currencies[to_currency], 4)     #Rounding to 4 decimal digits
        return amount
        
class Window(tk.Tk):
    def __init__(self, convert_amount):
        tk.Tk.__init__(self)
        self.convert_amt = convert_amount
        
        #window design
        self.title('Currency Converter')
        self.configure(background='black')
        self.geometry('500x200')
        
        #Title
        self.title_label = Label(self, text='Real Time Currency Conveter', borderwidth=3, bg='#DDDDDD', fg="#000000", relief='raised')
        self.title_label.config(font=('Courier', 15, 'bold'))
        self.title_label.place(x=10, y=5)
        #self.title_label.grid(pady=10)
        self.title_label.pack(side='top')
        
        #Date
        self.date_label = Label(self, text=f"1 Indian Rupee equals = {self.convert_amt.convert('INR','USD',1)} USD \n Date : {self.convert_amt.data['date']}", fg="#000000", relief="groove")
        self.date_label.place(x=160, y=50)
        
        #Entry Box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_entry=Entry(self, validate='key', validatecommand=valid, justify = tk.CENTER)
        
        #Converted amount field
        self.converted_amt_field = Label(self, text='', bg='white', justify=tk.CENTER, width=18, fg="black")
        
        #Dropdown
        self.to_currency_var = StringVar(self)
        self.from_currency_var = StringVar(self)
        #default values
        self.to_currency_var.set("USD")       
        self.from_currency_var.set("INR")
        
        font = ('Courier', 12, 'bold')
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_var, values=list(self.convert_amt.currencies.keys()), justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_var, values=list(self.convert_amt.currencies.keys()), justify=tk.CENTER)
        
        #placing
        self.amount_entry.place(x=36, y=150)
        self.converted_amt_field.place(x=346, y=150)
        self.from_currency_dropdown.place(x=30, y=120)
        self.to_currency_dropdown.place(x=340, y=120)
        
        #Button to convert
        self.convert_button = Button(self, text='Convert', fg='black', command=self.perform)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x=225, y=135)
        
    
    def perform(self):
        amount=float(self.amount_entry.get())
        from_curr = self.from_currency_var.get()
        to_curr = self.to_currency_var.get()
        
        converted_amt = round(self.convert_amt.convert(from_curr, to_curr, amount), 2)
        self.converted_amt_field.config(text = str(converted_amt))
    
    def restrictNumberOnly(self, action, string):
        #THis function restricts the user from entering any invalid value using regular expression
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string=="" or (string.count('.')<=1 and result is not None))


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyConverter(url)
    Window(converter)
    mainloop()
 