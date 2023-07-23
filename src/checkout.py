import calendar
from datetime import date


class MultiItemPromo:
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


class DiscountDayPromo:
    def __init__(self, name, discount_day, percent_discount):
        self.name = name
        self.discount_day = discount_day
        self.percent_discount = percent_discount

    def calculate_promotion(self, total):
        today = calendar.day_name[date.today().weekday()]
        if today == self.discount_day:
            return int(total * self.percent_discount)
        return total


class DeductFromTotalPromo:
    def __init__(self, name, target_total, deduction_amount):
        self.name = name
        self.target_total = target_total
        self.deduction_amount = deduction_amount

    def calculate_promotion(self, total):
        if total > 150:
            total -= self.deduction_amount
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
        checkout = self.items.items()

        for item, count in checkout:
            if item in self.item_promotions:
                total = self.apply_item_promotion(count, item, total)
            else:
                total = self.sum_items(count, item, total)

        if self.checkout_promotions:
            total = self.apply_checkouts_promotion(total)

        return total

    def apply_checkouts_promotion(self, total):
        for promo in self.checkout_promotions:
            total = self.checkout_promotions[promo].calculate_promotion(total)
        return total

    def sum_items(self, count, item, total):
        total += self.prices[item] * count
        return total

    def apply_item_promotion(self, count, item, total):
        total = self.item_promotions[item].calculate_promotion(total, self.prices[item], count)
        return total

    def add_item_promotion(self, item_promotion):
        self.item_promotions[item_promotion.item_name] = item_promotion

    def add_checkout_promotion(self, checkout_promotion):
        self.checkout_promotions[checkout_promotion.name] = checkout_promotion
