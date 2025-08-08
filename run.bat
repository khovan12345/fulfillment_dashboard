@echo off
REM ===================================
REM MIA Fulfillment Dashboard v2.0 - Windows Launcher
REM Tối ưu hóa cho Windows
REM ===================================

echo 🚀 MIA Fulfillment Dashboard v2.0
echo ==================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Lỗi: Python chưa được cài đặt hoặc không có trong PATH
    echo 💡 Tải Python từ: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if not exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo 📦 Installing/updating dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Dependencies installed
) else (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

REM Clean up processes
echo 🔄 Cleaning up processes...
taskkill /f /im streamlit.exe >nul 2>&1

REM Start dashboard
echo 🌟 Starting dashboard...
if exist "main.py" (
    echo ✅ Using new structure v2.0
    python main.py
) else if exist "app.py" (
    echo ⚠️  Using legacy structure v1.0
    echo 💡 Consider upgrading to v2.0
    echo 🚀 Starting Streamlit on port 8502...
    streamlit run app.py --server.port 8502 --server.address 0.0.0.0
) else (
    echo ❌ No valid entry point found
    echo Expected: main.py v2.0 or app.py v1.0
    pause
    exit /b 1
)

pause
