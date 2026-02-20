from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_extra_types.coordinate import Latitude
from pydantic_extra_types.coordinate import Longitude

class CategoriesDTO(BaseModel):
    name: str
    parent_name: str | None = None
    children: list["CategoriesDTO"]

class BaseInfoCompanyDTO(BaseModel):
    name: str
    number: PhoneNumber
    adress: str

class AllInfoCompanyDTO(BaseInfoCompanyDTO):
    category: "CategoriesDTO"
    latitude: Latitude
    longitude: Longitude





