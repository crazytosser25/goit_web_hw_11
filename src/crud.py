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
            models.Contact.first_name.ilike(f"%{query}%"),
            models.Contact.last_name.ilike(f"%{query}%"),
            models.Contact.email.ilike(f"%{query}%")
        )
    ).all()

def get_upcoming_birthdays(
    base: Session
):
    days = 7
    today = datetime.now().date()

    upcoming_birthdays = []
    contacts = base.query(models.Contact).all()
    for contact in contacts:
        birth_date = contact.birthday
        try:
            birthday_this_year = birth_date.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birth_date.replace(year=today.year+1)
        except TypeError:
            continue

        if 0 <= (birthday_this_year - today).days <= days:
            if birthday_this_year.weekday() >= 5:
                days_ahead = 0 - birthday_this_year.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                birthday_this_year += timedelta(days=days_ahead)
            contact.birthday = birthday_this_year
            upcoming_birthdays.append(contact)
    if upcoming_birthdays:
        return upcoming_birthdays
    return []

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
