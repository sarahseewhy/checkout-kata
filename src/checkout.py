import calendar
from datetime import date


class ItemPromotion:
    def __init__(self, item, unit, sale_price):
        self.item_name = item
        self.unit_count = unit
        self.price = sale_price


class PromotionCalculator:
    @staticmethod
    def calculate_item_promotion(sub_total, item, item_price, count, promotion):
        applied_promotions = count // promotion[item].unit_count
        sub_total += promotion[item].price * applied_promotions
        remaining_items = count % promotion[item].unit_count
        sub_total += remaining_items * item_price
        return sub_total

    @staticmethod
    def calculate_checkout_promotion(sub_total, promotion):
        today = calendar.day_name[date.today().weekday()]
        if today in promotion.criteria:
            return int(sub_total * promotion.discount)
        return sub_total


class CheckoutPromotion:
    def __init__(self, promo_type, criteria, discount):
        self.promo_type = promo_type
        self.criteria = criteria
        self.discount = discount


class PromotionLibrary:
    def __init__(self):
        self.checkout_promotions = {}
        self.item_promotions = {}

    def add_item_promotion(self, item_promotion):
        self.item_promotions[item_promotion.item_name] = item_promotion

    def add_checkout_promotion(self, checkout_promotion):
        self.checkout_promotions[checkout_promotion.promo_type] = checkout_promotion


class Checkout:
    def __init__(self):
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
        promo_library = PromotionLibrary()

        total = self.apply_item_promotions(promo_calculator, promo_library, total)

        if promo_library.checkout_promotions:
            total = self.apply_checkout_promotions(promo_calculator, promo_library, total)

        return total

    @staticmethod
    def apply_checkout_promotions(promo_calculator, promo_library, total):
        for promo in promo_library.checkout_promotions:
            promotion = promo_library.checkout_promotions[promo]
            total = promo_calculator.calculate_checkout_promotion(total, promotion)
        return total

    def apply_item_promotions(self, promo_calculator, promo_library, total):
        for item, count in self.items.items():
            promotions = promo_library.item_promotions
            item_price = self.prices[item]
            if item in promotions:
                total = promo_calculator.calculate_item_promotion(total, item, item_price, count, promotions)
            else:
                total += self.prices[item] * count
        return total
