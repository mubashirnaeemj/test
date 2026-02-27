#################1111111111111111111111##################
1111111111111111111111111111111111111
2222222222222222222222222222222
333333333333333333333333
this is the new code 
and also this one[
    asdadfaafaf
    af
    23242
    saf
]
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from routers.auth_router import auth_router
from routers.reports_router import reports_router

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Code Audit")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test routes for DB
@app.post("/users/")
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/repos/")
def add_repo(repo: schemas.RepositoryCreate, db: Session = Depends(get_db)):
    return crud.create_repository(db, repo)

@app.post("/commits/")
def add_commit(commit: schemas.CommitCreate, db: Session = Depends(get_db)):
    return crud.create_commit(db, commit)

@app.post("/reports/")
def add_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db, report)

@app.get("/")
def root():
    return {"message": "AI Code Audit Backend is running!"}
