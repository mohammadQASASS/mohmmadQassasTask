from sqlalchemy import (Column, Float, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.engine import Engine

DATABASE_URL: str = "sqlite:///./mohmmad.db"

engine: Engine = create_engine(DATABASE_URL)

metadata: MetaData = MetaData()

car_table = Table(
    'car', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('model', String),  
    Column('year', Integer), 
    Column('price', Float),  
)