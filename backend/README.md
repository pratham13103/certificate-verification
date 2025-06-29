cd backend
python -m venv venv
pip install -r requirements.txt
venv/Scripts/activate
uvicorn main:app --reload

add .env file in backend folder and add DATABASE_URL like this
DATABASE_URL=postgresql://postgres:<DBPassword>@localhost:5432/certificate_db
