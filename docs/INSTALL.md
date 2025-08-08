# 🛠️ Hướng Dẫn Cài Đặt Chi Tiết - Fulfillment Dashboard

## 📋 Mục Lục

1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Cài Đặt Python](#cài-đặt-python)
3. [Cài Đặt Dashboard](#cài-đặt-dashboard)
4. [Cấu Hình VS Code](#cấu-hình-vs-code)
5. [Khởi Chạy](#khởi-chạy)
6. [Xử Lý Sự Cố](#xử-lý-sự-cố)

## 🖥️ Yêu Cầu Hệ Thống

### Minimum Requirements

- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **RAM**: 4GB (khuyến nghị 8GB)
- **Disk**: 500MB free space
- **Network**: Internet connection (for installation)

### Recommended Requirements

- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **RAM**: 8GB+
- **Disk**: 2GB free space
- **CPU**: Multi-core processor
- **Monitor**: 1920x1080+ resolution

## 🐍 Cài Đặt Python

### Windows

#### Phương Pháp 1: Microsoft Store (Khuyến Nghị)

1. Mở Microsoft Store
2. Tìm kiếm "Python 3.11"
3. Click "Install"
4. Chờ quá trình cài đặt hoàn tất

#### Phương Pháp 2: Python.org

1. Truy cập: <https://www.python.org/downloads/>
2. Download Python 3.11+ for Windows
3. Chạy installer với quyền Administrator
4. ✅ **Quan trọng**: Check "Add Python to PATH"
5. Click "Install Now"

#### Xác Minh Cài Đặt

```cmd
# Mở Command Prompt
python --version
pip --version
```

### macOS

#### Phương Pháp 1: Homebrew (Khuyến Nghị)

```bash
# Cài Homebrew nếu chưa có
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài Python
brew install python@3.11
```

#### Phương Pháp 2: Python.org

1. Truy cập: <https://www.python.org/downloads/>
2. Download Python 3.11+ for macOS
3. Chạy installer package
4. Follow installation wizard

#### Xác Minh Cài Đặt

```bash
python3 --version
pip3 --version
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Cài Python và pip
sudo apt install python3.11 python3.11-pip python3.11-venv

# Tạo symlink (optional)
sudo ln -sf /usr/bin/python3.11 /usr/bin/python
sudo ln -sf /usr/bin/pip3 /usr/bin/pip
```

#### Xác Minh Cài Đặt

```bash
python --version
pip --version
```

## 📦 Cài Đặt Dashboard

### Bước 1: Tải Project

```bash
# Nếu có Git
git clone <repository-url>
cd fulfillment_dashboard

# Hoặc extract từ file ZIP
unzip fulfillment_dashboard.zip
cd fulfillment_dashboard
```

### Bước 2: Tạo Virtual Environment (Khuyến Nghị)

#### Windows

```cmd
# Tạo virtual environment
python -m venv venv

# Kích hoạt
venv\Scripts\activate

# Xác minh
where python
```

#### macOS/Linux

```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt
source venv/bin/activate

# Xác minh
which python
```

### Bước 3: Cài Đặt Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Cài dependencies
pip install -r requirements.txt

# Xác minh cài đặt
pip list
```

### Bước 4: Kiểm Tra Cài Đặt

```bash
# Test import các thư viện chính
python -c "import streamlit, plotly, pandas; print('✅ All packages installed successfully')"
```

## 🔧 Cấu Hình VS Code

### Cài Đặt VS Code

1. Truy cập: <https://code.visualstudio.com/>
2. Download cho OS tương ứng
3. Cài đặt với default settings

### Cài Đặt Extensions

1. Mở VS Code
2. Vào Extensions (Ctrl+Shift+X)
3. Cài các extension sau:
   - **Python** (Microsoft)
   - **Pylance** (Microsoft)
   - **Python Docstring Generator**
   - **autoDocstring**
   - **GitLens** (optional)

### Mở Project

1. File → Open Folder
2. Chọn thư mục `fulfillment_dashboard`
3. VS Code sẽ tự động detect Python project

### Cấu Hình Python Interpreter

1. Ctrl+Shift+P → "Python: Select Interpreter"
2. Chọn interpreter trong `venv` folder
3. Path sẽ giống: `./venv/bin/python` hoặc `.\venv\Scripts\python.exe`

### Kiểm Tra Cấu Hình

- File `.vscode/settings.json` đã được tạo sẵn
- File `.vscode/launch.json` đã có config để debug
- Status bar dưới cùng hiển thị Python version

## 🚀 Khởi Chạy

### Cách khuyến nghị: Script tự động (một lệnh duy nhất)

```bash
chmod +x run.sh
./run.sh
```

### Phương Pháp 2: Command Line Manual

```bash
# Kích hoạt virtual environment (nếu chưa)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Chạy dashboard
streamlit run app.py
```

### Phương Pháp 3: VS Code Debug

1. Mở `app.py` trong VS Code
2. F5 hoặc Run → Start Debugging
3. Chọn "Python: Streamlit" configuration

### Phương Pháp 4: VS Code Terminal

1. Ctrl+` để mở terminal trong VS Code
2. Terminal tự động activate virtual environment
3. Chạy: `streamlit run app.py`

## 🌐 Truy Cập Dashboard

### Local Development

- **URL**: <http://localhost:8501>
- **Alternative**: <http://127.0.0.1:8501>

### Network Access (Optional)

```bash
# Cho phép truy cập từ mạng LAN (ví dụ 8502)
streamlit run app.py --server.address 0.0.0.0 --server.port 8502
```

### Custom Port

```bash
# Nếu port 8501 bị chiếm
streamlit run app.py --server.port 8502
```

## 🔧 Xử Lý Sự Cố

### Lỗi Python Không Tìm Thấy

#### Windows

```cmd
# Kiểm tra PATH
echo %PATH%

# Thêm Python vào PATH manually
setx PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311"
```

#### macOS/Linux

```bash
# Kiểm tra PATH
echo $PATH

# Thêm vào ~/.bashrc hoặc ~/.zshrc
export PATH="/usr/local/bin/python3:$PATH"
```

### Lỗi Permission Denied

#### Windows

- Chạy Command Prompt as Administrator
- Hoặc thay đổi execution policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS/Linux

```bash
# Cấp quyền cho script
chmod +x run.sh

# Hoặc chạy với sudo nếu cần
sudo ./run.sh
```

### Lỗi Package Installation

```bash
# Clear pip cache
pip cache purge

# Reinstall với --no-cache-dir
pip install --no-cache-dir -r requirements.txt

# Upgrade pip và setuptools
pip install --upgrade pip setuptools wheel
```

### Lỗi Port Already in Use

```bash
# Kiểm tra process sử dụng port
# Windows
netstat -ano | findstr :8501

# macOS/Linux
lsof -i :8501

# Kill process nếu cần
# Windows
taskkill /PID <process_id> /F

# macOS/Linux
kill -9 <process_id>
```

### Lỗi Virtual Environment

```bash
# Xóa và tạo lại venv
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Tạo lại
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Reinstall packages
pip install -r requirements.txt
```

### Lỗi Data File

```bash
# Kiểm tra file tồn tại
ls data/orders_sample.csv

# Kiểm tra permissions
# Linux/macOS
ls -la data/orders_sample.csv

# Windows
dir data\orders_sample.csv
```

### Dashboard Không Load

1. **Kiểm tra terminal** có lỗi gì không
2. **Refresh browser** (Ctrl+F5)
3. **Clear browser cache**
4. **Thử trình duyệt khác**
5. **Kiểm tra firewall** có block port không

### Performance Issues

```bash
# Tăng memory limit cho Streamlit
streamlit run app.py --server.maxUploadSize 1000

# Giảm kích thước dữ liệu test
# Sửa file data/orders_sample.csv để có ít rows hơn
```

## ✅ Checklist Cài Đặt Thành Công

- [ ] Python 3.8+ installed và trong PATH
- [ ] pip hoạt động bình thường
- [ ] Virtual environment được tạo và activated
- [ ] Tất cả packages trong requirements.txt installed
- [ ] VS Code có Python extension
- [ ] Dashboard chạy được với `streamlit run app.py`
- [ ] Có thể truy cập <http://localhost:8501>
- [ ] Dashboard hiển thị data và charts
- [ ] Tất cả trang menu hoạt động bình thường

## 📞 Hỗ Trợ Thêm

### Self-Help Resources

- **README.md**: Hướng dẫn tổng quan
- **docs/user_guide.md**: Hướng dẫn sử dụng
- **Terminal logs**: Thông tin debug chi tiết

### Contact Support

- **Email**: <support@company.com>
- **Slack**: #fulfillment-dashboard
- **Internal Wiki**: [Link to internal docs]

### Bug Report Template

```
**Environment:**
- OS: [Windows 11/macOS 12/Ubuntu 20.04]
- Python: [3.11.0]
- Browser: [Chrome 119]

**Steps to Reproduce:**
1.
2.
3.

**Expected Result:**

**Actual Result:**

**Screenshots:**

**Terminal Logs:**
```

---

_Cài đặt thành công là bước đầu tiên để tận dụng tối đa Fulfillment Dashboard!_
