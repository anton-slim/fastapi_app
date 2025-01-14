from fastapi import APIRouter, HTTPException
from app.models import Basket, BasketCreate, BasketPublic, MushroomPublic, Message
from app.repository import BasketRepository, MushroomRepository

router = APIRouter(prefix="/baskets", tags=["baskets"])


@router.post("", response_model=Basket)
async def post_basket(item_in: BasketCreate):
    """
    Создать корзинку
    """
    item = Basket.model_validate(item_in.dict())
    BasketRepository().create(item)
    return item


@router.get("/{id}", response_model=BasketPublic)
async def get_basket(id: int):
    """
    Получить корзинку (по id), вместе с развернутой инфой по грибам
    """
    basket = BasketRepository().get(id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    mushrooms = MushroomRepository().get_by_ids(basket.mushrooms_ids)

    basket = BasketPublic.model_validate(basket.dict())
    basket.mushrooms = [MushroomPublic.model_validate(item.dict()) for item in mushrooms]
    return basket


@router.post("/{basket_id}/{mushroom_id}")
async def put_mushroom(basket_id: int, mushroom_id: int):
    """
    Положить в корзинку гриб
    """
    basket = BasketRepository().get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    mushroom = MushroomRepository().get(mushroom_id)
    if not mushroom:
        raise HTTPException(status_code=404, detail="Mushroom not found")

    if mushroom_id in basket.mushrooms_ids:
        raise HTTPException(status_code=404, detail="Mushroom already in a Basket")

    mushrooms = MushroomRepository().get_by_ids(basket.mushrooms_ids)
    basket_weight = MushroomRepository().get_mushrooms_weight(mushrooms)

    if basket_weight + mushroom.weight > basket.max_weight:
        raise HTTPException(status_code=401, detail="Could not put mushroom to basket, maximum weight exceeded")

    basket.add_mushroom(mushroom_id)
    return Message(message='Success')


@router.delete("/{basket_id}/{mushroom_id}")
async def delete_mushroom(basket_id: int, mushroom_id: int):
    """
    DELETE Удалить из корзинки гриб
    """
    basket = BasketRepository().get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    mushroom = MushroomRepository().get(mushroom_id)
    if not mushroom:
        raise HTTPException(status_code=404, detail="Mushroom not found")

    if mushroom_id not in basket.mushrooms_ids:
        raise HTTPException(status_code=404, detail="Mushroom not in a Basket")

    basket.getout_mushroom(mushroom_id)
    return Message(message='Success')


