from typing import Type, TypeVar, Any
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


def validate_model(model_cls: Type[T], raw_data: Any) -> T:
    """
    Generic model validation helper using Pydantic.
    Raises pydantic.ValidationError if raw_data fails schema.
    """
    return model_cls.model_validate(raw_data)
