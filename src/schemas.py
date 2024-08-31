from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone_number: str = Field(max_length=12)
    birthday: date
    other_info: Optional[str] = Field(max_length=250)

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
