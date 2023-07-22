class Promotion:
    def __init__(self, unit, price):
        self.unit_count = unit
        self.price = price


class PromotionsCalculator:
    @staticmethod
    def calculate_item_promotion(count, item, promotions, total, item_price):
        applied_promotions = count // promotions[item].unit_count
        total += promotions[item].price * applied_promotions
        remaining_items = count % promotions[item].unit_count
        total += remaining_items * item_price
        return total


class Checkout:
    def __init__(self):
        self.promotions = {}
        self.prices = {}
        self.items = {}

    def add_item(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1

    def add_price(self, item, price):
        self.prices[item] = price

    def calculate_total(self):
        total = 0

        for item, count in self.items.items():
            promotions = self.promotions
            promotions_calculator = PromotionsCalculator()
            if item in promotions:
                item_price = self.prices[item]
                total = promotions_calculator.calculate_item_promotion(count, item, promotions, total, item_price)
            else:
                total += self.prices[item] * count

        return total

    def add_promotion(self, item, unit, price):
        promotion = Promotion(unit, price)
        self.promotions[item] = promotion
