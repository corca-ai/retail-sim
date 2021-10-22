# Retailer's Sale Data Simulation

Retail-Sim is python package to easily create synthetic dataset of retaile store.


## Simulation Model

Simulator consists of `env`, that generates retailer store simulated data.


# Modelling PLAN

### Products

Create fake products and relationship between them. Relationship between products (Cateogries, to be more precise) consists of "exchangability", "complementarity". Products have many attributes, such as

  * Base Price
  * Base Cost
  * Volume
  * Attractiveness
  * Category
  * Price elasticity 
  * Relative Consumption rate
  * Loyalty

Volume implies how much satisfaction it provieds to the customer (How much of a need it subtracts). Volume is proportional to price, which can be set with vol_price_corr. 

Products are discretely grouped by some category. Each category has attribute "consumption rate", "general trend", and "seasonal trend". In real life, products such as fresh food, tissues, bottled water would have high consumption rate. General trend is random linear-like trend, seasonal trend is trend of sales that has period of 1 year. In real life, product like icecream would have winter-oriented seasonal trend.  


### Customers

Every customer has random set of "needs". Just as real life, you might need shampoo, pair of scissors, and some spagetti souce(All of these are considered as one category) Customers will try to fill those needs. As it happens in real life, customers are encourged to buy the product that both satisfy the needs and has a high preference.

### Product's Total Attractiveness

Every product comes with the Attractiveness attribute. If it has higher attractiveness, it is more likely to sell. However,

  * If the product is on discount, it will become more attractive.
  * If the product is on discount and it is advertised to be, it will become even more attractive.
  * If the product has high loyalty, it will have very high attractiveness to some customers.
  * There might be some general trend on the attractiveness.

  Therefore during simulation, total attractiveness will be defined as:

  $$Total = max(\text{Attractiveness} + \text{elasticity} * \text{discounted rate}, B(loyalty) * infty)$$
  

### Customer's state transition

Customers will buy with n budget, where n is pareto distibuted among all customers.
They will randomly pick a category depending on their current need distribution. After that, they will buy a product in that category, based on the products' total attractiveness. Buying that product will subtract the customer's need of that category by Volume's amount. 


