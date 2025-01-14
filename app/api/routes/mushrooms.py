from fastapi import APIRouter, HTTPException
from app.models import Mushroom, MushroomCreate, MushroomPublic, MushroomsPublic, MushroomUpdate, Message
from app.repository import MushroomRepository

router = APIRouter(prefix="/mushrooms", tags=["mushrooms"])


@router.post("", response_model=MushroomPublic)
async def post_mushroom(item_in: MushroomCreate):
    """
    Создать гриб
    """
    item = Mushroom.model_validate(item_in.dict())
    MushroomRepository().create(item)
    return item


@router.put("/{id}", response_model=MushroomPublic)
async def put_mushroom(id: int, item_in: MushroomUpdate):
    """
    Обновить гриб
    """
    item = MushroomRepository().get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_dict = item_in.model_dump(exclude_unset=True)
    item = MushroomRepository().update(id, update_dict)
    return item


@router.get("/{id}", response_model=MushroomPublic)
async def get_mushroom(id: int):
    """
    Получить конкретный гриб (по id)
    """
    item = MushroomRepository().get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("", response_model=MushroomsPublic)
async def get_all_mushrooms():
    """
    Получить список всех грибов
    """
    data = [MushroomPublic.model_validate(item.dict()) for item in MushroomRepository().get_all()]
    resp = {'data': data, 'count': len(data)}
    return MushroomsPublic.model_validate(resp)
