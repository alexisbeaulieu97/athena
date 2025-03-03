from typing import Dict, Optional
from athena.models import BaseModel
from athena.models.test_details import TestDetails


class TestFailedResult(BaseModel):
    message: Optional[str] = None
    details: Optional[Dict[str, TestDetails]] = None
