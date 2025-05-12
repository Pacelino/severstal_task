from database import get_session  
from dependencies import SessionDep
from models import Roll, RollPublic
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from datetime import datetime

from sqlalchemy import and_, between, func, select

""" 
Модуль для обработы статистических данных по рулонам

получение статистики по рулонам за определённый период:
– количество добавленных рулонов;
– количество удалённых рулонов;
– средняя длина, вес рулонов, находившихся на складе в этот период;
– максимальная и минимальная длина и вес рулонов, находившихся на
складе в этот период;
– суммарный вес рулонов на складе за период;
– максимальный и минимальный промежуток между добавлением и
удалением рулона.
"""

router = APIRouter(
    prefix = "/statistic",
    tags=["Статистика"]
)

@router.get("/get_created_rolls")
async def get_added_roll(
    session: SessionDep
):
    query = (
        select(Roll)
    )
    rolls = await session.execute(query)
    count_rolls = len(rolls.all())
    return {"count_rolls": count_rolls}
    
@router.get("/get_deleted_rolls")
async def get_deleted_rolls(session: SessionDep):
    query = (
        select(Roll).where(Roll.deleted_at != None)
    )
    
    roll_db = await session.execute(query)
    count_deleted_rolls = len(roll_db.all())
    return {"count_deleted_rolls": count_deleted_rolls}


@router.get("/get_avg_length_and_weight")
async def get_avg_lenght_and_weight(
    session: SessionDep,
    date_from: Annotated[datetime, Query()],
    date_at: Annotated[datetime, Query()]
    ):
    query = (
        select(
            func.avg(Roll.length).label("avg_length"), 
            func.avg(Roll.weight).label("avg_weight")
            )
        .select_from(Roll)
        .where(Roll.created_at.between(date_from, date_at))
    )
    result = await session.execute(query)
    stats = result.first() # <class 'sqlalchemy.engine.row.Row'>
    return {
        "avg_length": stats.avg_length,
        "avg_weight": stats.avg_weight
    }
    
@router.get("/get_min_max_lenght_weight")
async def min_max_lenght_weight(
    session: SessionDep,
    date_from: Annotated[datetime, Query()],
    date_at: Annotated[datetime, Query()]
    ):
    query = (
        select(
            func.max(Roll.length).label("max_length"), 
            func.min(Roll.length).label("min_lenght"),
            func.max(Roll.weight).label("max_weight"),
            func.min(Roll.weight).label("min_weight")
        )
        .where(Roll.created_at.between(date_from, date_at))
    )
    
    result = await session.execute(query)
    stats = result.first()
    content =  {
        "max_length": stats.max_length,
        "min_lenght": stats.min_lenght,
        "max_weight": stats.max_weight,
        "min_weight": stats.min_weight,
    }
    return content


@router.get("/get_sum_weight")
async def get_sum_weight(
    session: SessionDep,
    date_from: Annotated[datetime, Query()],
    date_at: Annotated[datetime, Query()]
):
    query = (
        select(
            func.sum(Roll.weight), 
        )
        .where(Roll.created_at.between(date_from, date_at))
    )
    roll_db = await session.execute(query)
    result = roll_db.first()[0]
    print(result)
    return {"sum_weight": result}


@router.get("/get_min_max_time_interval")
async def get_min_max_time_interval(
    session: SessionDep,
):
    try:
        # Вычисляем разницу между deleted_at и created_at в секундах
        interval_expr = func.extract('epoch', Roll.deleted_at - Roll.created_at)
        
        query = (
            select(
                func.min(interval_expr).label("min_interval_seconds"),
                func.max(interval_expr).label("max_interval_seconds")
            )
            .where(Roll.deleted_at.isnot(None))
        )
        result = await session.execute(query)
        stats = result.one_or_none()  # Получаем одну строку или None
        print(stats)
        if not stats:
            return {
                "message": "Нет данных об удаленных рулонах"
            }

        return {
            "min_interval_seconds": stats.min_interval_seconds,
            "max_interval_seconds": stats.max_interval_seconds,
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении статистики: {str(e)}"
        )