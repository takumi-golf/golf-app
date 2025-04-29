from pydantic import BaseModel
from typing import Any, Dict
 
class ErrorResponse(BaseModel):
    detail: str | Dict[str, Any] 