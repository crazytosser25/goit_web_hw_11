"""Main file"""
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import src.models as models
import src.schemas as schemas
import src.crud as crud
from src.database import DBSession, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    base = DBSession()
    try:
        yield base
    finally:
        base.close()

@app.get("/api/healthchecker")
def root():
    result = {"message": "Server alive."}
    return result

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    result =  crud.create_contact(base=db, contact=contact)
    return result

@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(
    skip: int = 0,
    db: Session = Depends(get_db)
):
    result = crud.get_all_contacts(
        base=db,
        skip=skip
    )
    return result

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_contact(base=db, id_=contact_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return result

@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts(
    query: str,
    db: Session = Depends(get_db)
):
    result = crud.search_contacts(
        base=db,
        query=query
    )
    return result

@app.get("/contacts/upcoming_birthdays/", response_model=List[schemas.Contact])
def upcoming_birthdays(db: Session = Depends(get_db)):
    result = crud.get_upcoming_birthdays(base=db)
    return result

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(
    contact_id: int,
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    result = crud.update_contact(
        base=db,
        id_=contact_id,
        contact=contact
    )
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return result

@app.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = crud.delete_contact(
        base=db,
        id_=contact_id
    )
    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    result = {"details": "Contact deleted"}
    return result
