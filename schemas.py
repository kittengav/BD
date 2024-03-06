from pydantic import BaseModel


class AviaryType(BaseModel):
    id: int = None
    name: str

    @classmethod
    def from_row(cls, row):
        return cls.model_validate({"id": row[0], "name": row[1]})

    class Config:
        __table_name__ = "aviary_types"
        __pk_field__ = "id"
        __fk_fields__ = dict()


class Aviary(BaseModel):
    id: int = None
    name: str
    type_id: int

    @classmethod
    def from_row(cls, row):
        return cls.model_validate({"id": row[0], "name": row[1], "type_id": row[2]})

    class Config:
        __table_name__ = "aviaries"
        __pk_field__ = "id"
        __fk_fields__ = {"type_id": AviaryType}


class AnimalType(BaseModel):
    id: int = None
    name: str
    description: str

    @classmethod
    def from_row(cls, row):
        return cls.model_validate({"id": row[0], "name": row[1], "description": row[2]})

    class Config:
        __table_name__ = "animal_types"
        __pk_field__ = "id"
        __fk_fields__ = dict()


class Animal(BaseModel):
    id: int = None
    name: str
    description: str
    type_id: int
    aviary_id: int | None = None

    @classmethod
    def from_row(cls, row):
        return cls.model_validate({"id": row[0], "name": row[1], "description": row[2], "type_id": row[3]})

    class Config:
        __table_name__ = "animals"
        __pk_field__ = "id"
        __fk_fields__ = {"type_id": AnimalType, "aviary_id": Aviary}
