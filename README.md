# Shopping Cart Optimization
A MILP formulation for shopping cart optimization.

## Problem description:

This is an example of a shopping cart optimization for a series of everyday
cleaning products. The same problem can serve as part of a inventory management system,
where storing space is limited.

We need to buy a series of cleaning products. There is a capacity constraint,
 which corresponds to our storage room's area in cm2.
Each product can serve us for a certain amount of time given in months.
We want to minimize our visits to the market. In other words our goal is to
maximize the time we need to make the next visit to the market.

It is modeled as a minmax mixed-integer linear programming problem with integer variables.

## Objective
The objective of the problem is to reduce our visits to the supermarket.

## Porblem Formulation:

### Requirements
- Python 3.6+
- pyscipopt
- SCIP Optimization Suite