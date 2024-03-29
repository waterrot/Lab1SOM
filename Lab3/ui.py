from tariefeenheden import Tariefeenheden
import tkinter as tk
import csv
import os
import json
import math
from datetime import datetime
from tkinter import messagebox
from pricing_table import PricingTable
from creditcard import CreditCard
from debitcard import DebitCard
from coin_machine import IKEAMyntAtare2000, coinMachine
from raise_error import Error
from ui_info import UIPayment, UIClass, UIWay, UIPayment, UIInfo




class UI(tk.Frame):
	PAYMENT_LOG_DIR = 'tvm_payment_logs'

	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.widgets()

	def log_payment(self, info:UIInfo, price, taxCollected):
		if info.payment == UIPayment.CreditCard:
			payment_method = 'CreditCard'
		elif info.payment == UIPayment.DebitCard:
			payment_method = 'DebitCard'
		elif info.payment == UIPayment.Cash:
			payment_method = 'Cash'
		else:
			payment_method = 'Unknown'

		# Logging payment information
		payment_info = {
			'ticket_id': '0001',  # can be implemented in the future
			'price': (str("{:.2f}".format(price))),
			'payment_method': payment_method,
			'tax_collected': taxCollected ,
			'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			'departure_station': info.from_station, 
			'arival_station': info.to_station,
			'travel_class': 'FirstClass' if info.travel_class == UIClass.FirstClass else 'SecondClass',
       		'ticket_type': 'Return' if info.way == UIWay.Return else 'Single',
			'machine_number': '0001'  # can be implemented in the future
		}

		# alter these two directory code snippets to for example send the logs to a remote server
		# Create the log directory if it doesn't exist
		if not os.path.exists(self.PAYMENT_LOG_DIR):
			os.makedirs(self.PAYMENT_LOG_DIR)

		# Append the payment information to the JSON file
		log_file_path = os.path.join(self.PAYMENT_LOG_DIR, 'payment_log.json')
		with open(log_file_path, 'a') as log_file:
			json.dump(payment_info, log_file)
			log_file.write('\n')

	def calculate_price(self, info: UIInfo) -> float:			
		
		# get number of tariefeenheden
		tariefeenheden: int = Tariefeenheden.get_tariefeenheden(info.from_station, info.to_station)

		# compute the column in the table based on choices
		table_column = 0
		if info.travel_class == UIClass.FirstClass:
			table_column = 1

		# compute price	
		priceTable: float = PricingTable.get_priceTable (table_column)
		
		# given price calculation by NS
		price = priceTable * 0.02 * tariefeenheden

		# double prices for returns
		if info.way == UIWay.Return:
			price *= 2

		return price
	
	def calculate_tax(self, priceCalc):
		#implement tax, 9% in the Netherlands
		price = priceCalc * 1.09
		# Round price to higher multiple of € 0,10
		price = math.ceil(price * 10) / 10

		# Calculate how much tax is collected so this can be logged
		taxCollected = (str("{:.2f}".format(price - priceCalc)))

		return price, taxCollected

	def calculate_payment_fees(self, price, info : UIInfo):
		# add 50 cents if paying with credit card
		if info.payment == UIPayment.CreditCard:
			price += 0.50
		return price

	def process_payment(self, info: UIInfo):
		priceBeforeTax = self.calculate_price(info)
		priceAfterTax, taxCollected = self.calculate_tax(priceBeforeTax)
		priceAfterFee = self.calculate_payment_fees(priceAfterTax, info)

		# first check for illegal route
		if info.from_station == info.to_station:
			e = Error()
			e.illegalRoute()
		else:
			self.log_payment(info, priceAfterFee, taxCollected)
			if info.payment == UIPayment.CreditCard:
				c = CreditCard()
				c.connect()
				ccid: int = c.begin_transaction(str("{:.2f}".format(priceAfterFee)))
				c.end_transaction(ccid)
				c.disconnect()
			elif info.payment == UIPayment.DebitCard:
				d = DebitCard()
				d.connect()
				dcid: int = d.begin_transaction(str("{:.2f}".format(priceAfterFee)))
				d.end_transaction(dcid)
				d.disconnect()
			elif info.payment == UIPayment.Cash:
				# access Ikea coin class with addapter (coinMachine)
				ikea_mynt_atare = IKEAMyntAtare2000()
				coin = coinMachine(ikea_mynt_atare)
				coin.start()
				coin.payment(str("{:.2f}".format(priceAfterFee)))
				coin.stop()


	def widgets(self):
		self.master.title("Ticket machine")
		menubar = tk.Menu(self.master)
		self.master.config(menu=menubar)

		fileMenu = tk.Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.on_exit)
		menubar.add_cascade(label="File", menu=fileMenu)

		# retrieve the list of stations
		data2 = Tariefeenheden.get_stations()

		stations_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
		stations_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
		# From station
		tk.Label(stations_frame, text = "From station:").grid(row=0, padx=5, sticky=tk.W)
		self.from_station = tk.StringVar(value=data2[0])
		tk.OptionMenu(stations_frame, self.from_station, *data2).grid(row=1, padx=5, sticky=tk.W)

		# To station
		tk.Label(stations_frame, text = "To station:").grid(row=0, column=1, sticky=tk.W)
		self.to_station = tk.StringVar(value=data2[0])
		tk.OptionMenu(stations_frame, self.to_station, *data2).grid(row=1, column=1, sticky=tk.W)

		ticket_options_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
		ticket_options_frame.pack(fill=tk.BOTH, expand=1, padx=10)

		# Class
		tk.Label(ticket_options_frame, text = "Travel class:").grid(row=1, sticky=tk.W)
		self.travel_class = tk.IntVar(value=UIClass.SecondClass.value)
		tk.Radiobutton(ticket_options_frame, text="First class", variable=self.travel_class, value=UIClass.FirstClass.value).grid(row=5, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="Second class", variable=self.travel_class, value=UIClass.SecondClass.value).grid(row=6, sticky=tk.W)

		# Way
		tk.Label(ticket_options_frame, text = "Way:").grid(row=7, sticky=tk.W)
		self.way = tk.IntVar(value=UIWay.OneWay.value)
		tk.Radiobutton(ticket_options_frame, text="One-way", variable=self.way, value=UIWay.OneWay.value).grid(row=8, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="Return", variable=self.way, value=UIWay.Return.value).grid(row=9, sticky=tk.W)

		
		payment_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
		payment_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

		# Payment
		tk.Label(payment_frame, text = "Payment:").grid(row=14, sticky=tk.W)
		self.payment = tk.IntVar(value=UIPayment.Cash.value)
		tk.Radiobutton(payment_frame, text="Cash", variable=self.payment, value=UIPayment.Cash.value).grid(row=15, sticky=tk.W)
		tk.Radiobutton(payment_frame, text="Credit Card", variable=self.payment, value=UIPayment.CreditCard.value).grid(row=16, sticky=tk.W)
		tk.Radiobutton(payment_frame, text="Debit Card", variable=self.payment, value=UIPayment.DebitCard.value).grid(row=17, sticky=tk.W)

		# Pay button
		tk.Button(self.master, text="Pay", command=self.on_click_pay).pack(side=tk.RIGHT, ipadx=10, padx=10, pady=10)

		# Illegal addition to this code :)
		# Raise error message box
		error_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
		error_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

		self.pack(fill=tk.BOTH, expand=1)
	
	def on_click_pay(self):
		self.process_payment(self.get_ui_info())

	def get_ui_info(self) -> UIInfo:
		return UIInfo(from_station=self.from_station.get(),
			to_station=self.to_station.get(),
			travel_class=self.travel_class.get(),
			way=self.way.get(),
			payment=self.payment.get())

	def on_exit(self):
		self.quit()

#endregion


def main():

	root = tk.Tk()
	UI(root)

	root.mainloop()


if __name__ == '__main__':
	main()
