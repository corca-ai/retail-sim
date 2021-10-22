import math
import random


NUM_CATEGORIES = "num_categories"
NUM_PRODUCTS = "num_products"

CATEGORIES = "categories"
GLOBAL_TREND = "global_trend"
SEASONAL_TREND = "seasonal_trend"
CONSUMPTION_RATE = "consumption_rate"

PRDT_ID = "prdt_id"
PRDT_TREND = "prdt_trend"
PRDT_LOYALTY = "prdt_loyalty"
PRDT_PRICE = "prdt_price"
PRDT_PRICE_ELASTICITY = "prdt_price_elasticity"
PRDT_VOLUME = "prdt_volume"

PRODUCTS = "products"
CATEGORY_NAME = "category_name"

COMP_GRAPH = "comp_graph"
EXCH_GRAPH = "exch_graph"


class ProductGenerator:
    def __init__(
        self,
        n_category: int = 5,
        cateogry_size: int = 10,
        consumption_rate_limit: float = 0.1,
        global_trend_limit: float = 0.1,
        seasonal_trend_limit: float = 0.1,
        n_max_complementory: int = 1,
        n_max_exchangeability: int = 1,
        prdt_trend_limit: float = 0.1,
        prdt_loyalty_limit: float = 0.2,
        prdt_price_limit: float = 0.1,
        prdt_elasticity_limit: float = 0.1,
        prdt_volume_price_noise: float = 0.1,
    ):
        self.n_category = n_category
        self.cateogry_size = cateogry_size
        self.consumption_rate_limit = consumption_rate_limit
        self.global_trend_limit = global_trend_limit
        self.seasonal_trend_limit = seasonal_trend_limit
        self.n_max_complementory = n_max_complementory
        self.n_max_exchangeability = n_max_exchangeability
        self.prdt_trend_limit = prdt_trend_limit
        self.prdt_loyalty_limit = prdt_loyalty_limit
        self.prdt_price_limit = prdt_price_limit
        self.prdt_elasticity_limit = prdt_elasticity_limit
        self.prdt_volume_price_noise = prdt_volume_price_noise

        self.cfgs = {
            NUM_CATEGORIES: self.n_category,
            NUM_PRODUCTS: 0,
            CATEGORIES: [],
            EXCH_GRAPH: [],
            COMP_GRAPH: [],
        }
        for idx in range(self.n_category):

            _cat = {
                CATEGORY_NAME: f"CAT_{str(hash(idx))}",
                PRODUCTS: [self._random_prdt(jdx) for jdx in range(self.cateogry_size)],
                GLOBAL_TREND: random.uniform(
                    -self.global_trend_limit, self.global_trend_limit
                ),
                SEASONAL_TREND: [
                    random.uniform(
                        -self.seasonal_trend_limit, self.seasonal_trend_limit
                    )
                    for _ in range(4)
                ],
                CONSUMPTION_RATE: random.uniform(
                    -self.consumption_rate_limit, self.consumption_rate_limit
                ),
            }
            self.cfgs[CATEGORIES].append(_cat)
            self.cfgs[NUM_PRODUCTS] += self.cateogry_size

            for _ in range(
                random.randint(0, self.n_max_complementory + self.n_max_exchangeability)
            ):
                _rand = random.randint(1, self.n_category - 1) + idx % self.n_category
                if random.random() < 0.5:
                    self.cfgs[COMP_GRAPH].append((idx, _rand))
                else:
                    self.cfgs[EXCH_GRAPH].append((idx, _rand))

    def _random_prdt(self, idx: int):
        _prdt = {
            PRDT_ID: f"PRDT_{str(hash(idx))}",
            PRDT_TREND: random.uniform(-self.prdt_trend_limit, self.prdt_trend_limit),
            PRDT_LOYALTY: random.uniform(0, self.prdt_loyalty_limit),
            PRDT_PRICE: random.uniform(-self.prdt_price_limit, self.prdt_price_limit),
            PRDT_PRICE_ELASTICITY: random.uniform(
                -self.prdt_elasticity_limit, self.prdt_elasticity_limit
            ),
        }
        _vol = _prdt[PRDT_PRICE] + random.uniform(
            -self.prdt_volume_price_noise, self.prdt_volume_price_noise
        )
        _prdt[PRDT_VOLUME] = math.exp(_vol)

        return _prdt

