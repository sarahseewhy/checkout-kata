import pytest

from src.checkout import Checkout


@pytest.fixture
def checkout():
    return Checkout()


def test_add_item_to_checkout(checkout):
    checkout.add_item("A")

    assert "A" in checkout.items


def test_add_item_to_checkout_and_record_count(checkout):
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.items["A"] == 2


def test_add_price_to_checkout(checkout):
    checkout.add_price("A", 30)

    assert checkout.prices["A"] == 30


def test_calculate_checkout_total(checkout):
    checkout.add_price("A", 30)
    checkout.add_price("B", 20)

    checkout.add_item("A")
    checkout.add_item("B")

    assert checkout.calculate_total() == 50


def test_add_promotion_to_checkout(checkout):
    checkout.add_promotion("A", 3, 75)

    assert checkout.promotions["A"].price == 75


def test_apply_promotion_to_checkout_total(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)

    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.calculate_total() == 75


def test_apply_multiple_discounts_to_checkout_total(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)

    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.calculate_total() == 150


def test_apply_multiple_discounts_to_checkout_total_including_remaining_items(checkout):
    checkout.add_promotion("A", 3, 75)
    checkout.add_price("A", 30)

    items = ["A", "A", "A", "A", "A", "A", "A"]
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")
    checkout.add_item("A")

    assert checkout.calculate_total() == 180
