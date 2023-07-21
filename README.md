# Checkout

## Requirements

Implement a checkout system similar to the one described in ["Back to the Checkout"](http://codekata.com/kata/kata09-back-to-the-checkout/).

- If 3 of Item A are purchased, the price for all 3 is £75.
- If 2 of Item B are purchased, the price for both is £35
- Special promotions:
  - If it's Friday there's a 50% off the checkout total
  - If the total basket price (after previous discounts) is over £150, the basket receives a discount of £20

## Scratch pad

- Checkout will be an object
- items: {item: count} = {"A": 1} 
- price: {item: price(int)} = {"A": 30}
- promotions (also an object): {item: promotion} = {"A": {3: 75}}, {"A": ?} 
  * downside: what about basket promotions? Will handle that when in scope

## Pairing first steps

Only applicable if doing this in a pair:

1. Share communication/pairing styles and set expectations
2. Discuss problem (questions, in scope, out of scope, expectations, assumptions, interface/data structures)
3. Make check list (loose basis for test cases)
4. Explain project setup
5. Check test setup
6. Begin TDD: red, green, refactor
7. Final tidy and refactor (readability, etc), have a good chat

## Checklist

- Create a Checkout
- Add an item to the checkout
- Add price to the checkout
- Calculate checkout total (single and multiple items)
- Add a promotion
  - If 3 of Item A are purchased, the price for all 3 is £75
  - If it's Friday there's a 50% off the checkout total
  - If 2 of Item B are purchased, the price for both is £35
  - If the total basket price (after previous discounts) is over £150, the basket receives a discount of £20
- Apply promotion to total
- Exceptions: 
  - if item doesn't have a price