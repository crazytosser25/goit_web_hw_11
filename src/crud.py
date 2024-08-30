"""CRUD operations"""
from sqlalchemy.orm import Session
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
