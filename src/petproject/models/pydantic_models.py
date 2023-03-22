from datetime import datetime
from enum import Enum
from typing import Any, Union
from uuid import uuid4

from pydantic import BaseModel, Field

# TODO добавить валидацию данных 


class TypeObject(Enum):
    file = "FILE"
    folder = "FOLDER"


class BaseElement(BaseModel):
    type: TypeObject = Field(description="Тип элемента - папка или файл")
    id: str = Field(
        default=lambda _: str(uuid4()), description="Уникальный идентификатор"
    )
    date: datetime = Field(description="Время последнего обновления элемента.")
    parent_id: str | None = Field(
        alias="parentId", description="id родительской папки"
    )
    
    
    
class Folder(BaseElement):  
    size: int = Field(
        description="Целое число, для папки - это суммарный размер всех элементов.", default=0
    )
    url: None = Field(default=None)
    
    children: list[Union['Folder', 'File']] = Field(
        default=[],
        description="Список всех дочерних элементов. Для файлов поле равно null.",
    )

class File(BaseElement):
    size: int = Field(
        description="Целое число, для папки - это суммарный размер всех элементов.", ge=1
    )
    url: str = Field(description='Ссылка на файл. Для папок поле равно null') 
    
    children: None = Field(default=None)
    

correct_type: dict[str, Any] = {
    "FILE": File,
    "FOLDER": Folder,
}

    # @root_validator()
    # @classmethod
    # def validate_all_attributes(cls: Type["Objects"], value) -> None:
    #     url: str = value.get("url")
    #     type: TypeObject = value.get("type")
    #     size: int = value.get("size")
    #     children: Optional["Objects"] = value.get("children")
    #     if url is not None and type == TypeObject.folder:
    #         raise ValueError("not correct type. for folders that attribute is null")

    #     elif url is None and type == TypeObject.file:
    #         raise ValueError("not correct type. for files that attribute is not null")

    #     elif size == 0 and children is None and type == TypeObject.folder:
    #         raise ValueError("if folder doesn't have any children, size has to be zero")

    #     elif type == TypeObject.file and children != None:
    #         raise ValueError("file doesn't have to any children")
    #     return value
