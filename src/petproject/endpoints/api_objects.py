from typing import Union

from fastapi import APIRouter, HTTPException, status
from fastapi_utils.cbv import cbv
from pydantic import ValidationError

from ..local_db.data import objects as data
from ..models.pydantic_models import File, Folder, correct_type

router = APIRouter()


@cbv(router)
class ApiDisk:
    @router.get(
        "/nodes/{id}",
        description="Получить информацию об элементе по идентификатору. При получении информации о папке также предоставляется информация о её дочерних элементах. для пустой папки поле children равно пустому массиву, а для файла равно null. размер папки - это суммарный размер всех её элементов. Если папка не содержит элементов, то размер равен 0. При обновлении размера элемента, суммарный размер папки, которая содержит этот элемент, тоже обновляется.",
    )
    def get_object(self, id: str):
        try:
            object_new = [correct_type[x["type"]].parse_obj(x) for x in data]
        except ValidationError as _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Validation Failed"
            )

        current_element = list(filter(lambda x: x.id == id, object_new))

        if len(current_element) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        elif len(current_element) != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Validation Failed"
            )

        element = current_element[0]
        if isinstance(element, Folder):
            element.children, element.size = self.get_children(element)
        return element.dict()

    def get_children(
        self, element: Folder
    ) -> tuple[list[Union["Folder", "File"]], int]:
        object_new: list[Union["Folder", "File"]] = [
            correct_type[x["type"]].parse_obj(x) for x in data
        ]
        current_element: list[Union["Folder", "File"]] = list(
            filter(lambda x: x.parent_id == element.id, object_new)
        )
        size = 0
        for children in current_element:
            if isinstance(children, Folder):
                children.children, children.size = self.get_children(children)
                size += children.size
            else:
                size += children.size
        return current_element, size

    @router.delete("/delete/{id}", description="")
    def delete_object(self, id: str):
        pass


# @app.get("/items", response_model=List[Item])
# def get_all_items():
#     return item_values


# @app.get("/item", response_model=List[Item])
# def read_item(item_id: UUID):
#     current_item = list(filter(lambda user: user.item_id == item_id, item_values))
#     return current_item
