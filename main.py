from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import re

app = FastAPI(title="TraCuuVN API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ────────────────────────────────────────────────────────────────────

class DiemThiRequest(BaseModel):
    sbd: str
    nam: str = ""

class BangLaiRequest(BaseModel):
    so_gplx: str

class BhxhRequest(BaseModel):
    ma_so: str

# ── Điểm thi ─────────────────────────────────────────────────────────────────

@app.post("/api/diem-thi/tra-cuu")
async def tra_cuu_diem_thi(req: DiemThiRequest):
    sbd = req.sbd.strip()
    if not sbd:
        raise HTTPException(status_code=400, detail="Vui lòng nhập số báo danh")

    # Thử nhiều năm nếu không truyền năm
    years = [req.nam] if req.nam else ["2024", "2023", "2022"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Referer": "https://diemthi.vnanet.vn/",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        for year in years:
            try:
                resp = await client.post(
                    "https://diemthi.vnanet.vn/index/ExamResultSearch",
                    json={"sobaodanh": sbd, "namthi": year},
                    headers=headers,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    # Nếu có dữ liệu trả về
                    if data and isinstance(data, list) and len(data) > 0:
                        item = data[0]
                        return {
                            "success": True,
                            "data": {
                                "ho_ten": item.get("HoTen", ""),
                                "sbd": item.get("SoBaoDanh", sbd),
                                "nam": year,
                                "ngu_van": str(item.get("NguVan", "--")),
                                "toan": str(item.get("Toan", "--")),
                                "ngoai_ngu": str(item.get("NgoaiNgu", "--")),
                                "vat_ly": str(item.get("VatLy", "--")),
                                "hoa_hoc": str(item.get("HoaHoc", "--")),
                                "sinh_hoc": str(item.get("SinhHoc", "--")),
                                "lich_su": str(item.get("LichSu", "--")),
                                "dia_ly": str(item.get("DiaLy", "--")),
                                "gdcd": str(item.get("GDCD", "--")),
                            }
                        }
                    elif data and isinstance(data, dict):
                        return {
                            "success": True,
                            "data": {
                                "ho_ten": data.get("HoTen", data.get("hoTen", "")),
                                "sbd": sbd,
                                "nam": year,
                                "ngu_van": str(data.get("NguVan", data.get("nguVan", "--"))),
                                "toan": str(data.get("Toan", data.get("toan", "--"))),
                                "ngoai_ngu": str(data.get("NgoaiNgu", data.get("ngoaiNgu", "--"))),
                                "vat_ly": str(data.get("VatLy", "--")),
                                "hoa_hoc": str(data.get("HoaHoc", "--")),
                                "sinh_hoc": str(data.get("SinhHoc", "--")),
                                "lich_su": str(data.get("LichSu", "--")),
                                "dia_ly": str(data.get("DiaLy", "--")),
                                "gdcd": str(data.get("GDCD", "--")),
                            }
                        }
            except Exception:
                continue

    raise HTTPException(status_code=404, detail="Không tìm thấy thông tin. Kiểm tra lại SBD.")

# ── Bằng lái ─────────────────────────────────────────────────────────────────

@app.post("/api/bang-lai/tra-cuu")
async def tra_cuu_bang_lai(req: BangLaiRequest):
    so = req.so_gplx.strip()
    if not so:
        raise HTTPException(status_code=400, detail="Vui lòng nhập số GPLX")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Referer": "https://gplx.gov.vn/",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.post(
                "https://gplx.gov.vn/api/tracuu/gplx",
                json={"sogplx": so},
                headers=headers,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    # Normalize các key có thể khác nhau
                    d = data if isinstance(data, dict) else (data[0] if isinstance(data, list) and data else {})
                    return {
                        "success": True,
                        "data": {
                            "ho_ten": d.get("hoTen", d.get("HoTen", d.get("ho_ten", ""))),
                            "so_gplx": d.get("soGPLX", d.get("SoGPLX", so)),
                            "hang": d.get("hang", d.get("Hang", d.get("hangGPLX", "--"))),
                            "ngay_cap": d.get("ngayCap", d.get("NgayCap", "--")),
                            "ngay_het_han": d.get("ngayHetHan", d.get("NgayHetHan", "--")),
                            "noi_cap": d.get("noiCap", d.get("NoiCap", "--")),
                            "trang_thai": d.get("trangThai", d.get("TrangThai", "Đang hoạt động")),
                        }
                    }
        except Exception as e:
            pass

    raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bằng lái. Kiểm tra lại số GPLX.")

# ── BHXH ─────────────────────────────────────────────────────────────────────

@app.post("/api/bhxh/tra-cuu")
async def tra_cuu_bhxh(req: BhxhRequest):
    ma = req.ma_so.strip()
    if not ma:
        raise HTTPException(status_code=400, detail="Vui lòng nhập mã số BHXH/CCCD")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Referer": "https://baohiemxahoi.gov.vn/",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.post(
                "https://baohiemxahoi.gov.vn/tracuu/api/tracuubhyt",
                json={"maSoBHXH": ma, "maKiemTra": ""},
                headers=headers,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    d = data if isinstance(data, dict) else (data[0] if isinstance(data, list) and data else {})
                    return {
                        "success": True,
                        "data": {
                            "ho_ten": d.get("hoTen", d.get("HoTen", "")),
                            "ma_so_bhxh": d.get("maSoBHXH", d.get("maSo", ma)),
                            "noi_kcb": d.get("noiKCB", d.get("noiDangKyKCB", "--")),
                            "han_the": d.get("denNgay", d.get("hanThe", "--")),
                            "trang_thai": d.get("trangThai", "Đang hoạt động"),
                        }
                    }
        except Exception:
            pass

    raise HTTPException(status_code=404, detail="Không tìm thấy thông tin BHXH. Kiểm tra lại mã số.")

# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"status": "ok", "message": "TraCuuVN API đang chạy"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
