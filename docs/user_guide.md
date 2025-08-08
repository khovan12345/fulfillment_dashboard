# 📖 Hướng Dẫn Người Dùng - Fulfillment Dashboard

## 🎯 Giới Thiệu

Fulfillment Dashboard là một ứng dụng web được xây dựng để theo dõi và quản lý tiến độ xác nhận đơn
hàng và bàn giao vận chuyển trong hệ thống ONE. Dashboard cung cấp giao diện trực quan với các biểu
đồ tương tác và báo cáo chi tiết.

## 🚀 Bắt Đầu Nhanh

### 1. Khởi Chạy Dashboard

```bash
# Cách khuyến nghị: script tự động
chmod +x run.sh
./run.sh

# (Tùy chọn) Command line manual
streamlit run app.py --server.port 8502
```

### 2. Truy Cập Web Interface

- Mở trình duyệt
- Truy cập: `http://localhost:8501`
- Dashboard sẽ tự động tải dữ liệu và hiển thị

## 📊 Giao Diện Chính

### Header

- **Tiêu đề**: Fulfillment Dashboard - Hệ thống ONE
- **Thời gian cập nhật**: Hiển thị lần cập nhật cuối cùng

### Sidebar (Thanh Bên)

- **Nút làm mới**: Cập nhật dữ liệu mới nhất
- **Menu điều hướng**: 4 trang chính
- **Thông tin thời gian**: Timestamp cập nhật

### Main Content (Nội Dung Chính)

Hiển thị theo trang được chọn trong menu

## 📋 Chi Tiết Các Trang

### 📊 Trang Tổng Quan

#### KPIs Chính (Hàng 1)

1. **📦 Tổng đơn hàng**
   - Hiển thị tổng số đơn hàng
   - Không có delta (thay đổi)

2. **✅ Tỷ lệ xác nhận đúng hạn**
   - Hiển thị phần trăm xác nhận đúng hạn
   - Delta so với mục tiêu 90%
   - Màu xanh nếu đạt mục tiêu

3. **🚚 Tỷ lệ giao hàng đúng hạn**
   - Hiển thị phần trăm giao hàng đúng hạn
   - Delta so với mục tiêu 85%
   - Màu xanh nếu đạt mục tiêu

4. **❌ Đơn hàng hủy**
   - Số lượng đơn hàng bị hủy
   - Delta hiển thị tỷ lệ hủy

#### Biểu Đồ Hiệu Suất (Hàng 2)

1. **Biểu đồ tròn - Phân bố trạng thái**
   - Các trạng thái: confirmed, delivered, cancelled, pending
   - Màu sắc phân biệt rõ ràng
   - Hover để xem chi tiết

2. **Biểu đồ cột - Đơn hàng theo vùng**
   - Các vùng: Hà Nội, TP.HCM, Đà Nẵng, etc.
   - Color scale theo số lượng
   - Click legend để ẩn/hiện

#### Timeline Đơn Hàng (Hàng 3)

1. **Biểu đồ trên**: Số lượng đơn hàng theo ngày
   - Line chart với markers
   - Xaxis: Ngày, Yaxis: Số đơn hàng

2. **Biểu đồ dưới**: Tỷ lệ đúng hạn theo ngày
   - 2 đường: Xác nhận và Giao hàng
   - Màu xanh và cam phân biệt

#### Thống Kê Nhanh (Hàng 4)

1. **Cột trái - Mục Tiêu KPI**
   - Bảng so sánh mục tiêu vs thực tế
   - Icon trạng thái (✅/❌)

2. **Cột phải - Thống Kê Giá Trị**
   - Tổng giá trị đơn hàng
   - Giá trị trung bình
   - Min/Max giá trị

### 📈 Trang Biểu Đồ Chi Tiết

#### Phân Tích Nâng Cao (Hàng 1)

1. **Đơn hàng theo giờ**
   - Bar chart 24 giờ
   - Xác định peak hours
   - Hover hiển thị số lượng chính xác

2. **Heatmap theo ngày & giờ**
   - Ma trận 7x24 (ngày x giờ)
   - Color intensity theo số lượng
   - Viridis color scale

#### Funnel Analysis (Hàng 2)

- **Phễu chuyển đổi**: Từ tạo đơn → hoàn thành
- Các stage: Tạo → Xác nhận → Giao hàng → Hoàn thành
- Tỷ lệ chuyển đổi giữa các bước

### 📋 Trang Dữ Liệu

#### Bộ Lọc (Hàng 1)

1. **Lọc trạng thái**
   - Dropdown: Tất cả + các trạng thái có sẵn
   - Real-time filtering

2. **Lọc vùng**
   - Dropdown: Tất cả + các vùng có sẵn
   - Combine với bộ lọc khác

3. **Lọc thời gian**
   - Date range picker
   - Default: Toàn bộ khoảng thời gian

#### Bảng Dữ Liệu (Hàng 2)

- **Các cột hiển thị**:
  - Order ID
  - Order Date (formatted)
  - Status
  - Region
  - Order Value (formatted VND)
  - Is Confirmed On-time
  - Is Delivered On-time

