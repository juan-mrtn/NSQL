from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, List, Annotated
from enum import Enum
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class HouseEnum(str, Enum):
    MARVEL = "Marvel"
    DC = "DC"

class SuperheroBase(BaseModel):
    name: str = Field(...)
    real_name: Optional[str] = None
    appearance_year: int = Field(...)
    house: HouseEnum = Field(...)
    biography: str = Field(...)
    equipment: Optional[List[str]] = []
    images: List[str] = Field(..., min_length=1)

class SuperheroCreate(SuperheroBase):
    pass

class SuperheroUpdate(BaseModel):
    name: Optional[str] = None
    real_name: Optional[str] = None
    appearance_year: Optional[int] = None
    house: Optional[HouseEnum] = None
    biography: Optional[str] = None
    equipment: Optional[List[str]] = None
    images: Optional[List[str]] = None

class SuperheroInDB(SuperheroBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Spider-Man",
                "real_name": "Peter Parker",
                "appearance_year": 1962,
                "house": "Marvel",
                "biography": "Bitten by a radioactive spider...",
                "equipment": ["Web-shooters"],
                "images": ["https://example.com/spidey.jpg"]
            }
        }
    )
