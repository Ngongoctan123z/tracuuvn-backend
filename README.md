# TraCuuVN Backend

## Deploy lên Render.com (miễn phí)

1. Tạo tài khoản tại https://render.com
2. New → Web Service → Connect GitHub
3. Upload folder này lên GitHub trước
4. Render tự detect render.yaml và deploy

## API Endpoints

### Điểm thi THPT
POST /api/diem-thi/tra-cuu
Body: { "sbd": "12345678", "nam": "2024" }
Nam để trống = tự động thử 2024, 2023, 2022, 2021

### Bằng lái xe  
POST /api/bang-lai/tra-cuu
Body: { "so_gplx": "012345678" }

### BHXH / BHYT
POST /api/bhxh/tra-cuu
Body: { "ma_so": "0123456789" }

## Test local
pip install -r requirements.txt
uvicorn main:app --reload
Mở http://localhost:8000/docs
