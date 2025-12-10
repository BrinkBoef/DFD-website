from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FundBase(BaseModel):
    fund_name: Optional[str] = None
    vintage: Optional[float] = None
    size: Optional[str] = None
    status: Optional[str] = None
    strategy: Optional[str] = None
    region: Optional[str] = None
    sector: Optional[str] = None


class Fund(FundBase):
    id: int
    company_id: int
    sub_strategy: Optional[str] = None
    industry: Optional[str] = None
    country_region: Optional[str] = None
    net_irr: Optional[float] = None
    qtl: Optional[str] = None
    invested: Optional[str] = None
    pct_of_tgt: Optional[float] = None
    raised: Optional[str] = None
    curr_inv: Optional[float] = None
    dpi: Optional[float] = None
    moic: Optional[float] = None
    rvpi: Optional[float] = None
    dry_powder: Optional[str] = None
    target: Optional[str] = None
    time_in_mkt: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PersonBase(BaseModel):
    name: str
    email: Optional[str] = None
    job_title: Optional[str] = None
    linkedin: Optional[str] = None


class Person(PersonBase):
    id: int
    company_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyBase(BaseModel):
    name: str


class Company(CompanyBase):
    id: int
    total_funds: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyWithFunds(Company):
    funds: List[Fund] = []

    class Config:
        from_attributes = True


class CompanyWithDetails(Company):
    funds: List[Fund] = []
    people: List[Person] = []

    class Config:
        from_attributes = True
