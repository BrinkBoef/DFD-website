import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

def clean_value(value):
    """Clean NaN and None values"""
    if pd.isna(value):
        return None
    return value

def import_gp_data(file_path: str):
    """Import data from GP.xlsx into the database"""

    print(f"Reading Excel file: {file_path}")
    df = pd.read_excel(file_path)

    print(f"Total rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # Create tables
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Get unique companies (General Partners)
        unique_companies = df['General Partner'].unique()
        print(f"\nFound {len(unique_companies)} unique companies")

        # Create company mapping
        company_map = {}

        print("\nCreating companies...")
        for idx, company_name in enumerate(unique_companies, 1):
            if pd.notna(company_name):
                # Check if company already exists
                existing = db.query(models.Company).filter(
                    models.Company.name == company_name
                ).first()

                if not existing:
                    company = models.Company(name=company_name)
                    db.add(company)
                    db.flush()
                    company_map[company_name] = company.id
                else:
                    company_map[company_name] = existing.id

                if idx % 100 == 0:
                    print(f"  Processed {idx}/{len(unique_companies)} companies...")
                    db.commit()

        db.commit()
        print(f"Created {len(company_map)} companies")

        # Import funds
        print("\nImporting funds...")
        for idx, row in df.iterrows():
            company_name = row['General Partner']

            if pd.isna(company_name) or company_name not in company_map:
                continue

            company_id = company_map[company_name]

            fund = models.Fund(
                company_id=company_id,
                fund_name=clean_value(row['Fund']),
                vintage=clean_value(row['Vintage']),
                size=clean_value(row['Size (USD)']),
                status=clean_value(row['Status']),
                fund_inception_date=clean_value(row['Fund Inception Date']),
                strategy=clean_value(row['Strategy']),
                sub_strategy=clean_value(row['Sub-strategy']),
                sector=clean_value(row['Sector']),
                industry=clean_value(row['Industry']),
                region=clean_value(row['Region']),
                country_region=clean_value(row['Country/Region']),
                net_irr=clean_value(row['Net IRR (%)']),
                qtl=clean_value(row['Qtl']),
                invested=clean_value(row['Invested']),
                pct_of_tgt=clean_value(row['% of Tgt']),
                raised=clean_value(row['Raised']),
                curr_inv=clean_value(row['Curr Inv']),
                dpi=clean_value(row['DPI']),
                amt=clean_value(row['Amt']),
                pct=clean_value(row['Pct']),
                dry_powder=clean_value(row['Dry Powder']),
                hist_inv=clean_value(row['Hist Inv']),
                moic=clean_value(row['MOIC']),
                management_fee=clean_value(row['Mangement Fee (%)']),
                pic=clean_value(row['PIC (%)']),
                first_qtl=clean_value(row['1st']),
                second_qtl=clean_value(row['2nd']),
                third_qtl=clean_value(row['3rd']),
                fourth_qtl=clean_value(row['4th']),
                na_qtl=clean_value(row['N.A.']),
                total_qtl=clean_value(row['Total']),
                rvpi=clean_value(row['RVPI']),
                target=clean_value(row['Target']),
                time_in_mkt=clean_value(row['Time in Mkt']),
                tot_inv=clean_value(row['Tot Inv']),
                unrealized=clean_value(row['Unrealized'])
            )

            db.add(fund)

            if (idx + 1) % 500 == 0:
                print(f"  Imported {idx + 1}/{len(df)} funds...")
                db.commit()

        db.commit()
        print(f"\nSuccessfully imported {len(df)} funds")

        # Update company fund counts
        print("\nUpdating company fund counts...")
        for company_name, company_id in company_map.items():
            fund_count = db.query(models.Fund).filter(
                models.Fund.company_id == company_id
            ).count()

            company = db.query(models.Company).filter(
                models.Company.id == company_id
            ).first()

            if company:
                company.total_funds = fund_count

        db.commit()
        print("Done!")

        # Print summary
        total_companies = db.query(models.Company).count()
        total_funds = db.query(models.Fund).count()

        print("\n" + "="*50)
        print("IMPORT SUMMARY")
        print("="*50)
        print(f"Total Companies: {total_companies}")
        print(f"Total Funds: {total_funds}")
        print(f"Average funds per company: {total_funds/total_companies:.2f}")

        # Show top companies
        print("\nTop 10 companies by number of funds:")
        top_companies = db.query(models.Company).order_by(
            models.Company.total_funds.desc()
        ).limit(10).all()

        for i, company in enumerate(top_companies, 1):
            print(f"  {i}. {company.name}: {company.total_funds} funds")

    except Exception as e:
        print(f"Error during import: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Path to GP.xlsx
    file_path = "GP.xlsx"

    if not os.path.exists(file_path):
        file_path = "../GP.xlsx"

    if not os.path.exists(file_path):
        print("Error: GP.xlsx not found!")
        sys.exit(1)

    import_gp_data(file_path)
