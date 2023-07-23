import pytest
from freezegun import freeze_time

from src.checkout import Checkout, ItemPromotion, CheckoutPromotion


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
    checkout.add_item_promotion(promotion)

    assert checkout.item_promotions["A"].sale_price == 75


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


def test_checkout_can_add_checkout_promotions(checkout):
    day_promotion = CheckoutPromotion("day_promo", "Friday", .5)
    checkout.add_checkout_promotion(day_promotion)

    assert "day_promo" in checkout.checkout_promotions


def test_checkout_calculates_total_with_checkout_promotion(checkout, make_it_friday):
    day_promotion = CheckoutPromotion("day_promo", "Friday", .5)
    checkout.add_checkout_promotion(day_promotion)

    checkout.add_item("A")
    checkout.add_item("B")

    assert checkout.calculate_total() == 25


def test_item_promotion_applies_promotion_rules_to_total(checkout):
    item_promo = ItemPromotion("A", 3, 75)
    discounted_total = item_promo.calculate_promotion(0, 30, 3)

    assert discounted_total == 75


def test_item_promotion_applies_promotion_rules_to_remaining_items(checkout):
    item_promo = ItemPromotion("A", 3, 75)
    discounted_total = item_promo.calculate_promotion(0, 30, 4)

    assert discounted_total == 105


def test_item_promotion_does_not_apply_promotion_rules(checkout):
    item_promo = ItemPromotion("A", 3, 75)
    total = item_promo.calculate_promotion(0, 30, 2)

    assert total == 60


def test_checkout_promotion_applies_promotion_rules_to_total(checkout, make_it_friday):
    checkout_promo = CheckoutPromotion({}, "Friday", .5)
    discounted_total = checkout_promo.calculate_promotion(100)

    assert discounted_total == 50


def test_checkout_promotion_does_not_apply_promotion_rules(checkout):
    checkout_promo = CheckoutPromotion({}, "Friday", .5)
    total = checkout_promo.calculate_promotion(100)

    assert total == 100
