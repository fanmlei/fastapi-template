from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.background import BackgroundTask

from .codes import BusinessResponseCode

DataType = TypeVar("DataType")


class UnifiedResponseModel(BaseModel, Generic[DataType]):
    code: BusinessResponseCode | None = Field(BusinessResponseCode.SUCCESS, description="响应码")
    message: str | None = Field(None, description="提示信息")
    data: DataType | None = Field(None, description="响应数据")



class UnifiedJSONResponse(JSONResponse):
    def __init__(
        self,
        code: BusinessResponseCode | None = BusinessResponseCode.SUCCESS,
        message: str | None = None,
        data: Any = None,
        status_code: int = 200,
        headers: dict | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        content = UnifiedResponseModel(code=code, message=message, data=data).model_dump(exclude_none=True)
        super().__init__(
            content=jsonable_encoder(content),
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )
