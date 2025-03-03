from pydantic import BaseModel as BM


class BaseModel(BM):
    model_config = {
        "arbitrary_types_allowed": True,
        "validate_assignment": True,
    }
