import pytest
from freezegun import freeze_time

from src.checkout import Checkout, PromotionCalculator, ItemPromotion, CheckoutPromotion, PromotionLibrary


@pytest.fixture
def checkout():
    checkout = Checkout()
    checkout.add_price("A", 30)
    checkout.add_price("B", 20)
    return checkout


@pytest.fixture()
def make_it_friday():
    most_recent_friday = '2023-07-21'
    with freeze_time(most_recent_friday):
        yield


def test_add_item_to_checkout():
    checkout = Checkout()

    checkout.add_item("A")

    assert "A" in checkout.items


def test_record_item_count_in_checkout():
    checkout = Checkout()

    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.items["A"] == 2


def test_add_price_to_checkout():
    checkout = Checkout()

    checkout.add_price("A", 30)
    checkout.add_price("B", 20)

    assert checkout.prices["A"] == 30


def test_calculate_checkout_total_for_multiple_different_items(checkout):
    checkout.add_item("A")
    checkout.add_item("B")

    assert checkout.calculate_total() == 50


def test_add_item_promotion_to_promotion_library(checkout):
    promotion = ItemPromotion("A", 3, 75)
    promo_library = PromotionLibrary()
    promo_library.add_item_promotion(promotion)

    assert promo_library.item_promotions["A"].price == 75


def test_apply_single_promotion_to_odd_number_of_items(checkout):
    promotion = ItemPromotion("A", 3, 75)
    checkout.add_item_promotion(promotion)

    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.calculate_total() == 75


def test_apply_single_promotion_to_even_number_of_items(checkout):
    promotion = ItemPromotion("A", 3, 75)
    checkout.add_item_promotion(promotion)

    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.calculate_total() == 105


def test_apply_multiple_promotions_to_even_number_of_items(checkout):
    promotion = ItemPromotion("A", 3, 75)
    checkout.add_item_promotion(promotion)

    six_items = ["A", "A", "A", "A", "A", "A"]

    for item in six_items:
        checkout.add_item(item)

    assert checkout.calculate_total() == 150


def test_apply_multiple_promotions_to_odd_number_of_items(checkout):
    promotion = ItemPromotion("A", 3, 75)
    checkout.add_item_promotion(promotion)

    seven_items = ["A", "A", "A", "A", "A", "A", "A"]

    for item in seven_items:
        checkout.add_item(item)

    assert checkout.calculate_total() == 180


def test_apply_promotion_to_different_items(checkout):
    promotion = ItemPromotion("A", 3, 75)
    checkout.add_item_promotion(promotion)

    items = ["A", "A", "A", "B"]

    for item in items:
        checkout.add_item(item)

    assert checkout.calculate_total() == 95


def test_promotion_calculator_calculates_multi_item_promotion(checkout):
    item_count = 3
    item = "A"
    item_price = 30
    starting_total = 0
    promotion = ItemPromotion("A", 3, 75)
    promotions = {item: promotion}
    promotion_calculator = PromotionCalculator()

    discounted_total = promotion_calculator.calculate_item_promotion(starting_total, item, item_price, item_count,
                                                                     promotions)

    assert discounted_total == 75


def test_checkout_can_add_checkout_promotions(checkout):
    day_promotion = CheckoutPromotion("day_of_the_week", "Friday", .5)
    promo_library = PromotionLibrary()
    promo_library.add_checkout_promotion(day_promotion)

    assert "day_of_the_week" in promo_library.checkout_promotions


def test_promotion_calculator_applies_day_of_the_week_promotion_to_a_total(checkout, make_it_friday):
    promo_calculator = PromotionCalculator()
    day_promotion = CheckoutPromotion("day_of_the_week", "Friday", .5)
    total_before_discount = 100
    checkout.add_checkout_promotion(day_promotion)

    total = promo_calculator.calculate_checkout_promotion(total_before_discount, day_promotion)

    assert total == 50


def test_promotion_calculator_does_not_apply_day_of_the_week_promotion_to_a_total(checkout):
    promo_calculator = PromotionCalculator()
    day_promotion = CheckoutPromotion("day_of_the_week", "Friday", .5)
    total_before_discount = 100
    checkout.add_checkout_promotion(day_promotion)

    total = promo_calculator.calculate_checkout_promotion(total_before_discount, day_promotion)
    assert total == total_before_discount


def test_checkout_calculates_total_with_checkout_promotion(checkout, make_it_friday):
    day_promotion = CheckoutPromotion("day_of_the_week", "Friday", .5)
    checkout.add_checkout_promotion(day_promotion)

    checkout.add_item("A")
    checkout.add_item("B")

    assert checkout.calculate_total() == 25
