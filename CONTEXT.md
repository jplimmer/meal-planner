# Meal Planner

A shared weekly dinner planner for a two-person household. This context covers
sourcing recipes from external sites and agreeing a set of them for the coming
week.

## Language

### Sourcing

**Provider**:
An external site that Recipes are obtained from, such as MindfulChef. Providers
are interchangeable — a Recipe's origin does not affect how it is planned with.
_Avoid_: source, scraper, integration

**Recipe**:
A dish that can be cooked, obtained from a Provider. Exists independently of any
particular week.
_Avoid_: meal, dish

**Recipe Cache**:
The household's own store of Recipes previously obtained from Providers. It is
the only thing consulted while planning; Providers never are.
_Avoid_: index, library, database

### Planning

**Draft**:
The single shared plan for the coming week, visible to both members of the
household. Exactly one exists at a time.
_Avoid_: session, plan, meal plan, week

**Slot**:
One position in the Draft, either filled by a Suggestion or empty. The number of
Slots is fixed when the Draft is created.
_Avoid_: place, spot, item

**Suggestion**:
A Recipe filling a Slot. Rejecting a Suggestion empties its Slot.
_Avoid_: candidate, pick, proposal, recommendation

**Rejection**:
A record that a Recipe was turned down while planning a Draft. It lasts as long
as that Draft, so a rejected Recipe is never suggested in it again.
_Avoid_: skip, veto, dismissal, swap

**Shopping List**:
The ingredients needed to cook the Draft's Suggestions, grouped by Recipe.
_Avoid_: grocery list, basket, ingredients
