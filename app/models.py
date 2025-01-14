from pydantic import BaseModel, Field, computed_field
from pydantic.json_schema import SkipJsonSchema
from typing import Any, Optional
from datetime import datetime


class MushroomBase(BaseModel):
    name: str
    eatable: bool
    weight: int


class Mushroom(MushroomBase):
    id: int = 0
    datetime: float


class MushroomPublic(MushroomBase):
    id: int
    datetime: SkipJsonSchema[float] = Field(exclude=True)

    @computed_field(return_type=int)
    @property
    def freshness(self) -> int:
        if not self.datetime:
            return 0
        return int(datetime.now().timestamp()) - int(self.datetime)

    @freshness.setter
    def freshness(self, value):
        raise Exception('read only variable')


class MushroomCreate(MushroomBase):
    datetime: SkipJsonSchema[float] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if not self.datetime:
            self.datetime = datetime.now().timestamp()


# Properties to receive on item update
class MushroomUpdate(MushroomBase):
    name: str | None = None
    eatable: bool | None = None
    weight: int | None = None


class MushroomsPublic(BaseModel):
    data: list[MushroomPublic]
    count: int


class BasketBase(BaseModel):
    name: str
    max_weight: int


class Basket(BasketBase):
    id: int = 0
    mushrooms_ids: set = set()

    def add_mushroom(self, mushroom_id: int):
        self.mushrooms_ids.add(mushroom_id)

    def getout_mushroom(self, mushroom_id: int):
        self.mushrooms_ids.remove(mushroom_id)


class BasketPublic(BasketBase):
    id: int
    mushrooms_ids: SkipJsonSchema[set] = Field(exclude=True)
    mushrooms: Optional[list[MushroomPublic]] = None

    @computed_field(return_type=int)
    @property
    def weight(self) -> int:
        if len(self.mushrooms_ids) == 0:
            return 0
        return sum([item.weight for item in self.mushrooms])


class BasketCreate(BasketBase):
    pass


class Message(BaseModel):
    message: str