- **Tính năng**:
  - Sortable columns
  - Responsive design
  - Hide index
  - Full width

#### Thông Tin Bộ Lọc (Hàng 3)

- Hiển thị số lượng bản ghi sau lọc
- Tổng số bản ghi ban đầu

### ⚙️ Trang Cài Đặt

#### Ngưỡng KPI (Hàng 1)

1. **Cột trái**:
   - Slider: Ngưỡng xác nhận (80-100%)
   - Slider: Ngưỡng giao hàng (70-95%)

2. **Cột phải**:
   - Slider: Giới hạn tỷ lệ hủy (5-20%)
   - Slider: Giới hạn giờ chờ (6-24h)

#### Tự Động Làm Mới (Hàng 2)

- Checkbox: Bật/tắt auto refresh
- Dropdown: Khoảng thời gian (30s, 1m, 5m, 10m)

#### Xuất Dữ Liệu (Hàng 3)

- Button: Tải xuống CSV
- Future: Excel, PDF export

## 🎮 Tương Tác Với Dashboard

### Biểu Đồ Plotly

1. **Hover**: Di chuột để xem tooltip chi tiết
2. **Zoom**:
   - Scroll wheel để zoom in/out
   - Box select để zoom vùng
3. **Pan**: Kéo để di chuyển biểu đồ
4. **Legend**: Click để ẩn/hiện data series
5. **Toolbar**:
   - Download PNG
   - Pan/Zoom tools
   - Reset axes

### Streamlit Widgets

1. **Selectbox**: Click để mở dropdown
2. **Slider**: Kéo để thay đổi giá trị
3. **Date Input**: Click để mở calendar
4. **Button**: Click để thực hiện action
5. **Checkbox**: Click để toggle on/off

### Navigation

1. **Sidebar Menu**: Click để chuyển trang
2. **Refresh Button**: Reload toàn bộ dữ liệu
3. **Browser Back/Forward**: Không khuyến khích

## 💡 Mẹo Sử Dụng Hiệu Quả

### Monitoring Daily

1. **Bắt đầu ngày**: Kiểm tra trang Tổng quan
2. **Theo dõi KPIs**: Chú ý các metric có màu đỏ
3. **Xem xu hướng**: Timeline để phát hiện pattern

### Troubleshooting

1. **Identify Issues**: Dùng biểu đồ Funnel
2. **Deep Dive**: Chuyển sang trang Chi tiết
3. **Root Cause**: Sử dụng bộ lọc trong trang Dữ liệu

### Performance Optimization

1. **Peak Hours**: Xem biểu đồ theo giờ
2. **Regional Issues**: Phân tích theo vùng
3. **Trend Analysis**: Sử dụng timeline charts

## 🚨 Xử Lý Sự Cố Người Dùng

### Dashboard Không Tải

1. Kiểm tra URL: `http://localhost:8501`
2. Refresh browser (Ctrl+F5)
3. Kiểm tra terminal có lỗi không
4. Restart application

### Dữ Liệu Không Hiển Thị

1. Click nút "Làm mới dữ liệu"
2. Kiểm tra file data/orders_sample.csv
3. Xem terminal logs để debug

### Biểu Đồ Lỗi Hiển Thị

1. Hover vào biểu đồ để xem lỗi
2. Thử zoom reset (double-click)
3. Refresh trang nếu cần

### Performance Chậm

1. Giảm khoảng thời gian filter
2. Close các tab browser khác
3. Restart dashboard nếu cần

## 📱 Mobile Responsive

### Smartphone

- Sidebar collapse tự động
- Charts resize theo screen
- Touch-friendly controls

### Tablet

- Optimal viewing experience
- All features available
- Portrait/landscape support

## 🔄 Cập Nhật Dữ Liệu

### Automatic Refresh

- Bật trong trang Cài đặt
- Chọn interval phù hợp
- Dashboard tự reload

### Manual Refresh

- Click nút "Làm mới" trong sidebar
- Hoặc refresh browser page
- Dữ liệu được tải lại từ file

### Data File Update

- Thay thế file CSV trong thư mục data/
- Giữ nguyên format và column names
- Dashboard sẽ auto-detect changes

## 🔐 Bảo Mật & Quyền Truy Cập

### Local Deployment

- Dashboard chạy local, không có authentication
- Chỉ truy cập được từ localhost
- Dữ liệu được lưu local

### Production Deployment

- Cần setup authentication (OAuth, LDAP)
- HTTPS encryption
- Database security

## 📞 Hỗ Trợ Kỹ Thuật

### Self-Service

1. Đọc README.md
2. Kiểm tra terminal logs
3. Thử basic troubleshooting

### Contact Support

- **Email**: <support@company.com>
- **Slack**: #fulfillment-dashboard
- **Phone**: +84-xxx-xxx-xxx (business hours)

### Bug Report

- Screenshot lỗi
- Steps to reproduce
- Browser và OS info
- Terminal logs nếu có

---

_Hướng dẫn này được cập nhật thường xuyên. Vui lòng kiểm tra phiên bản mới nhất._
