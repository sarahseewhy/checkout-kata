# Checkout

1. [Requirements](#requirements)
2. [Checklists](#checklists)
3. [Reflections](#reflections)

## Requirements

Implement a checkout system similar to the one described in ["Back to the Checkout"](http://codekata.com/kata/kata09-back-to-the-checkout/).

- If 3 of Item A are purchased, the price for all 3 is £75.
- If 2 of Item B are purchased, the price for both is £35
- Special promotions:
  - If it's Friday there's a 50% off the checkout total
  - If the total basket price (after previous discounts) is over £150, the basket receives a discount of £20

## Checklists

### Pairing

Only applicable if doing this in a pair:

1. Share communication/pairing styles and set expectations
2. Discuss problem (questions, in scope, out of scope, expectations, assumptions, interface/data structures)
3. Make check list (loose basis for test cases)
4. Explain project setup
5. Check test setup
6. Begin TDD: red, green, refactor
7. Final tidy and refactor (readability, etc), have a good chat

### Code

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

## Reflections

#### Lessons in extendability

After I fulfilled the first requirement (creating a multi-buy promotion) I wanted to extract the promotion logic into its own object to remove responsibility from the Checkout. I also knew I wanted to implement a checkout promotion and thought I'd need a calculator of some kind to handle both types of promotions.

I initially chose not to use the existing object (ItemPromotion) because I'd hoped to keep that object "dumb". I had an internal assumption/belief (maybe from my Java days) that objects shouldn't contain logic, instead logic should be handled by objects purpose-built for action.

This led me down a thorny path of creating a PromotionCalculator which contained all the promotion logic and for a brief moment a PromotionLibrary (yikes!).

However, I didn't like how complex the code was becoming and how difficult it would be to extend it further as I added more promotions. I stumbled on a [Martin Fowler blog on polymorphism](https://www.refactoring.com/catalog/replaceConditionalWithPolymorphism.html) which helped me check my assumption about objects not containing logic.

I'm so glad I did this! Once I shifted the promotion logic to the ItemPromotion class extending the code was a breeze.

#### Checkout improvements

I think the Checkout class could be made smaller. It's still doing a bit more than I'd like (although most of the methods are small and created more for readability). 

The Checkout should just add items and calculate the total.

Should the Checkout know about promotions? I'm not sure. It fits for right now but perhaps it could talk to another object whose sole purpose is to know about promotions.

#### Lambdas

I'm not adverse to if/else statements or for-loops, in some ways I find them easier to read. However, I think it would've been interesting to apply some lambda logic to the code.

I'd like to see the impact on readability but also lambdas could make the code a bit cleaner. If/else statements run the risk of creating unintended side effects.

#### Exceptions

I didn't get to this item on the checklist and I wish I had :(