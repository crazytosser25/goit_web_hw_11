"""CRUD operations"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_
import src.models as models
import src.schemas as schemas


def create_contact(
    base: Session,
    contact: schemas.ContactCreate
):
    base_contact = models.Contact(**contact.model_dump())
    base.add(base_contact)
    base.commit()
    base.refresh(base_contact)
    return base_contact

def get_contact(
    base: Session,
    id_: int
):
    return base.query(models.Contact).filter(models.Contact.id == id_).first()

def get_all_contacts(
    base: Session,
    skip: int = 0
):
    return base.query(models.Contact).offset(skip).all()

def search_contacts(
    base: Session,
    query: str
):
    return base.query(models.Contact).filter(
        or_(
            models.Contact.first_name.like(f"%{query}%"),
            models.Contact.last_name.like(f"%{query}%"),
            models.Contact.email.like(f"%{query}%")
        )
    ).all()

def get_upcoming_birthdays(
    base: Session
):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    # upcoming_birthdays = []
    # today = date.today()

    # for user, _ in self.data.items():
    #     birth_date = self.data[user].show_birthday()
    #     try:
    #         birthday_this_year = birth_date.replace(year=today.year)
    #         if birthday_this_year < today:
    #             birthday_this_year = birth_date.replace(year=today.year+1)
    #     except TypeError:
    #         continue

    #     if 0 <= (birthday_this_year - today).days <= days:
    #         birthday_this_year = adjust_for_weekend(birthday_this_year)
    #         congratulation_date_str = date_to_string(birthday_this_year)
    #         upcoming_birthdays.append({
    #             "name": user,
    #             "congratulation_date": congratulation_date_str
    #         })
    # if upcoming_birthdays:
    #     return stringify_birthdays(upcoming_birthdays)
    # return 'No birthdays exspected next week.'

    return base.query(models.Contact).filter(
        models.Contact.birthday >= today,
        models.Contact.birthday <= next_week
    ).all()

def update_contact(
    base: Session,
    id_: int,
    contact: schemas.ContactCreate
):
    base_ct = base.query(models.Contact).filter(models.Contact.id == id_).first()
    if base_ct:
        for key, value in contact.model_dump().items():
            setattr(base_ct, key, value)
        base.commit()
        base.refresh(base_ct)
    return base_ct

def delete_contact(
    base: Session,
    id_: int
):
    contact = base.query(models.Contact).filter(models.Contact.id == id_).first()
    if contact:
        base.delete(contact)
        base.commit()
    return contact
