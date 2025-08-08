# 🚀 Fulfillment Dashboard - Hệ thống ONE

> Cổng mặc định: 8502 • Lệnh chạy duy nhất (khuyến nghị): `./run.sh`

Dashboard theo dõi tiến độ xác nhận đơn hàng và bàn giao vận chuyển cho hệ thống ONE.

## 📊 Tính Năng Chính

### 🎯 KPIs Theo Dõi

- **Tổng đơn hàng**: Số lượng đơn hàng tổng cộng
- **Tỷ lệ xác nhận đúng hạn**: Mục tiêu ≥90%
- **Tỷ lệ bàn giao đúng hạn**: Mục tiêu ≥85%
- **Đơn hàng bị hủy**: Theo dõi số lượng và tỷ lệ
- **Đơn tồn đọng**: Đơn hàng chưa xác nhận quá 12 giờ

### 📈 Biểu Đồ Tương Tác

- **Biểu đồ tròn**: Phân bố trạng thái đơn hàng
- **Biểu đồ cột**: Đơn hàng theo vùng địa lý
- **Timeline**: Xu hướng đơn hàng theo thời gian
- **Heatmap**: Phân bố đơn hàng theo ngày/giờ
- **Funnel**: Phân tích chuyển đổi đơn hàng

### 🔧 Tính Năng Khác

- **Bộ lọc động**: Lọc theo trạng thái, vùng, thời gian
- **Tự động làm mới**: Cập nhật dữ liệu theo chu kỳ
- **Responsive**: Tương thích với PC và mobile
- **Xuất dữ liệu**: Export CSV/Excel

## 🛠️ Yêu Cầu Hệ Thống

### Phần Mềm Cần Thiết

- **Python**: 3.8 trở lên
- **pip**: Package manager của Python
- **VS Code**: (khuyến nghị) với Python extension

### Thư Viện Python

```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.1.0
numpy>=1.24.3
matplotlib>=3.7.2
seaborn>=0.12.2
openpyxl>=3.1.2
python-dateutil>=2.8.2
pytz>=2023.3
```

## 🚀 Hướng Dẫn Cài Đặt

### Thiết lập biến môi trường

```bash
cp .env.example .env
# Mở file .env và điền các biến:
# - ONE_USERNAME, ONE_PASSWORD
# - EMAIL_ADDRESS, EMAIL_PASSWORD, SLACK_WEBHOOK_URL (nếu dùng thông báo)
# - GOOGLE_CREDENTIALS_FILE: đường dẫn tuyệt đối tới JSON service account (không nằm trong repo)
```

### Phương Pháp khuyến nghị: Script tự động (một lệnh duy nhất)

#### Windows

```batch
# Chạy file run.bat
double-click run.bat
```

#### Linux/macOS

```bash
chmod +x run.sh
./run.sh
```

### Phương Pháp 2: Cài Đặt Thủ Công (tùy chọn)

#### Bước 1: Tạo Virtual Environment (khuyến nghị)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

#### Bước 2: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

#### Bước 3: Khởi Chạy Dashboard

Khuyến nghị dùng `./run.sh`. Nếu muốn chạy trực tiếp:

```bash
streamlit run app.py --server.port 8502
```

#### Bước 4: Truy Cập Dashboard

Mở trình duyệt và truy cập (mặc định): `http://localhost:8502`

## 📁 Cấu Trúc Project

```
fulfillment_dashboard/
├── app.py                    # File chính của dashboard
├── requirements.txt          # Danh sách thư viện cần thiết
├── setup.py                 # Script cài đặt package
├── run.bat                  # Script khởi chạy Windows
├── run.sh                   # Script khởi chạy Linux/macOS
├── README.md                # Hướng dẫn sử dụng
│
├── data/                    # Thư mục dữ liệu
│   └── orders_sample.csv    # Dữ liệu mẫu
│
├── config/                  # Thư mục cấu hình
│   └── config.py           # File cấu hình chính
│
├── utils/                   # Thư mục utilities
│   └── helpers.py          # Các hàm tiện ích
│
├── components/              # Thư mục components
│   └── dashboard_components.py  # Các thành phần UI
│
├── .vscode/                # Cấu hình VS Code
│   ├── settings.json       # Cài đặt workspace
│   └── launch.json         # Cấu hình debug
│
└── docs/                   # Thư mục tài liệu
    └── user_guide.md       # Hướng dẫn người dùng
```

## 🎮 Hướng Dẫn Sử Dụng

