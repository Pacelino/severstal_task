from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from sqlalchemy import and_, between, select
from contextlib import asynccontextmanager

from database import setup_table
from models import Roll, RollPublic, RollCreate, RollDeleted
from dependencies import SessionDep
from scheme import RollScheme


router = APIRouter(
    prefix="/api"
)

# @router.on_event("startup")
# async def on_startup():
#     await setup_table()


@router.post("/add_rolls/", response_model=RollPublic)
async def create_rolls(session: SessionDep, roll: RollCreate):
    db_roll = Roll.model_validate(roll)
    session.add(db_roll)
    await session.commit()
    await session.refresh(db_roll)
    return db_roll


@router.get("/rolls/", response_model=list[RollPublic])
async def read_rolls(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    ):
    query = select(Roll).offset(offset).limit(limit)
    rolls = await session.execute(query)
    return rolls.scalars().all()


@router.patch("/remove_from_warehouse/{roll_id}", response_model=RollPublic)
async def remove_from_warehouse(
    roll_id: int, 
    roll: RollDeleted, 
    session: SessionDep
    ):
    roll_db = await session.get(Roll, roll_id)
    if not roll_db:
        raise HTTPException(status_code=404, detail=f"Roll not found by id={roll_id}")
    roll_data = roll.model_dump(exclude_unset=True)
    roll_db.sqlmodel_update(roll_data)
    session.add(roll_db)
    await session.commit()
    await session.refresh(roll_db)
    
    return roll_db


@router.get("/filter_rolls/", response_model=list[RollPublic])
async def filter_rolls(
    filters_data: Annotated[RollScheme, Query()],
    session: SessionDep,
):
    query = select(Roll)
    conditions = []

    
    if filters_data.id_from is not None and filters_data.id_to is not None:
        if filters_data.id_from >= filters_data.id_to:
            raise HTTPException(status_code=404, detial="id_from cannot be greater than id_to")
        conditions.append(between(Roll.id, filters_data.id_from, filters_data.id_to))
    else: 
        if filters_data.id_from is not None:
            conditions.append(Roll.id >= filters_data.id_from)
        if filters_data.id_to is not None:
            conditions.append(Roll.id <= filters_data.id_to)

    if filters_data.length_from is not None and filters_data.length_to is not None:
        if filters_data.length_from >= filters_data.length_to:
            raise HTTPException(status_code=404, detial="length_from cannot be greater than length_to")
        conditions.append(between(Roll.length, filters_data.length_from, filters_data.length_to))
    else: 
        if filters_data.length_from is not None:
            conditions.append(Roll.length >= filters_data.length_from)
        if filters_data.length_to is not None:
            conditions.append(Roll.length <= filters_data.length_to)
            
    if filters_data.weight_from is not None and filters_data.weight_to is not None:
        if filters_data.weight_from >= filters_data.weight_to:
            raise HTTPException(status_code=404, detial="weight_from cannot be greater than weight_to")
        conditions.append(between(Roll.weight, filters_data.weight_from, filters_data.weight_to))
    else: 
        if filters_data.length_from is not None:
            conditions.append(Roll.length >= filters_data.length_from)
        if filters_data.length_to is not None:
            conditions.append(Roll.length <= filters_data.length_to)

    # Фильтрация по дате создания
    if filters_data.created_at is not None:
        conditions.append(Roll.created_at == filters_data.created_at)

    # Фильтрация по дате удаления
    if filters_data.deleted_at is not None:
        conditions.append(Roll.deleted_at == filters_data.deleted_at)

    if conditions:
        query = query.where(and_(*conditions))

    roll_db = await session.execute(query)
    return roll_db.scalars().all()
    
    