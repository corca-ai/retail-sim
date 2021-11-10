from typing import Dict, Union, List, Tuple
import numpy as np

from .products import *

PROMOTION_PRDTS = "promotion_prdts"
CUSTOMER_NEED = "customer_need"
CUSTOMER_TEMPERATURE = "customer_temperature"
CUSTOMER_BUDGET = "customer_budget"

def sample_softmax(x : Union[List[float], np.ndarray], t : float = 1):
    """
    Sample from a softmax distribution.
    :param x: The input vector.
    :param t: The temperature.
    :return: The sampled value.
    """
    x = np.array(x)
    x = x - np.max(x)
    x = np.exp(x / t)
    x = x / np.sum(x)
    return np.random.choice(range(len(x)), p = x)


class RetailEnv:
    def __init__(
        self,
        prdt_config,
        customer_temperature_limit: float = 3.0,
        n_customer_limit : int = 100,
        budget_limit: float = 100.0,
        goal : str = "sale",
    ):
        self.prdt_config = prdt_config
        self.customer_temperature_limit = customer_temperature_limit
        self.budget_limit = budget_limit
        self.n_customer_limit = n_customer_limit
        self.goal = goal
        self.n_category = self.prdt_config[NUM_CATEGORIES]
        self.n_product = self.prdt_config[NUM_PRODUCTS]

        self.consumption_rate = [
            cat[CONSUMPTION_RATE] for cat in self.prdt_config[CATEGORIES]
        ]

        self.prdts = []

        for cats in self.prdt_config[CATEGORIES]:
            for prdt in cats[PRODUCTS]:
                self.prdts.append((prdt[PRDT_ID], prdt[PRDT_PRICE], prdt[PRDT_COST]))
                

        self.time_step: int = 0

    def _random_customer(self):
        cust = {
            CUSTOMER_NEED: [random.random() + x for x in self.consumption_rate],
            CUSTOMER_TEMPERATURE: random.random() * self.customer_temperature_limit,
            CUSTOMER_BUDGET: random.random() * self.budget_limit,
        }
        return cust

    def _customer_event(self, prdt_sale : Dict[str, float])-> List[str]:
        customer = self._random_customer()
        customer_budget = customer[CUSTOMER_BUDGET]
        customer_temperature = customer[CUSTOMER_TEMPERATURE]
        customer_need = np.array(customer[CUSTOMER_NEED])

        bought_history = []

        while customer_budget > 0:
            # select category
            score = customer_temperature * customer_need
            # score softmax
            category_idx = sample_softmax(score)

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
            at_list = np.array(at_list)
            # select product. update budget.
            prdt_idx = sample_softmax(at_list)
            cost = _category[PRODUCTS][prdt_idx][PRDT_PRICE]
            volume = _category[PRODUCTS][prdt_idx][PRDT_VOLUME]
            prdt_id = _category[PRODUCTS][prdt_idx][PRDT_ID]
            customer_budget -= cost
            

            # update customer need
            customer_need[category_idx] -= volume
            for idx, jdx in self.prdt_config[COMP_GRAPH]:
                if idx == category_idx:
                    customer_need[jdx] -= 0.5 * volume
            
            for idx, jdx in self.prdt_config[EXCH_GRAPH]:
                if jdx == category_idx:
                    customer_need[idx] += 0.5 * volume
            
            bought_history.append(prdt_id)

        return bought_history
                
        

    def step(self, action):
        promotion_dict : Dict[str, float] = action[PROMOTION_PRDTS]
        # WIP
        total_customers = random.randint(1, self.n_customer_limit)
        qty = {}
        for _ in range(total_customers):
            bought_history = self._customer_event(promotion_dict)
            for prdt_id in bought_history:
                if prdt_id in qty:
                    qty[prdt_id] += 1
                else:
                    qty[prdt_id] = 1

        profit = self.get_profit(qty, self.prdts)
        sale = self.get_sale(qty, self.prdts)

        if self.goal == "sale":
            reward = sale
        elif self.goal == "profit":
            reward = profit
        else:
            raise ValueError("Invalid goal")

        self.time_step += 1
        return qty, 
    
    @staticmethod
    def get_sale(qty : Dict[str, float], prdts : List[Tuple[str, float, float]]) -> float:
        sale = 0
        for prdt_id, qty in qty.items():
            for prdt in prdts:
                if prdt[0] == prdt_id:
                    sale  += qty * prdt[1]
                    break
        return sale

    @staticmethod
    def get_profit(qty : Dict[str, float], prdts : List[Tuple[str, float, float]]) -> float:
        profit = 0
        for prdt_id, qty in qty.items():
            for prdt in prdts:
                if prdt[0] == prdt_id:
                    profit += qty * (prdt[1] - prdt[2])
                    break
        return profit

    def render(self):
        # graphic render? to be implemented
        pass

    def reset(self):
        pass

