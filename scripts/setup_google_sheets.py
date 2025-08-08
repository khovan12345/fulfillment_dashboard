#!/usr/bin/env python3
"""
Google Sheets Setup Script
Khởi tạo Google Sheets cho hệ thống Fulfillment Dashboard
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.append(str(Path(__file__).parent.parent))

try:
    import gspread
    from google.oauth2.service_account import Credentials
    import pandas as pd
except ImportError:
    print("❌ Thiếu thư viện cần thiết!")
    print("Cài đặt: pip install gspread google-auth pandas openpyxl")
    sys.exit(1)

class GoogleSheetsSetup:
    def __init__(self):
        self.config_path = Path("config/system_config.json")
        self.credentials_path = Path("config/service_account.json")
        self.config = self.load_config()
        self.client = None
        self.spreadsheet = None
        
    def load_config(self):
        """Tải cấu hình hệ thống"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file cấu hình: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Lỗi đọc file JSON: {e}")
            sys.exit(1)
    
    def setup_credentials(self):
        """Thiết lập xác thực Google API"""
        if not self.credentials_path.exists():
            print(f"❌ Không tìm thấy file credentials: {self.credentials_path}")
            print("💡 Hướng dẫn tạo service account:")
            print("1. Truy cập: https://console.cloud.google.com/")
            print("2. Tạo project mới hoặc chọn project có sẵn")
            print("3. Bật Google Sheets API và Google Drive API")
            print("4. Tạo Service Account và tải file JSON")
            print("5. Đặt file JSON vào config/service_account.json")
            return False
        
        try:
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=scope
            )
            self.client = gspread.authorize(creds)
            print("✅ Kết nối Google API thành công")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi kết nối Google API: {e}")
            return False
    
    def create_or_open_spreadsheet(self):
        """Tạo hoặc mở spreadsheet"""
        spreadsheet_id = self.config.get("google_sheets", {}).get("spreadsheet_id")
        
        if spreadsheet_id:
            try:
                self.spreadsheet = self.client.open_by_key(spreadsheet_id)
                print(f"✅ Đã mở spreadsheet: {self.spreadsheet.title}")
                return True
            except Exception as e:
                print(f"⚠️  Không thể mở spreadsheet: {e}")
                print("Sẽ tạo spreadsheet mới...")
        
        # Tạo spreadsheet mới
        try:
            self.spreadsheet = self.client.create("Fulfillment Dashboard - Hệ thống ONE")
            print(f"✅ Đã tạo spreadsheet mới: {self.spreadsheet.title}")
            print(f"📋 ID: {self.spreadsheet.id}")
            print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{self.spreadsheet.id}")
            
            # Cập nhật config với ID mới
            self.update_config_with_spreadsheet_id(self.spreadsheet.id)
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo spreadsheet: {e}")
            return False
    
    def update_config_with_spreadsheet_id(self, spreadsheet_id):
        """Cập nhật config với spreadsheet ID mới"""
        self.config["google_sheets"]["spreadsheet_id"] = spreadsheet_id
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Đã cập nhật config với Spreadsheet ID: {spreadsheet_id}")
    
    def setup_config_worksheet(self):
        """Tạo worksheet cấu hình hệ thống"""
        try:
            # Tạo hoặc lấy worksheet
            try:
                worksheet = self.spreadsheet.worksheet("Cấu hình hệ thống")
                worksheet.clear()
            except:
                worksheet = self.spreadsheet.add_worksheet(
                    title="Cấu hình hệ thống", 
                    rows=100, 
                    cols=20
                )
            
            # Header
            headers = [
                ["🏗️ DASHBOARD FULFILLMENT - CẤU HÌNH HỆ THỐNG", "", ""],
                ["📅 Cập nhật lần cuối:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ""],
                ["", "", ""],
                ["PHẦN", "CÀI ĐẶT", "GIÁ TRỊ", "MÔ TẢ"]
            ]
            
            # Cấu hình hệ thống
            system_config = [
                ["🌐 HỆ THỐNG", "URL chính", self.config["system"]["one_url"], "Địa chỉ hệ thống ONE"],
                ["", "URL đơn hàng", self.config["system"]["orders_url"], "Đường dẫn trang đơn hàng"],
                ["", "Thời gian chờ đăng nhập", f"{self.config['system']['login_timeout']} giây", "Thời gian chờ tối đa để đăng nhập"],
                ["", "Thời gian tải trang", f"{self.config['system']['page_load_timeout']} giây", "Thời gian chờ tối đa để tải trang"],
                ["", "Tối ưu JavaScript", "✅ Bật" if self.config["system"]["use_javascript_optimization"] else "❌ Tắt", "Sử dụng tối ưu hóa JavaScript"],
                ["", "Thời gian phiên", f"{self.config['system']['session_timeout']} giây", "Thời gian phiên làm việc"],
                ["", "", ""],
                
                ["📊 XỬ LÝ DỮ LIỆU", "Số dòng test tối đa", str(self.config["data_processing"]["max_rows_for_testing"]), "Giới hạn dữ liệu khi test"],
                ["", "Chế độ nhanh", "✅ Bật" if self.config["data_processing"]["enable_fast_mode"] else "❌ Tắt", "Xử lý dữ liệu nhanh"],
                ["", "Định dạng xuất", ", ".join(self.config["data_processing"]["export_formats"]), "Các định dạng file xuất"],
                ["", "", ""],
                
                ["📧 THÔNG BÁO EMAIL", "Trạng thái", "✅ Bật" if self.config["notifications"]["email"]["enabled"] else "❌ Tắt", "Gửi thông báo qua email"],
                ["", "SMTP Server", self.config["notifications"]["email"]["smtp_server"], "Máy chủ gửi email"],
                ["", "SMTP Port", str(self.config["notifications"]["email"]["smtp_port"]), "Cổng SMTP"],
                ["", "Người nhận", ", ".join(self.config["notifications"]["email"]["recipients"]), "Danh sách email nhận thông báo"],
                ["", "", ""],
                
                ["💬 THÔNG BÁO SLACK", "Trạng thái", "✅ Bật" if self.config["notifications"]["slack"]["enabled"] else "❌ Tắt", "Gửi thông báo qua Slack"],
                ["", "", ""],
                
                ["⏰ TỰ ĐỘNG HÓA", "Trạng thái", "✅ Bật" if self.config["scheduling"]["enabled"] else "❌ Tắt", "Chạy tự động theo lịch"],
                ["", "Chu kỳ", f"{self.config['scheduling']['interval_hours']} giờ", "Khoảng thời gian giữa các lần chạy"],
                ["", "", ""],
                
                ["📊 GOOGLE SHEETS", "Trạng thái", "✅ Bật" if self.config["google_sheets"]["enabled"] else "❌ Tắt", "Đồng bộ với Google Sheets"],
                ["", "Spreadsheet ID", self.config["google_sheets"]["spreadsheet_id"], "ID của bảng tính Google"],
                ["", "Tự động đồng bộ", "✅ Bật" if self.config["google_sheets"]["auto_sync"] else "❌ Tắt", "Tự động cập nhật dữ liệu"],
            ]
            
            # Ghi dữ liệu
            all_data = headers + system_config
            
            # Ghi từng dòng để tránh lỗi
            for i, row in enumerate(all_data, 1):
                worksheet.update(f'A{i}:D{i}', [row])
            
            # Format
            self.format_config_worksheet(worksheet)
            
            print("✅ Đã tạo worksheet 'Cấu hình hệ thống'")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo worksheet cấu hình: {e}")
            return False
    
    def setup_sla_rules_worksheet(self):
        """Tạo worksheet quy tắc SLA"""
        try:
            try:
                worksheet = self.spreadsheet.worksheet("Quy tắc SLA")
                worksheet.clear()
            except:
                worksheet = self.spreadsheet.add_worksheet(
                    title="Quy tắc SLA", 
                    rows=100, 
                    cols=15
                )
            
            # Header và dữ liệu SLA
            headers = [
                ["📋 QUY TẮC SLA - THỜI GIAN XỬ LÝ ĐỚN HÀNG", "", "", "", "", ""],
                ["📅 Cập nhật:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "", "", "", ""],
                ["", "", "", "", "", ""],
                ["LOẠI ĐƠN HÀNG", "THỜI GIAN XÁC NHẬN", "THỜI GIAN GIAO HÀNG", "MỨC ĐỘ ƯU TIÊN", "GHI CHÚ", "TRẠNG THÁI", "NGƯỜI PHỤ TRÁCH"]
            ]
            
            sla_data = [
                ["Đơn thường", "2 giờ", "24 giờ", "Bình thường", "Đơn hàng thông thường", "✅ Hoạt động", "Team CS"],
                ["Đơn gấp", "30 phút", "4 giờ", "Cao", "Đơn hàng ưu tiên cao", "✅ Hoạt động", "Supervisor"],
                ["Đơn VIP", "15 phút", "2 giờ", "Rất cao", "Khách hàng VIP", "✅ Hoạt động", "Manager"],
                ["Đơn COD", "1 giờ", "12 giờ", "Bình thường", "Thanh toán khi nhận hàng", "✅ Hoạt động", "Team CS"],
                ["Đơn xuất khẩu", "4 giờ", "72 giờ", "Bình thường", "Giao hàng quốc tế", "✅ Hoạt động", "Team Logistics"],
                ["", "", "", "", "", ""],
                ["📊 NGƯỠNG KPI", "", "", "", "", ""],
                ["Tỷ lệ xác nhận đúng hạn", "≥ 90%", "Bắt buộc", "Mục tiêu tối thiểu", "", ""],
                ["Tỷ lệ giao hàng đúng hạn", "≥ 85%", "Bắt buộc", "Mục tiêu tối thiểu", "", ""],
                ["Tỷ lệ hủy đơn tối đa", "≤ 10%", "Giới hạn", "Không được vượt quá", "", ""],
                ["Thời gian chờ tối đa", "≤ 12 giờ", "Cảnh báo", "Cần xử lý ngay", "", ""],
            ]
            
            all_data = headers + sla_data
            
            # Ghi dữ liệu
            for i, row in enumerate(all_data, 1):
                worksheet.update(f'A{i}:G{i}', [row])
            
            # Format
            self.format_sla_worksheet(worksheet)
            
            print("✅ Đã tạo worksheet 'Quy tắc SLA'")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo worksheet SLA: {e}")
            return False
    
    def setup_automation_logs_worksheet(self):
        """Tạo worksheet log tự động hóa"""
        try:
            try:
                worksheet = self.spreadsheet.worksheet("Nhật ký tự động")
                worksheet.clear()
            except:
                worksheet = self.spreadsheet.add_worksheet(
                    title="Nhật ký tự động", 
                    rows=1000, 
                    cols=12
                )
            
            # Header
            headers = [
                ["📝 NHẬT KÝ HỆ THỐNG TỰ ĐỘNG", "", "", "", "", "", "", "", "", ""],
                ["📅 Tạo:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", "", ""],
                ["THỜI GIAN", "HOẠT ĐỘNG", "TRẠNG THÁI", "SỐ ĐƠN XỬ LÝ", "THÀNH CÔNG", "LỖI", "THỜI GIAN XỬ LÝ", "NGƯỜI DÙNG", "GHI CHÚ", "CHI TIẾT", "ID PHIÊN"]
            ]
            
            # Dữ liệu mẫu
            sample_data = [
                [
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Khởi tạo hệ thống",
                    "✅ Thành công",
                    "0",
                    "1",
                    "0",
                    "< 1s",
                    "System",
                    "Thiết lập Google Sheets",
                    "Tạo các worksheet cần thiết",
                    "SETUP_001"
                ],
                ["", "", "", "", "", "", "", "", "", ""],
                ["📋 HƯỚNG DẪN SỬ DỤNG:", "", "", "", "", "", "", "", "", ""],
                ["- Hệ thống sẽ tự động ghi log vào đây", "", "", "", "", "", "", "", "", ""],
                ["- Mỗi hành động sẽ có ID phiên riêng", "", "", "", "", "", "", "", "", ""],
                ["- Kiểm tra cột TRẠNG THÁI để biết kết quả", "", "", "", "", "", "", "", "", ""],
                ["- Xem cột CHI TIẾT khi có lỗi", "", "", "", "", "", "", "", "", "", ""],
            ]
            
            all_data = headers + sample_data
            
            # Ghi dữ liệu
            for i, row in enumerate(all_data, 1):
                worksheet.update(f'A{i}:K{i}', [row])
            
            # Format
            self.format_logs_worksheet(worksheet)
            
            print("✅ Đã tạo worksheet 'Nhật ký tự động'")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo worksheet logs: {e}")
            return False
    
    def format_config_worksheet(self, worksheet):
        """Format worksheet cấu hình"""
        try:
            # Header chính
            worksheet.format('A1:D1', {
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 1.0},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                'horizontalAlignment': 'CENTER'
            })
            
            # Header cột
            worksheet.format('A4:D4', {
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                'textFormat': {'bold': True},
                'horizontalAlignment': 'CENTER'
            })
            
            # Cột phần
            worksheet.format('A:A', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.95, 'green': 0.95, 'blue': 0.95}
            })
            
        except Exception as e:
            print(f"⚠️  Không thể format worksheet: {e}")
    
    def format_sla_worksheet(self, worksheet):
        """Format worksheet SLA"""
        try:
            # Header chính
            worksheet.format('A1:G1', {
                'backgroundColor': {'red': 1.0, 'green': 0.6, 'blue': 0.2},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                'horizontalAlignment': 'CENTER'
            })
            
            # Header cột
            worksheet.format('A4:G4', {
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                'textFormat': {'bold': True},
                'horizontalAlignment': 'CENTER'
            })
            
        except Exception as e:
            print(f"⚠️  Không thể format worksheet: {e}")
    
    def format_logs_worksheet(self, worksheet):
        """Format worksheet logs"""
        try:
            # Header chính
            worksheet.format('A1:K1', {
                'backgroundColor': {'red': 0.6, 'green': 0.8, 'blue': 0.6},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                'horizontalAlignment': 'CENTER'
            })
            
            # Header cột
            worksheet.format('A4:K4', {
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                'textFormat': {'bold': True},
                'horizontalAlignment': 'CENTER'
            })
            
        except Exception as e:
            print(f"⚠️  Không thể format worksheet: {e}")
    
    def setup_permissions(self):
        """Thiết lập quyền truy cập"""
        try:
            # Chia sẻ với email trong config (nếu có)
            email_recipients = self.config.get("notifications", {}).get("email", {}).get("recipients", [])
            
            for email in email_recipients:
                if email != "admin@example.com":  # Bỏ qua email mẫu
                    try:
                        self.spreadsheet.share(email, perm_type='user', role='writer')
                        print(f"✅ Đã chia sẻ với: {email}")
                    except Exception as e:
                        print(f"⚠️  Không thể chia sẻ với {email}: {e}")
            
            print("�� Lưu ý: Hãy chia sẻ spreadsheet với nhân viên cần thiết")
            
        except Exception as e:
            print(f"⚠️  Lỗi thiết lập quyền: {e}")
    
    def run(self):
        """Chạy script setup"""
        print("🚀 BẮT ĐẦU THIẾT LẬP GOOGLE SHEETS")
        print("=" * 50)
        
        # Kiểm tra credentials
        if not self.setup_credentials():
            return False
        
        # Tạo/mở spreadsheet
        if not self.create_or_open_spreadsheet():
            return False
        
        # Tạo các worksheets
        success = True
        success &= self.setup_config_worksheet()
        success &= self.setup_sla_rules_worksheet()
        success &= self.setup_automation_logs_worksheet()
        
        if success:
            # Thiết lập quyền
            self.setup_permissions()
            
            print("=" * 50)
            print("🎉 THIẾT LẬP HOÀN TẤT!")
            print(f"📊 Spreadsheet: {self.spreadsheet.title}")
            print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{self.spreadsheet.id}")
            print(f"📋 ID: {self.spreadsheet.id}")
            print("")
            print("📝 Các worksheet đã tạo:")
            print("  - Cấu hình hệ thống")
            print("  - Quy tắc SLA")  
            print("  - Nhật ký tự động")
            print("")
            print("💡 Bước tiếp theo:")
            print("  1. Chia sẻ spreadsheet với nhân viên")
            print("  2. Cập nhật quy tắc SLA theo yêu cầu")
            print("  3. Kiểm tra cấu hình hệ thống")
            
            return True
        else:
            print("❌ Có lỗi xảy ra trong quá trình thiết lập")
            return False

def main():
    """Hàm chính"""
    try:
        setup = GoogleSheetsSetup()
        setup.run()
    except KeyboardInterrupt:
        print("\n⚠️  Đã hủy thiết lập")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()
