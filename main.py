from enum import Enum

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from schemas import *
from dependencies import get_object, get_objects, update_object, create_object, delete_object


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ModelName(str, Enum):
    animals = "animals"
    aviaries = "aviaries"
    animal_types = "animal_types"
    aviary_types = "aviary_types"


Entities = {
    "animals": Animal,
    "aviaries": Aviary,
    "animal_types": AnimalType,
    "aviary_types": AviaryType
}


@app.get("/api/v1/{model_name}")
async def get_list(model_name: ModelName, offset: int = 0, limit: int = 10, order_by: str = None):
    serializer = Entities[model_name]
    s_fields = serializer.__fields__.keys()
    if order_by is not None:
        if "," in order_by:
            for o in order_by.split(","):
                if o not in s_fields:
                    order_by = None
                    break
            order_by = order_by.split(',')
        elif order_by not in s_fields:
            order_by = None
        else:
            order_by = (order_by, )
    result = await get_objects(serializer, offset, limit, order_by)
    return JSONResponse(result, status_code=200)


@app.get("/api/v1/{model_name}/{item_id}")
async def get_retrieve(model_name: ModelName, item_id: int):
    serializer = Entities[model_name]
    result = await get_object(serializer, item_id)
    return JSONResponse(result, status_code=200)


@app.post("/api/v1/{model_name}")
async def create(model_name: ModelName, request: Request):
    serializer: BaseModel = Entities[model_name]
    _object = serializer.model_validate_json(await request.body())
    result = await create_object(_object)
    return JSONResponse(result, status_code=201)


@app.put("/api/v1/{model_name}")
async def update(model_name: ModelName, request: Request):
    serializer: BaseModel = Entities[model_name]
    _object = serializer.model_validate_json(await request.body())
    result = await update_object(_object)
    return JSONResponse(result, status_code=200)


@app.delete("/api/v1/{model_name}/{item_id}")
async def delete(model_name: ModelName, item_id: int):
    serializer: BaseModel = Entities[model_name]
    result = await delete_object(serializer, item_id)
    return JSONResponse({"id": result}, status_code=200)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/animals")
async def animals(request: Request):
    return templates.TemplateResponse(request=request, name="animals.html")


@app.get("/animal_types")
async def animal_types(request: Request):
    return templates.TemplateResponse(request=request, name="animal_types.html")


@app.get("/aviaries")
async def aviaries(request: Request):
    return templates.TemplateResponse(request=request, name="aviaries.html")


@app.get("/aviary_types")
async def aviary_types(request: Request):
    return templates.TemplateResponse(request=request, name="aviary_types.html")



