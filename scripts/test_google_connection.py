#!/usr/bin/env python3
"""
Test Google Sheets Connection
Kiểm tra kết nối Google Sheets
"""

import json
import sys
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.append(str(Path(__file__).parent.parent))

def test_credentials():
    """Kiểm tra file credentials"""
    credentials_path = Path("config/service_account.json")
    
    if not credentials_path.exists():
        print("❌ Không tìm thấy file credentials")
        print(f"📂 Đường dẫn: {credentials_path.absolute()}")
        print("💡 Tạo file service_account.json trong thư mục config/")
        return False
    
    try:
        with open(credentials_path, 'r') as f:
            creds = json.load(f)
        
        required_fields = ["type", "project_id", "private_key", "client_email"]
        missing_fields = [field for field in required_fields if field not in creds]
        
        if missing_fields:
            print(f"❌ File credentials thiếu các trường: {', '.join(missing_fields)}")
            return False
        
        print("✅ File credentials hợp lệ")
        print(f"📧 Service email: {creds['client_email']}")
        print(f"🏗️ Project ID: {creds['project_id']}")
        return True
        
    except json.JSONDecodeError:
        print("❌ File credentials không phải JSON hợp lệ")
        return False
    except Exception as e:
        print(f"❌ Lỗi đọc credentials: {e}")
        return False

def test_config():
    """Kiểm tra file config"""
    config_path = Path("config/system_config.json")
    
    if not config_path.exists():
        print("❌ Không tìm thấy file config")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        gs_config = config.get("google_sheets", {})
        
        print("✅ File config hợp lệ")
        print(f"📊 Google Sheets: {'✅ Bật' if gs_config.get('enabled') else '❌ Tắt'}")
        print(f"📋 Spreadsheet ID: {gs_config.get('spreadsheet_id', 'Chưa có')}")
        print(f"🔄 Auto sync: {'✅' if gs_config.get('auto_sync') else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi đọc config: {e}")
        return False

def test_connection():
    """Test kết nối thực tế"""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("❌ Thiếu thư viện!")
        print("Cài đặt: pip install gspread google-auth")
        return False
    
    try:
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(
            "config/service_account.json", scopes=scope
        )
        client = gspread.authorize(creds)
        
        # Test tạo spreadsheet tạm
        test_sheet = client.create("Test Connection - Fulfillment")
        print("✅ Kết nối Google API thành công")
        print(f"📊 Test spreadsheet: {test_sheet.title}")
        print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{test_sheet.id}")
        
        # Xóa test spreadsheet
        client.del_spreadsheet_by_key(test_sheet.id)
        print("🗑️ Đã xóa test spreadsheet")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        print("💡 Kiểm tra:")
        print("  - Service account có quyền đúng?")
        print("  - APIs đã được bật?")
        print("  - Internet kết nối ổn định?")
        return False

def main():
    """Hàm chính"""
    print("🔍 KIỂM TRA KẾT NỐI GOOGLE SHEETS")
    print("=" * 40)
    
    success = True
    
    print("\n1️⃣ Kiểm tra file credentials...")
    success &= test_credentials()
    
    print("\n2️⃣ Kiểm tra file config...")
    success &= test_config()
    
    print("\n3️⃣ Test kết nối thực tế...")
    success &= test_connection()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 TẤT CẢ KIỂM TRA THÀNH CÔNG!")
        print("✅ Sẵn sàng chạy script setup_google_sheets.py")
    else:
        print("❌ CÓ LỖI CẦN KHẮC PHỤC")
        print("📖 Xem hướng dẫn: scripts/huong_dan_google_sheets.md")

if __name__ == "__main__":
    main()
