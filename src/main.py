"""Main file"""
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import src.models as models
import src.schemas as schemas
import src.crud as crud
from src.database import DBSession, engine


logging.basicConfig(
    level=logging.INFO,
    format='line_num: %(lineno)s > %(message)s'
)

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
    return {"message": "Server alive."}

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    return crud.create_contact(base=db, contact=contact)

@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(
    skip: int = 0,
    db: Session = Depends(get_db)
):
    return crud.get_all_contacts(
        base=db,
        skip=skip
    )

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    db_contact = crud.get_contact(base=db, id_=contact_id)
    if db_contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(
    contact_id: int,
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    db_contact = crud.update_contact(
        base=db,
        id_=contact_id,
        contact=contact
    )
    if db_contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return db_contact

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
    return {"details": "Contact deleted"}
