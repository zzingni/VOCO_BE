import pandas as pd
from sqlalchemy.orm import Session

from app.models.company import Company
from app.db.database import SessionLocal
import app.models

db: Session = SessionLocal()

df = pd.read_excel("colist.xlsx")
df = df.fillna("")

companies = []

for _, row in df.iterrows():
    companies.append({
        "company_name": row["사업장명"],
        "industry_name": row["사업장업종코드명"],
        "status": "ACTIVE"
    })

db.bulk_insert_mappings(Company, companies)

db.commit()
db.close()

print("기업 데이터 삽입 완료")