from enum import IntEnum

class UIClass(IntEnum):
	FirstClass = 1
	SecondClass = 2

class UIWay(IntEnum):
	OneWay = 1
	Return = 2


class UIPayment(IntEnum):
	DebitCard = 1
	CreditCard = 2
	Cash= 3

class UIInfo:
	from_station: str = ""
	to_station: str = ""
	travel_class: UIClass = UIClass.SecondClass
	way: UIWay = UIWay.OneWay
	payment: UIPayment.Cash

	def __init__(self, from_station: str, to_station: str, travel_class: UIClass, way: UIWay, payment: UIPayment):
		self.from_station = from_station
		self.to_station = to_station
		self.travel_class = travel_class
		self.way = way
		self.payment = payment
