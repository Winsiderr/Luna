from urllib.parse import unquote

from fastapi import APIRouter

from database.pydentick_schemes import AllInfoCompanyDTO, BaseInfoCompanyDTO
from database.CRUDDB import select_db_id, select_db_category, select_db_name, select_db_adress, select_db_nearby

router = APIRouter(prefix="/company", tags=["company_get"])


@router.get("id/{id}", response_model=AllInfoCompanyDTO)
def get_by_id(id: int):
    return select_db_id(id)

@router.get("nearby/nearby", response_model=list[BaseInfoCompanyDTO])
def get_nearby(lat: float, lon: float, radius: float = 10.0):
    return select_db_nearby(lat, lon, radius)

@router.get("name/{name}", response_model=AllInfoCompanyDTO)
def get_by_name(name: str):
    return select_db_name(name)

@router.get("adress/{adress}", response_model=list[BaseInfoCompanyDTO])
def get_by_adress(adress: str):
    return select_db_adress(unquote(adress))

@router.get("category_name/{category_name}", response_model=list[BaseInfoCompanyDTO])
def get_by_category(category_name: str):
    return select_db_category(category_name)




