from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    total_funds = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    funds = relationship("Fund", back_populates="company", cascade="all, delete-orphan")
    people = relationship("Person", back_populates="company", cascade="all, delete-orphan")


class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Basic Information
    fund_name = Column(String, index=True)
    vintage = Column(Float)
    size = Column(String)
    status = Column(String)
    fund_inception_date = Column(String)

    # Strategy & Focus
    strategy = Column(String)
    sub_strategy = Column(String)
    sector = Column(String)
    industry = Column(Text)
    region = Column(String)
    country_region = Column(String)

    # Financial Metrics
    net_irr = Column(Float)
    qtl = Column(String)
    invested = Column(String)
    pct_of_tgt = Column(Float)
    raised = Column(String)
    curr_inv = Column(Float)
    dpi = Column(Float)
    amt = Column(String)
    pct = Column(Float)
    dry_powder = Column(String)
    hist_inv = Column(Float)
    moic = Column(Float)
    management_fee = Column(String)
    pic = Column(Float)

    # Quartile Rankings
    first_qtl = Column(Float)
    second_qtl = Column(Float)
    third_qtl = Column(Float)
    fourth_qtl = Column(Float)
    na_qtl = Column(Float)
    total_qtl = Column(Float)

    # Additional Metrics
    rvpi = Column(Float)
    target = Column(String)
    time_in_mkt = Column(String)
    tot_inv = Column(Float)
    unrealized = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="funds")


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    name = Column(String, nullable=False)
    email = Column(String, index=True)
    job_title = Column(String)
    linkedin = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="people")
