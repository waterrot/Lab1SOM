from tkinter import messagebox
from ui_info import UIPayment, UIClass, UIWay, UIDiscount, UIPayment, UIInfo 

class Error():
    def illegalRoute(self):
        messagebox.showinfo(message = "Its not possible to travel to the same station")


