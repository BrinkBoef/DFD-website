from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DealFlowData API",
    description="API for managing private equity companies and funds",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to DealFlowData API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/api/companies", response_model=List[schemas.Company])
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = Query(None, description="Search companies by name"),
    db: Session = Depends(get_db)
):
    """Get list of companies with optional search"""
    companies = crud.get_companies(db, skip=skip, limit=limit, search=search)
    return companies


@app.get("/api/companies/{company_id}", response_model=schemas.CompanyWithDetails)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get a specific company with all its funds and people"""
    company = crud.get_company_with_funds(db, company_id=company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@app.get("/api/funds", response_model=List[schemas.Fund])
def get_funds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get list of funds"""
    funds = crud.get_funds(db, skip=skip, limit=limit)
    return funds


@app.post("/api/companies", response_model=schemas.Company)
def create_company(company: schemas.CompanyBase, db: Session = Depends(get_db)):
    """Create a new company"""
    db_company = crud.get_company_by_name(db, name=company.name)
    if db_company:
        raise HTTPException(status_code=400, detail="Company already exists")
    return crud.create_company(db=db, company=company)


@app.post("/api/companies/{company_id}/people", response_model=schemas.Person)
def create_person(
    company_id: int,
    person: schemas.PersonBase,
    db: Session = Depends(get_db)
):
    """Add a person to a company"""
    company = crud.get_company(db, company_id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.create_person(db=db, person=person, company_id=company_id)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
