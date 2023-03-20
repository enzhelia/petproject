from datetime import datetime
from enum import Enum
from typing import Optional, Type, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, root_validator


class TypeObject(Enum):
    file = "FILE"
    folder = "FOLDER"


class Objects(BaseModel):
    type: TypeObject = Field(description="Тип элемента - папка или файл")
    id: str = Field(
        default=lambda _: str(uuid4()), description="Уникальный идентификатор"
    )
    size: Optional[int] = Field(
        description="Целое число, для папки - это суммарный размер всех элементов."
    )
    url: Optional[str] = Field(description="Ссылка на файл. Для папок поле равно null.")
    parent_id: Optional[Union[str, UUID]] = Field(
        alias="parentId", description="id родительской папки"
    )
    date: datetime = Field(description="Время последнего обновления элемента.")
    children: Optional["Objects"] = Field(
        default=None,
        description="Список всех дочерних элементов. Для файлов поле равно null.",
    )

    @root_validator()
    @classmethod
    def validate_all_attributes(cls: Type["Objects"], value) -> None:
        url: str = value.get("url")
        type: TypeObject = value.get("type")
        size: int = value.get("size")
        children: Optional["Objects"] = value.get("children")
        if url is not None and type == TypeObject.folder:
            raise ValueError("not correct type. for folders that attribute is null")
        elif url is None and type == TypeObject.file:
            raise ValueError("not correct type. for files that attribute is not null")
        elif size == 0 and children is None and type == TypeObject.folder:
            raise ValueError("if folder doesn't have any children, size has to be zero")
        elif type == TypeObject.file and children is not None:
            raise ValueError("file doesn't have to any children")
        return value
