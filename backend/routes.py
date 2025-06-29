from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Certificate
from utils import overlay_text_on_image
from pydantic import BaseModel
from typing import List
from fastapi.responses import FileResponse
import os

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route: Verify a certificate
@router.get("/verify/{cert_number}")
def verify_certificate(cert_number: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.cert_number == cert_number).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    image_path = overlay_text_on_image(cert.cert_number, cert.name, cert.course, cert.start_date, cert.end_date)
    
    return {
        "name": cert.name,
        "course": cert.course,
        "start_date": cert.start_date.strftime("%Y-%m-%d"),
        "end_date": cert.end_date.strftime("%Y-%m-%d"),
        "generated_on": cert.generated_on.strftime("%Y-%m-%d"),
        "image_url": f"/{image_path}"
    }

# Response model for sidebar listing
class CertificateSummary(BaseModel):
    cert_number: str
    name: str

    class Config:
        orm_mode = True

# Route: Get minimal list of certificates
@router.get("/certificates", response_model=List[CertificateSummary])
def list_certificates(db: Session = Depends(get_db)):
    certs = db.query(Certificate).all()
    return certs

# Route: Force file download (not inline display)
@router.get("/download/{filename}")
def download_certificate(filename: str):
    file_path = os.path.join("modified_certs", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=filename
    )
