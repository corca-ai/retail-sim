import numpy as np
import torch

from products import *

PROMOTION_PRDTS = "promotion_prdts"
CUSTOMER_NEED = "customer_need"
CUSTOMER_TEMPERATURE = "customer_temperature"
CUSTOMER_BUDGET = "customer_budget"


class RetailEnv:
    def __init__(
        self,
        prdt_config,
        customer_temperature_limit: float = 3.0,
        budget_limit: float = 100.0,
    ):
        self.prdt_config = prdt_config
        self.customer_temperature_limit = customer_temperature_limit
        self.budget_limit = budget_limit
        self.n_category = self.prdt_config[NUM_CATEGORIES]
        self.n_product = self.prdt_config[NUM_PRODUCTS]

        self.consumption_rate = [
            cat[CONSUMPTION_RATE] for cat in self.prdt_config[CATEGORIES]
        ]
        self.time_step: int = 0

    def _random_customer(self):
        cust = {
            CUSTOMER_NEED: [random.random() + x for x in self.consumption_rate],
            CUSTOMER_TEMPERATURE: random.random() * self.customer_temperature_limit,
            CUSTOMER_BUDGET: random.random() * self.budget_limit,
        }
        return cust

    def _customer_event(self, prdt_sale):
        customer = self._random_customer()
        customer_budget = customer[CUSTOMER_BUDGET]
        customer_temperature = customer[CUSTOMER_TEMPERATURE]
        customer_need = torch.tensor(customer[CUSTOMER_NEED])

        while customer_budget > 0:
            # select category
            score = torch.softmax(customer_temperature * customer_need)
            category_idx = torch.multinomial(score, 1).item()

            # select product within that cateogry
            # lazy implementation. will update later
            # TODO: update later
            _category = self.prdt_config[CATEGORIES][category_idx]
            at_list = [
                max(
                    _prdt[PRDT_TREND] * self.time_step
                    + prdt_sale[_prdt[PRDT_ID]] * _prdt[PRDT_PRICE_ELASTICITY],
                    (random.random() < _prdt[PRDT_LOYALTY]) * 100,
                )
                for _prdt in _category[PRODUCTS]
            ]
            at_list = torch.tensor(at_list)

            # TODO: select product, update customer budget, customer need, and return recipt.

            pass

    def step(self, action):
        promotion_list = action[PROMOTION_PRDTS]
        # WIP
        self.time_step += 1

    def render(self):
        pass

    def reset(self):
        pass

