from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel

""" 
Хранятся модели баз данных
"""

""" 
Рулон:
id
длина, 
вес, 
дата добавления, 
дата удаления
"""

class RollBase(SQLModel):
    length: int | None = Field(index=True, gt=0)
    weight: int | None = Field(index=True, gt=0)
    
    
class Roll(RollBase, table=True, extend_existing=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    deleted_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    

class RollCreate(RollBase):
    pass
      
class RollDeleted(RollBase):
    deleted_at: datetime = Field(default=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))

    
class RollPublic(RollBase):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    deleted_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    