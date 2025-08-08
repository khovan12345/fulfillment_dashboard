# 📊 Hướng Dẫn Thiết Lập Google Sheets

## 🎯 Mục đích
Script này sẽ tạo một Google Sheets để quản lý cấu hình hệ thống Fulfillment Dashboard với giao diện tiếng Việt, giúp nhân viên dễ dàng theo dõi và cập nhật.

## 🔧 Chuẩn bị

### 1. Tạo Service Account (Tài khoản dịch vụ)

1. **Truy cập Google Cloud Console:**
   - Vào: https://console.cloud.google.com/
   - Đăng nhập bằng tài khoản Google

2. **Tạo hoặc chọn Project:**
   - Tạo project mới hoặc chọn project có sẵn
   - Tên gợi ý: "Fulfillment Dashboard"

3. **Bật APIs cần thiết:**
   - Vào "APIs & Services" > "Library"
   - Tìm và bật: "Google Sheets API"
   - Tìm và bật: "Google Drive API"

4. **Tạo Service Account:**
   - Vào "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Tên: "fulfillment-dashboard-service"
   - Mô tả: "Service account cho Fulfillment Dashboard"

5. **Tạo JSON Key:**
   - Click vào service account vừa tạo
   - Vào tab "Keys"
   - Click "Add Key" > "Create new key" > "JSON"
   - Tải file JSON về và đặt tên: `service_account.json`
   - Copy file này vào thư mục: `config/service_account.json`

### 2. Cài đặt thư viện

```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt thư viện Google Sheets
pip install gspread google-auth google-auth-oauthlib google-auth-httplib2
```

## 🚀 Chạy Script

```bash
# Chạy script thiết lập
python scripts/setup_google_sheets.py
```

## 📋 Kết quả mong đợi

Script sẽ tạo ra 3 worksheets:

### 1. 🏗️ Cấu hình hệ thống
- Hiển thị tất cả cài đặt hiện tại
- URL hệ thống, thời gian chờ, cấu hình email...
- Dễ dàng theo dõi và kiểm tra

### 2. 📋 Quy tắc SLA
- Định nghĩa thời gian xử lý cho từng loại đơn hàng
- Ngưỡng KPI cần đạt
- Phân công trách nhiệm

### 3. 📝 Nhật ký tự động
- Ghi lại tất cả hoạt động của hệ thống
- Theo dõi lỗi và thành công
- Phân tích hiệu suất

## 👥 Chia sẻ cho nhân viên

1. **Sau khi script chạy xong:**
   - Mở URL Google Sheets được hiển thị
   - Click "Share" ở góc phải trên

2. **Thêm nhân viên:**
   - Nhập email của nhân viên
   - Chọn quyền: "Editor" (để sửa) hoặc "Viewer" (chỉ xem)
   - Click "Send"

3. **Quyền đề xuất:**
   - **Manager/Supervisor:** Editor (có thể sửa)
   - **Nhân viên CS:** Viewer (chỉ xem)
   - **IT Support:** Editor (có thể sửa)

## 🔄 Sử dụng hàng ngày

### Cho Manager:
- Kiểm tra cấu hình hệ thống
- Cập nhật quy tắc SLA khi cần
- Theo dõi nhật ký lỗi

### Cho nhân viên CS:
- Xem quy tắc SLA để biết thời gian xử lý
- Kiểm tra trạng thái hệ thống
- Báo cáo lỗi qua nhật ký

### Cho IT:
- Cập nhật cấu hình khi thay đổi
- Theo dõi log hệ thống
- Khắc phục sự cố

## 🛠️ Khắc phục sự cố

### Lỗi "Credentials not found":
```bash
# Kiểm tra file credentials
ls -la config/service_account.json
```

### Lỗi "Permission denied":
- Kiểm tra service account đã được tạo đúng
- Đảm bảo APIs đã được bật

### Lỗi "Spreadsheet not found":
- Kiểm tra ID trong config/system_config.json
- Đảm bảo service account có quyền truy cập

## 📞 Hỗ trợ

Nếu gặp vấn đề, liên hệ:
- **IT Support:** it@company.com
- **Manager:** manager@company.com

---

📝 **Lưu ý:** Google Sheets này sẽ được đồng bộ tự động với hệ thống. Mọi thay đổi sẽ ảnh hưởng đến hoạt động của dashboard.
