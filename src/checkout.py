import calendar
from datetime import date


class ItemPromotion:
    def __init__(self, item, unit, sale_price):
        self.item_name = item
        self.unit_count = unit
        self.sale_price = sale_price

    def calculate_promotion(self, sub_total, item_price, count):
        applied_promotions = count // self.unit_count
        sub_total += self.sale_price * applied_promotions
        remaining_items = count % self.unit_count
        sub_total += remaining_items * item_price
        return sub_total


class CheckoutPromotion:
    def __init__(self, name, criteria, discount):
        self.name = name
        self.criteria = criteria
        self.discount = discount

    def calculate_promotion(self, total):
        today = calendar.day_name[date.today().weekday()]
        if today in self.criteria:
            return int(total * self.discount)
        return total


class Checkout:
    def __init__(self):
        self.prices = {}
        self.items = {}
        self.checkout_promotions = {}
        self.item_promotions = {}

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
            promotions = self.item_promotions
            item_price = self.prices[item]
            if item in self.item_promotions:
                total = self.item_promotions[item].calculate_promotion(total, item_price, count)
            else:
                total += self.prices[item] * count

        if self.checkout_promotions:
            for promo in self.checkout_promotions:
                total = self.checkout_promotions[promo].calculate_promotion(total)

        return total

    def add_item_promotion(self, item_promotion):
        self.item_promotions[item_promotion.item_name] = item_promotion

    def add_checkout_promotion(self, checkout_promotion):
        self.checkout_promotions[checkout_promotion.name] = checkout_promotion
