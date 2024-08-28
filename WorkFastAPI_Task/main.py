from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import and_, delete, insert, select, update, func
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import NoResultFound
from database import car_table, engine 


app = FastAPI()

def get_db():
    with engine.begin() as conn:
        yield conn


class CountryCreate(BaseModel):
    name: str
    iso_code: str
    continent: Optional[str] = None
    population: Optional[int] = None
    capital: Optional[str] = None

class CountryResponse(CountryCreate):
    id: int

@app.get("/cars/", response_model=List[CountryResponse], status_code=status.HTTP_200_OK)
async def get_cars(
    id: Optional[int] = None,
    name: Optional[str] = None,
    iso_code: Optional[str] = None,
    continent: Optional[str] = None,
    db: Connection = Depends(get_db) 
) -> List[CountryResponse]:
    if id is not None:
        selected_country = db.execute(select(car_table).where(car_table.c.id == id)).mappings().first()
        if selected_country is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
        return [CountryResponse(**selected_country)]
    if name is not None:
        selected_country = db.execute(select(car_table).where(func.lower(car_table.c.name) == func.lower(name))).mappings().first()
        if selected_country is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
        return [CountryResponse(**selected_country)]
    
    if iso_code is not None:
        selected_country = db.execute(select(car_table).where(car_table.c.iso_code == iso_code)).mappings().first()
        if selected_country is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
        return [CountryResponse(**selected_country)]
    
    if continent is not None:
        selected_cars = db.execute(select(car_table).where(car_table.c.continent == continent)).mappings().fetchall()
        if not selected_cars:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cars found for the given continent")
        return [CountryResponse(**country) for country in selected_cars]
    
    selected_cars = db.execute(select(car_table)).mappings().fetchall()
    return [CountryResponse(**country) for country in selected_cars]


@app.post("/cars/", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
async def create_country(country: CountryCreate, db: Connection = Depends(get_db)) -> CountryResponse:
       db.execute(insert(car_table).values(**country.dict()))
       new_country = db.execute(select(car_table).where(car_table.c.iso_code == country.iso_code)).mappings().first()
       if new_country is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve the new country")
       return CountryResponse(**new_country)


@app.put("/cars/{car_id}", response_model=CountryResponse, status_code=status.HTTP_200_OK)
async def update_country(car_id: int, country: CountryCreate, db: Connection = Depends(get_db)) -> CountryResponse:
    country_to_update = db.execute(select(car_table).where(car_table.c.id == car_id)).mappings().first()
    if country_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")

    db.execute(update(car_table).where(car_table.c.id == car_id).values(**country.dict()))  # Use .dict()
    updated_country = db.execute(select(car_table).where(car_table.c.id == car_id)).mappings().first()
    return CountryResponse(**updated_country)


@app.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(car_id: int, db: Connection = Depends(get_db)):
    country_to_delete = db.execute(select(car_table).where(car_table.c.id == car_id)).mappings().first()
    if country_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    db.execute(delete(car_table).where(car_table.c.id == car_id))
    return  
