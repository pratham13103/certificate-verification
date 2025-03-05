from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Certificate
from utils import overlay_text_on_image

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/verify/{cert_number}")
def verify_certificate(cert_number: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.cert_number == cert_number).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    image_path = overlay_text_on_image(cert.name, cert.course, cert.start_date, cert.end_date)
    
    return {
        "name": cert.name,
        "course": cert.course,
        "start_date": cert.start_date.strftime("%Y-%m-%d"),
        "end_date": cert.end_date.strftime("%Y-%m-%d"),
        "image_url": f"/{image_path}"
    }
