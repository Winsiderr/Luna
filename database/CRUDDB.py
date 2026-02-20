from fastapi import HTTPException

from database.database_up import session_factory
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, aliased
from database.schemes import Company, Category
from database.pydentick_schemes import AllInfoCompanyDTO, BaseInfoCompanyDTO


def select_db_id(id: int)-> AllInfoCompanyDTO:
    with session_factory() as session:
        result = session.execute(
            select(Company)
            .where(Company.id == id)
            .options(
                selectinload(Company.category).selectinload(Category.parent),
                selectinload(Company.category).selectinload(Category.children)
            )
        )
        company = result.scalars().first()
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")
        return AllInfoCompanyDTO.model_validate(company, from_attributes=True)

def select_db_name(name: str) -> AllInfoCompanyDTO:
    with session_factory() as session:
        result = session.execute(
            select(Company)
            .where(Company.name == name)
            .options(
                selectinload(Company.category).selectinload(Category.parent),
                selectinload(Company.category).selectinload(Category.children)
            )
        )
        company = result.scalars().first()
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")
        return AllInfoCompanyDTO.model_validate(company, from_attributes=True)

def select_db_adress(adress: str) -> list[BaseInfoCompanyDTO]:
    with session_factory() as session:
        result = session.execute(
            select(Company)
            .where(Company.adress == adress)
            .options(
                selectinload(Company.category).selectinload(Category.parent),
                selectinload(Company.category).selectinload(Category.children)
            )
        )
        company = result.scalars().all()
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")
        return [BaseInfoCompanyDTO.model_validate(c, from_attributes=True) for c in company]

def select_db_category(category_name: str) -> list[BaseInfoCompanyDTO]:
    with session_factory() as session:
        category_cte = (
            select(Category.id)
            .where(Category.name == category_name)
            .cte("category_tree", recursive=True)
        )
        child_alias = aliased(Category)
        recursive_part = select(child_alias.id).where(
            child_alias.parent_id == category_cte.c.id
        )
        category_cte = category_cte.union_all(recursive_part)

        stmt = select(Company).where(
            Company.category_id.in_(select(category_cte.c.id))
        )
        result = session.execute(stmt)
        companies = result.scalars().all()
        if companies is None:
            raise HTTPException(status_code=404, detail="Company not found")
        return [BaseInfoCompanyDTO.model_validate(c, from_attributes=True) for c in companies]

def select_db_nearby(lat: float, lon: float, radius_km: float) -> list[BaseInfoCompanyDTO]:
    with session_factory() as session:
        distance_expr = 6371 * func.acos(
            func.least(
                1,
                func.greatest(
                    -1,
                    func.cos(func.radians(lat))
                    * func.cos(func.radians(Company.latitude))
                    * func.cos(func.radians(Company.longitude) - func.radians(lon))
                    + func.sin(func.radians(lat))
                    * func.sin(func.radians(Company.latitude)),
                ),
            )
        )
        stmt = select(Company).where(distance_expr <= radius_km)
        result = session.execute(stmt)
        companies = result.scalars().all()
        return [BaseInfoCompanyDTO.model_validate(c, from_attributes=True) for c in companies]