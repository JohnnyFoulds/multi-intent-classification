"""
The Pydantic models for to be used for the format instructions.
"""


from typing import List
from pydantic import BaseModel, Field, validator

# the desired output schema
class SentimentCategory(BaseModel):
    category: str = Field(description="A category identified from the text. The category_definitions must be in the category_definitions list. Carefully consider the category definitions to decide if it is relevant to the verbatim.")
    reason: str = Field(description="Cite evidence for selecting the category. This is a short sentence or phrase from the text that supports the category selected. This is not a repeat of the category definition or the input text, it is for providing a valid reason why the text falls into the category.")
    relevance: float = Field(description="How relevant the category is for the text. This is a value between 0 and 1.")
    sentiment: str = Field(description="The sentiment of the identified category.", choices=["positive", "negative", "neutral"])

    # validate the sentiment
    @validator("sentiment")
    def sentiment_must_be_valid(cls, field):
        if field not in ["positive", "negative", "neutral"]:
            raise ValueError("sentiment must be one of 'positive', 'negative' or 'neutral'")
        return field

class SentimentCategories(BaseModel):
    categories: List[SentimentCategory] = Field(description="A list of relevant categories identified in the text. There can be a maximum of 3 categories identified and added to the list.")
