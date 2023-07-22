class Promotion:
    def __init__(self, unit, price):
        self.unit_count = unit
        self.price = price


class PromotionCalculator:
    @staticmethod
    def calculate_multi_item_promotion(item, count, item_price, sub_total, promotions):
        applied_promotions = count // promotions[item].unit_count
        sub_total += promotions[item].price * applied_promotions
        remaining_items = count % promotions[item].unit_count
        sub_total += remaining_items * item_price
        return sub_total


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
        promo_calculator = PromotionCalculator()
        for item, count in self.items.items():
            promotions = self.promotions
            if item in promotions:
                total = promo_calculator.calculate_multi_item_promotion(item, count, self.prices[item], total, promotions)
            else:
                total += self.prices[item] * count

        return total

    def add_promotion(self, item, unit, price):
        promotion = Promotion(unit, price)
        self.promotions[item] = promotion
