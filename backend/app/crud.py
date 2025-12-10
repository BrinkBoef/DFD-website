from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from . import models, schemas


def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()


def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()


def get_companies(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
):
    query = db.query(models.Company)

    if search:
        query = query.filter(models.Company.name.ilike(f"%{search}%"))

    return query.order_by(models.Company.name).offset(skip).limit(limit).all()


def get_company_with_funds(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()


def create_company(db: Session, company: schemas.CompanyBase):
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def create_fund(db: Session, fund_data: dict, company_id: int):
    db_fund = models.Fund(company_id=company_id, **fund_data)
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund


def get_funds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Fund).offset(skip).limit(limit).all()


def update_company_fund_count(db: Session, company_id: int):
    company = get_company(db, company_id)
    if company:
        fund_count = db.query(func.count(models.Fund.id)).filter(
            models.Fund.company_id == company_id
        ).scalar()
        company.total_funds = fund_count
        db.commit()
        db.refresh(company)
    return company


def create_person(db: Session, person: schemas.PersonBase, company_id: int):
    db_person = models.Person(**person.dict(), company_id=company_id)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person
