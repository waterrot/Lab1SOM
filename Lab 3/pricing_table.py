class PricingTable:

    @staticmethod
    def get_priceTable(col: int) -> float:
        priceTable = 0

        if col == 0:
            priceTable = 2.10
        elif col == 1:
            priceTable = 3.60
        else:
            raise Exception("Unknown column number")
        
        return priceTable