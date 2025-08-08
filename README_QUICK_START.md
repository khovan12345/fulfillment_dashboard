# 🚀 QUICK START - FULFILLMENT DASHBOARD

## Khởi chạy nhanh (5 phút)

### 1. Cài đặt và chạy
```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Khởi chạy dashboard
./start_all.sh
```

### 2. Truy cập dashboard
- **URL**: http://localhost:8502
- **Tài khoản**: Không cần đăng nhập
- **Tính năng**: Xem báo cáo, thống kê, quản lý đơn hàng

### 3. Thiết lập Google Sheets (tùy chọn)
```bash
# Thiết lập Google Sheets với giao diện Tiếng Việt
python scripts/setup_google_sheets.py

# Quản lý Google Sheets
python scripts/gs_manager.py
```

## 📁 Cấu trúc dự án

```
fulfillment_dashboard/
├── app.py              # Dashboard chính
├── start_all.sh        # Khởi chạy nhanh
├── requirements.txt    # Thư viện Python
├── config/
│   ├── config.py       # Cấu hình hệ thống
│   └── system_config.json
├── scripts/
│   ├── gs_manager.py   # Quản lý Google Sheets
│   ├── setup_google_sheets.py
│   └── test_basic.py   # Kiểm tra cơ bản
└── docs/
    └── huong_dan_su_dung.md
```

## 🛠️ Công cụ hữu ích

| Script | Mục đích | Cách chạy |
|--------|----------|-----------|
| `start_all.sh` | Khởi chạy dashboard | `./start_all.sh` |
| `gs_manager.py` | Quản lý Google Sheets | `python scripts/gs_manager.py` |
| `test_basic.py` | Kiểm tra hệ thống | `python scripts/test_basic.py` |

## 🔧 Xử lý sự cố nhanh

### Lỗi port đã sử dụng:
```bash
# Tìm và dừng process
lsof -ti:8502 | xargs kill -9
./start_all.sh
```

### Thiếu thư viện:
```bash
pip install -r requirements.txt
```

### Lỗi Google Sheets:
```bash
python scripts/test_basic.py
# Làm theo hướng dẫn hiển thị
```

## 🎯 Tính năng chính

✅ **Dashboard Streamlit** - Giao diện web hiện đại  
✅ **Google Sheets** - Lưu trữ cấu hình và log  
✅ **Quản lý SLA** - Thiết lập thời gian xử lý  
✅ **Nhật ký tự động** - Theo dõi hoạt động  
✅ **Giao diện Tiếng Việt** - Thân thiện với nhân viên  
✅ **Backup tự động** - Bảo vệ dữ liệu  

## 📞 Hỗ trợ

- **Hướng dẫn chi tiết**: `docs/huong_dan_su_dung.md`
- **Logs hệ thống**: Xem trong terminal dashboard
- **Google Sheets logs**: Worksheet "Nhật ký tự động"

---
💡 **Tip**: Chạy `./start_all.sh` để khởi động nhanh tất cả mọi thứ!