### 1. Khởi Chạy Dashboard

- Chạy script `run.bat` (Windows) hoặc `run.sh` (Linux/macOS)
- Hoặc chạy lệnh: `streamlit run app.py --server.port 8502`
- Truy cập `http://localhost:8502` trên trình duyệt

### 2. Điều Hướng Dashboard

#### 📊 Trang Tổng Quan

- Hiển thị KPIs chính
- Biểu đồ hiệu suất tổng quan
- Timeline xu hướng đơn hàng
- Bảng thống kê nhanh

#### 📈 Trang Biểu Đồ Chi Tiết

- Phân tích đơn hàng theo giờ
- Heatmap phân bố theo ngày/giờ
- Funnel analysis chuyển đổi

#### 📋 Trang Dữ Liệu

- Bảng chi tiết đơn hàng
- Bộ lọc theo trạng thái, vùng, thời gian
- Tìm kiếm và sắp xếp

#### ⚙️ Trang Cài Đặt

- Điều chỉnh ngưỡng KPI
- Cấu hình tự động làm mới
- Xuất dữ liệu

### 3. Tương Tác Với Biểu Đồ

- **Hover**: Xem chi tiết khi di chuột
- **Zoom**: Phóng to/thu nhỏ biểu đồ
- **Pan**: Kéo để di chuyển
- **Legend**: Click để ẩn/hiện series
- **Download**: Tải xuống biểu đồ dạng PNG

## 🔧 Tùy Chỉnh Dashboard

### Thay Đổi Dữ Liệu

1. Chuẩn bị file CSV với cấu trúc tương tự `data/orders_sample.csv`
2. Cập nhật đường dẫn trong `config/config.py`:

   ```python
   DATA_PATH = "data/your_data.csv"
   ```

### Điều Chỉnh KPI Thresholds

Sửa file `config/config.py`:

```python
KPI_THRESHOLDS = {
    'confirmation_target': 0.95,  # 95% thay vì 90%
    'delivery_target': 0.90,      # 90% thay vì 85%
    'cancellation_limit': 0.05,   # 5% thay vì 10%
    'pending_hours_limit': 8      # 8 giờ thay vì 12 giờ
}
```

### Thay Đổi Màu Sắc

Cập nhật `COLORS` trong `config/config.py`:

```python
COLORS = {
    'primary': '#your_color',
    'success': '#your_color',
    # ...
}
```

## 🐛 Xử Lý Sự Cố

### Lỗi Thường Gặp

#### 1. "ModuleNotFoundError"

```bash
# Cài đặt lại dependencies
pip install -r requirements.txt
```

#### 2. "FileNotFoundError: data/orders_sample.csv"

```bash
# Đảm bảo file dữ liệu tồn tại
ls data/orders_sample.csv
```

#### 3. "Port 8502 is already in use"

```bash
# Sử dụng port khác (ví dụ 8503)
streamlit run app.py --server.port 8503
```

#### 4. Dashboard không hiển thị dữ liệu

- Kiểm tra định dạng file CSV
- Đảm bảo có cột bắt buộc: `order_id`, `order_date`, `status`
- Kiểm tra encoding file (nên dùng UTF-8)

### Logs và Debug

- Kiểm tra terminal/command prompt để xem lỗi chi tiết
- Sử dụng VS Code với Python extension để debug
- Bật chế độ debug của Streamlit: `streamlit run app.py --server.port 8502 --logger.level debug`

## 🔄 Cập Nhật và Bảo Trì

### Cập Nhật Dữ Liệu

- Thay thế file trong thư mục `data/`
- Dashboard sẽ tự động tải lại khi refresh

### Backup

- Sao lưu thư mục `data/` định kỳ
- Export cấu hình từ `config/`

### Monitoring

- Theo dõi hiệu suất qua Streamlit admin
- Kiểm tra logs để phát hiện lỗi sớm

## 📞 Hỗ Trợ

### Liên Hệ

- **Email**: <support@company.com>
- **Phone**: +84-xxx-xxx-xxx

### Tài Liệu Bổ Sung

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 📄 License

Bản quyền thuộc về công ty. Vui lòng liên hệ để biết thêm chi tiết về giấy phép sử dụng.

---

**Phiên bản**: 1.0.0 **Ngày cập nhật**: 2024 **Tác giả**: AI Assistant

_Dashboard được thiết kế để tối ưu hóa việc theo dõi và quản lý tiến độ đơn hàng trong hệ thống
ONE._
