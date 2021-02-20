"""Shopping cart optimization
Author: Leonidas Ioannidis, 2021, leonidas.yovan@gmail.com

Problem description:

This is an example of a shopping cart optimization for a series of everyday
cleaning products.

We need to buy a series of cleaning products. There is a capacity constraint
to respect, which corresponds to our storage room's area in cm2.
Each product can last a certain amount of time given in months.
We want to minimize our visits to the market. In other words our goal is to
maximize the time we need to make another visit to the market.

The same problem can serve as part of a inventory management system, where
storing space is limited.

It is modeled as a minmax problem with an integer variable for each product.

Porblem Formulation:
P: number of products
c_p: area that p ocupies in cm3
d_p: time in moths that product p lasts

max         z
subj. to    z <= sum(d_p * x_p) for_all x
            sum(c_p * x_p)  # capacity constraint
            x_p in {1..2..inf}  # integer quantities

"""

from pyscipopt import Model, quicksum

P = 7
prods = range(P)
c = {0: 0.30,  # bleach
     1: 0.27,  # dishwashing detergent
     2: 0.29,  # dishwasher detergent
     3: 0.28,  # salt
     4: 0.12,  # rinse aid
     5: 0.11,  # shampoo
     6: 0.32}  # soap

d = {0: 3,
     1: 2,
     2: 2.2,
     3: 5,
     4: 11,
     5: 1.1,
     6: 1.7}

K = 3.4

m = Model("Supermarket")

x = {}
for p in prods:
    x[p] = m.addVar(vtype='I', lb=1, name=f'x_{p}')

z = m.addVar(vtype='C', name='min_time')

# Constraints
m.addCons(quicksum(c[p] * x[p] for p in prods) <= K)

# min term to maximize in objective
for p in prods:
    m.addCons(z <= d[p] * x[p])

m.setObjective(z, 'maximize')

m.optimize()

print(f"OBJ value: {m.getObjVal()}")

for p in prods:
    print(f"x_{p}: {round(m.getVal(x[p]), 2)}")
