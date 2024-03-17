"""
The Pydantic schemas used in the API.
"""

from typing import Optional
from pydantic import BaseModel, Field
from config.format_instructions import SentimentCategories

class Verbatim(BaseModel):
    id: str = Field(...)
    text: str = Field(...)

class Classification(BaseModel):
    id: str = Field(...)
    classification: Optional[SentimentCategories] = Field(None, description="A list of relevant categories identified in the text.")
