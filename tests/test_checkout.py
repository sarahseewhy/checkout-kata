import pytest

from src.checkout import Checkout, PromotionCalculator, Promotion


@pytest.fixture
def checkout():
    return Checkout()


def test_add_item_to_checkout(checkout):
    checkout.add_item("A")

    assert "A" in checkout.items


def test_record_item_count_in_checkout(checkout):
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.items["A"] == 2


def test_add_price_to_checkout(checkout):
    checkout.add_price("A", 30)

    assert checkout.prices["A"] == 30


def test_calculate_checkout_total_for_multiple_different_items(checkout):
    checkout.add_price("A", 30)
    checkout.add_price("B", 20)

    checkout.add_item("A")
    checkout.add_item("B")

    assert checkout.calculate_total() == 50


def test_add_promotion_to_checkout(checkout):
    checkout.add_promotion("A", 3, 75)

    assert checkout.promotions["A"].price == 75


def test_apply_single_promotion_to_odd_number_of_items(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)

    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.calculate_total() == 75


def test_apply_single_promotion_to_even_number_of_items(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)

    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.calculate_total() == 105


def test_apply_multiple_promotions_to_even_number_of_items(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)

    even_number_of_items = ["A", "A", "A", "A", "A", "A"]

    for item in even_number_of_items:
        checkout.add_item(item)

    assert checkout.calculate_total() == 150


def test_apply_multiple_promotions_to_odd_number_of_items(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)

    odd_number_of_items = ["A", "A", "A", "A", "A", "A", "A"]

    for item in odd_number_of_items:
        checkout.add_item(item)

    assert checkout.calculate_total() == 180


def test_apply_promotion_to_different_items(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)
    checkout.add_price("B", 20)

    items = ["A", "A", "A", "B"]

    for item in items:
        checkout.add_item(item)

    assert checkout.calculate_total() == 95

def test_create_promotion_calculator():
    promo_calculator = PromotionCalculator()


def test_promotion_calculator_calculates_multi_item_promotion(checkout):
    item_count = 3
    item = "A"
    item_price = 30
    starting_total = 0
    promotion = Promotion(3, 75)
    promotions = {item: promotion}
    promotion_calculator = PromotionCalculator()

    discounted_total = promotion_calculator.calculate_multi_item_promotion(item, item_count, item_price, starting_total, promotions)

    assert discounted_total == 75
