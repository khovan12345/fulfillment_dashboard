#!/usr/bin/env python3
"""
Test cơ bản cho Google Sheets
"""

import json
import os
import sys
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.append(str(Path(__file__).parent.parent))

def test_basic_connection():
    """Test kết nối cơ bản"""
    print("🔍 Kiểm tra cơ bản...")
    
    # 1. Kiểm tra file cấu hình
    config_path = Path("config/system_config.json")
    print(f"📁 Config file: {config_path}")
    print(f"✅ Tồn tại: {config_path.exists()}")
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✅ Config hợp lệ")
            
            # Kiểm tra Google Sheets config
            gs_config = config.get("google_sheets", {})
            print(f"📊 Spreadsheet ID: {gs_config.get('spreadsheet_id', 'CHƯA CÓ')}")
            
        except Exception as e:
            print(f"❌ Lỗi đọc config: {e}")
    
    # 2. Kiểm tra credentials
    creds_path = Path("config/service_account.json")
    print(f"\n🔑 Credentials file: {creds_path}")
    print(f"✅ Tồn tại: {creds_path.exists()}")
    
    # 3. Kiểm tra thư viện
    print("\n📚 Kiểm tra thư viện:")
    libraries = [
        "gspread",
        "google.oauth2.service_account",
        "google.auth",
        "pandas",
        "streamlit"
    ]
    
    for lib in libraries:
        try:
            __import__(lib)
            print(f"✅ {lib}")
        except ImportError:
            print(f"❌ {lib} - Chưa cài đặt")
    
    print("\n" + "="*50)
    print("💡 HƯỚNG DẪN:")
    print("1. Nếu thiếu credentials, chạy: python scripts/setup_google_sheets.py")
    print("2. Nếu thiếu thư viện, chạy: pip install -r requirements.txt")
    print("3. Test đầy đủ: python scripts/test_google_connection.py")
    print("4. Quản lý sheets: python scripts/gs_manager.py")

if __name__ == "__main__":
    test_basic_connection()
