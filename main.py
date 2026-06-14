from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import diem_thi, bang_lai, bhxh

app = FastAPI(title="TraCuuVN API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diem_thi.router, prefix="/api/diem-thi", tags=["Điểm Thi"])
app.include_router(bang_lai.router, prefix="/api/bang-lai", tags=["Bằng Lái"])
app.include_router(bhxh.router,     prefix="/api/bhxh",     tags=["BHXH"])

@app.get("/")
def root():
    return {"status": "ok", "message": "TraCuuVN API đang chạy"}

@app.get("/health")
def health():
    return {"status": "healthy"}
