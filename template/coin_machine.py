from tkinter import messagebox

class IKEAMyntAtare2000:

	def starta(self):
		messagebox.showinfo(message = "Welkom to the NS coin counter. Continue to start the payment")

	def stoppa(self):
		messagebox.showinfo(message = "End of transaction, goodbye!")
		
	def betala(self, pris: int):
		messagebox.showinfo(message = f"Please pay €{pris}")


#adapter to english code
class coinMachine:
    def __init__(self, ikea_mynt_atare: IKEAMyntAtare2000):
        self.ikea_mynt_atare = ikea_mynt_atare

    def start(self):
        self.ikea_mynt_atare.starta()

    def stop(self):
        self.ikea_mynt_atare.stoppa()

    def payment(self, pris: int):
        self.ikea_mynt_atare.betala(pris)