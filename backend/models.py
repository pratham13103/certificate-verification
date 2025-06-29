from database import Base
from sqlalchemy import Column, String, Date
from datetime import date

class Certificate(Base):
    __tablename__ = "certificates"

    cert_number = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    course = Column(String, nullable=False) 
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    generated_on = Column(Date, nullable=False, default=date.today)  
