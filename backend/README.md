Steps to install certificate verification backend of FastAPI and PostgreSQL 

cd backend
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload

add .env file in backend folder and add DATABASE_URL like this
DATABASE_URL=postgresql://postgres:<DBPassword>@localhost:5432/certificate_db

create a postgresql database certificate_db and create table named certificates

SQL Alchemy is not used so you need to manually insert this data into the table 

INSERT INTO certificates (cert_number, name, course, start_date, end_date)
VALUES ('CERT126', 'John Doe', 'Research Intern', '2024-01-01', '2024-12-31');

SELECT * FROM certificates;

//Additional PSQL Commands
also you can alter the table using the command
ALTER TABLE certificates