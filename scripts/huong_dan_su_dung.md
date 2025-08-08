# 📋 HƯỚNG DẪN SỬ DỤNG GOOGLE SHEETS

## 🚀 Cài đặt ban đầu

### Bước 1: Chuẩn bị
```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Kiểm tra cơ bản
python scripts/test_basic.py
```

### Bước 2: Thiết lập Google Sheets
```bash
# Chạy script thiết lập (giao diện Tiếng Việt)
python scripts/setup_google_sheets.py
```

Script sẽ:
- ✅ Tạo Google Sheets mới
- ✅ Thiết lập các worksheet cần thiết
- ✅ Cấu hình quyền truy cập
- ✅ Lưu cấu hình vào system_config.json

### Bước 3: Kiểm tra kết nối
```bash
# Test kết nối đầy đủ
python scripts/test_google_connection.py
```

## 🛠️ Công cụ sử dụng hàng ngày

### 1. Google Sheets Manager
```bash
python scripts/gs_manager.py
```

**Chức năng:**
- �� Xem quy tắc SLA
- 📝 Xem log gần đây
- ✏️ Ghi log mới
- 💾 Backup sheets
- 🔗 Mở Google Sheets

### 2. Dashboard chính
```bash
# Chạy dashboard
./run.sh
# Hoặc
python -m streamlit run app.py --server.port 8502
```

## 📊 Cấu trúc Google Sheets

### 1. **Cấu hình hệ thống**
- Lưu trữ các thiết lập hệ thống
- Timeout, URLs, notifications
- Có thể chỉnh sửa trực tiếp

### 2. **Quy tắc SLA**
- Định nghĩa thời gian xử lý cho từng loại đơn
- Mức độ ưu tiên
- Người phụ trách

### 3. **Nhật ký tự động**
- Ghi lại tất cả hoạt động của hệ thống
- Tự động cập nhật khi có hoạt động
- Có thể lọc theo thời gian

### 4. **Thống kê tổng quan**
- Báo cáo hiệu suất hàng ngày
- Biểu đồ phân tích
- Tỷ lệ thành công/lỗi

## 🔧 Xử lý sự cố

### Lỗi thường gặp:

#### 1. "Không kết nối được Google Sheets"
```bash
# Kiểm tra credentials
ls -la config/service_account.json

# Kiểm tra config
python scripts/test_basic.py
```

#### 2. "Thiếu thư viện"
```bash
# Cài đặt lại
pip install gspread google-auth google-auth-oauthlib
```

#### 3. "Lỗi quyền truy cập"
- Kiểm tra service account có quyền chỉnh sửa sheet
- Đảm bảo sheet được share với email service account

### Khôi phục dữ liệu:
```bash
# Tạo backup thủ công
python scripts/gs_manager.py
# Chọn option 4: Backup sheets
```

## 👥 Sử dụng cho nhân viên

### Quyền truy cập:
- **Chỉ xem**: Nhân viên thường
- **Chỉnh sửa**: Quản lý, Admin
- **Toàn quyền**: IT, System Admin

### Giao diện thân thiện:
- Tất cả menu và thông báo bằng Tiếng Việt
- Hướng dẫn chi tiết từng bước
- Màu sắc trực quan (✅ ❌ 📊 ��)

### Workflow thường ngày:
1. Mở dashboard: `./run.sh`
2. Xem báo cáo trên Google Sheets
3. Cập nhật SLA nếu cần
4. Kiểm tra log hoạt động

## 📞 Hỗ trợ

### File log:
- Dashboard: Kiểm tra terminal chạy `./run.sh`
- Google Sheets: Xem trong worksheet "Nhật ký tự động"

### Liên hệ IT:
- Lỗi kết nối: Kiểm tra service_account.json
- Lỗi hiệu suất: Xem dashboard logs
- Cần thêm chức năng: Tạo issue

---

🎯 **Mục tiêu**: Tạo môi trường làm việc hiệu quả, dễ sử dụng cho tất cả nhân viên
