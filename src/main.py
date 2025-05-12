from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from api import roll, statistics
from database import setup_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_table()
    yield

app = FastAPI(lifespan=lifespan)



app.include_router(roll.router)
app.include_router(statistics.router)



# @app.on_event("startup")
# async def on_startup():
#     await setup_table()


# @app.post("/add_rolls/", response_model=RollPublic)
# async def create_rolls(session: SessionDep, roll: RollCreate):
#     db_roll = Roll.model_validate(roll)
#     session.add(db_roll)
#     await session.commit()
#     return db_roll


# @app.get("/rolls/", response_model=list[RollPublic])
# async def read_rolls(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
#     ):
#     query = select(Roll).offset(offset).limit(limit)
#     rolls = await session.execute(query)
#     return rolls.scalars().all()





if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)