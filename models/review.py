#!/usr/bin/python3
"""This is the review class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """This is the class for Review
    Attributes:
        place_id: place id
        user_id: user id
        text: review description
    """
    __tablename__ = "reviews"

    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)

# #!/usr/bin/python3
# """ Review module for the HBNB project """
# from models.base_model import BaseModel


# class Review(BaseModel):
#     """ Review classto store review information """
#     place_id = ""
#     user_id = ""
#     text = ""
