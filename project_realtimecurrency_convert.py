
import re
import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk

class RealtimeCurrencyConverter:
    def __init__(self,url):
        self.data = requests.get(url).json()
        self.currencies = self.data['conversion_rates']

    def convert(self, from_currency, to_currency, amount):
        intial_amount = amount
        # first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

class Display(tk.Tk):

    def __init__(self,c):
        tk.Tk.__init__(self)
        self.title = "MyProject"
        self.currency_converter = c
        self.geometry("500x300")

        # Label
        self.intro_label = Label(self,text='Real Time Currency Converter',fg='black',bg='antiquewhite2',relief=tk.RAISED,borderwidth=3)
        self.intro_label.config(font=('Aptos Display',16,'bold'))

        self.date_label = Label(self,text=f"1 Indian Rupee equals = {self.currency_converter.convert('INR','USD',1)}USD \n Last Updated : {self.currency_converter.data['time_last_update_utc'][0:16]}",relief=tk.GROOVE,borderwidth=5)

        self.intro_label.place(x = 88 , y = 5)
        self.date_label.place(x = 150 , y = 50)
        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%P')
        # restrictNumberOnly function will restrict the user from entering invalid number in Amount field. We have defined it later in the code
        self.amount_field = Entry(self,bd = 3, relief = tk.RIDGE, justify = tk.CENTER,validate='key', validatecommand=valid)
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 18, borderwidth = 3)
 
        # dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("INR") # by_default
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD") # by_default
 
        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
 
        # placing the dropdown and label fields
        self.from_currency_dropdown.place(x = 25, y= 120)
        self.amount_field.place(x = 30, y = 150)
        self.to_currency_dropdown.place(x = 335, y= 120)
        self.converted_amount_field_label.place(x = 340, y = 150)

        # Convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", command = self.perform) 
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x = 220, y = 135)

    def perform(self):
        # perform function is used to perform the actual currency conversion and display the converted amount
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()
 
        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 3)
     
        self.converted_amount_field_label.config(text = str(converted_amount))

    def restrictNumberOnly(self, string):
        # restrictNumberOnly function restricts the user from entering invalid number in Amount field
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))
    
if __name__ == '__main__':
    url = 'https://v6.exchangerate-api.com/v6/a5e8cc15ed9807a10db32a3c/latest/USD'
    c = RealtimeCurrencyConverter(url)
 
    Display(c)
    mainloop()