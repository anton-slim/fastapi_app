from app.models import Mushroom, Basket
from app.core import singleton


@singleton
class MushroomRepository:
    mushrooms: dict[int, Mushroom] = {}
    mushrooms_next_id = 1

    def create(self, item: Mushroom):
        item.id = self.mushrooms_next_id
        self.mushrooms[item.id] = item
        self.mushrooms_next_id += 1

    def update(self, item_id: int, data: dict) -> Mushroom:
        item = self.get(item_id)
        if not item:
            raise Exception('item not found')
        return self.set(item_id, item.copy(update=data))

    def get(self, item_id: int) -> Mushroom | None:
        if item_id not in self.mushrooms:
            return None
        return self.mushrooms[item_id]

    def set(self, item_id: int, item: Mushroom) -> Mushroom | None:
        if item_id not in self.mushrooms:
            return None
        self.mushrooms[item_id] = item
        return item

    def get_all(self) -> list[Mushroom] | None:
        items = self.mushrooms.items()
        return [item for i, item in items] if len(items) > 0 else []

    def get_by_ids(self, ids: list) -> list[Mushroom] | None:
        items = self.mushrooms.items()
        if len(items) == 0:
            return []
        return [item for i, item in items if i in ids]

    @staticmethod
    def get_mushrooms_weight(mushrooms: list[Mushroom]):
        return sum([item.weight for item in mushrooms])


@singleton
class BasketRepository:
    baskets: dict[int, Basket] = {}
    baskets_next_id = 1

    def create(self, item: Basket):
        item.id = self.baskets_next_id
        self.baskets[item.id] = item
        self.baskets_next_id += 1

    def get(self, item_id: int) -> Basket | None:
        if item_id not in self.baskets:
            return None
        return self.baskets[item_id]
