import math

class PricingTable:

    @staticmethod
    def get_price(tariefeenheden: int, col: int) -> float:
        price = 0

        if col == 0:
            price = 2.10
        elif col == 1:
            price = 3.60
        else:
            raise Exception("Unknown column number")
        

        # given price calculation by NS
        priceCalc = price * 0.02 * tariefeenheden
    
        # Round price to higher multiple of € 0,10
        price = math.ceil(priceCalc * 10) / 10

        # Format it to print with an added zero, instead of e.g. 5,8 -> 5,80
        return price
