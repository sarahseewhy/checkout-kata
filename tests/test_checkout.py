import pytest

from src.checkout import Checkout


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
