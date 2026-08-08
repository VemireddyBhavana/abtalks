from typing import List, Optional
from pydantic import BaseModel, Field


class TopicModel(BaseModel):
    id: str = Field(..., description="Unique topic identifier")
    title: str = Field(..., description="Topic title")
    category: str = Field(..., description="Topic category or domain")


class DayModel(BaseModel):
    day_number: int = Field(..., ge=1, description="Day index starting at 1")
    module_id: str = Field(..., description="Associated parent module ID")
    title: str = Field(..., description="Day title")
    description: str = Field(..., description="Detailed description of day content")
    topics: List[TopicModel] = Field(default_factory=list, description="Topics covered in the day")
    learning_objectives: List[str] = Field(default_factory=list, description="Target learning goals")
    tools_used: List[str] = Field(default_factory=list, description="Technologies or tools introduced")


class ModuleModel(BaseModel):
    id: str = Field(..., description="Unique module identifier")
    title: str = Field(..., description="Module title")
    description: str = Field(..., description="Module description")


class CurriculumModel(BaseModel):
    curriculum_id: str = Field(..., description="Curriculum identifier")
    title: str = Field(..., description="Curriculum title")
    version: str = Field(default="1.0.0", description="Curriculum specification version")
    modules: List[ModuleModel] = Field(default_factory=list, description="Module definitions")
    days: List[DayModel] = Field(default_factory=list, description="Daily curriculum schedule")
