#!/usr/bin/env python3
"""
Google Sheets Manager - Quản lý Google Sheets
Script tiện ích cho nhân viên
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.append(str(Path(__file__).parent.parent))

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("❌ Thiếu thư viện! Chạy: pip install gspread google-auth")
    sys.exit(1)

class GoogleSheetsManager:
    def __init__(self):
        self.config_path = Path("config/system_config.json")
        self.credentials_path = Path("config/service_account.json")
        self.client = None
        self.spreadsheet = None
        self.config = self.load_config()

    def load_config(self):
        """Tải cấu hình"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def connect(self):
        """Kết nối Google Sheets"""
        try:
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            # Ưu tiên biến môi trường GOOGLE_CREDENTIALS_FILE
            import os
            env_creds = os.getenv('GOOGLE_CREDENTIALS_FILE')
            creds_path = env_creds if env_creds else str(self.credentials_path)

            creds = Credentials.from_service_account_file(
                creds_path, scopes=scope
            )
            self.client = gspread.authorize(creds)

            spreadsheet_id = self.config.get("google_sheets", {}).get("spreadsheet_id")
            if spreadsheet_id:
                self.spreadsheet = self.client.open_by_key(spreadsheet_id)
                print(f"✅ Đã kết nối: {self.spreadsheet.title}")
                return True
            else:
                print("❌ Không tìm thấy Spreadsheet ID trong config")
                return False

        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False

    def log_activity(self, activity, status, details="", user="System"):
        """Ghi log hoạt động"""
        if not self.connect():
            return False

        try:
            worksheet = self.spreadsheet.worksheet("Nhật ký tự động")

            # Tìm dòng trống đầu tiên (sau header)
            values = worksheet.get_all_values()
            next_row = len([row for row in values if any(row)]) + 1

            # Tạo dữ liệu log
            log_data = [
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                activity,
                status,
                "0",  # Số đơn xử lý
                "1" if "thành công" in status.lower() else "0",  # Thành công
                "0" if "thành công" in status.lower() else "1",  # Lỗi
                "< 1s",  # Thời gian xử lý
                user,
                details,
                "",  # Chi tiết
                f"LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"  # ID phiên
            ]

            worksheet.update(f'A{next_row}:K{next_row}', [log_data])
            print(f"✅ Đã ghi log: {activity}")
            return True

        except Exception as e:
            print(f"❌ Lỗi ghi log: {e}")
            return False

    def update_config_value(self, section, setting, new_value):
        """Cập nhật giá trị cấu hình trên Google Sheets"""
        if not self.connect():
            return False

        try:
            worksheet = self.spreadsheet.worksheet("Cấu hình hệ thống")
            values = worksheet.get_all_values()

            # Tìm dòng chứa setting
            for i, row in enumerate(values):
                if len(row) >= 2 and row[1] == setting:
                    # Cập nhật giá trị
                    worksheet.update_cell(i + 1, 3, new_value)
                    print(f"✅ Đã cập nhật {setting}: {new_value}")

                    # Ghi log
                    self.log_activity(
                        f"Cập nhật cấu hình",
                        "✅ Thành công",
                        f"Thay đổi {setting} thành {new_value}"
                    )
                    return True

            print(f"❌ Không tìm thấy setting: {setting}")
            return False

        except Exception as e:
            print(f"❌ Lỗi cập nhật: {e}")
            return False

    def get_sla_rules(self):
        """Lấy quy tắc SLA"""
        if not self.connect():
            return []

        try:
            worksheet = self.spreadsheet.worksheet("Quy tắc SLA")
            values = worksheet.get_all_values()

            # Lấy dữ liệu SLA (bỏ qua header)
            sla_rules = []
            for row in values[4:]:  # Bỏ qua 4 dòng đầu
                if row and row[0] and "Đơn" in row[0]:
                    sla_rules.append({
                        "loai_don": row[0],
                        "thoi_gian_xac_nhan": row[1],
                        "thoi_gian_giao_hang": row[2],
                        "muc_do_uu_tien": row[3],
                        "ghi_chu": row[4] if len(row) > 4 else "",
                        "trang_thai": row[5] if len(row) > 5 else "",
                        "nguoi_phu_trach": row[6] if len(row) > 6 else ""
                    })

            return sla_rules

        except Exception as e:
            print(f"❌ Lỗi đọc SLA: {e}")
            return []

    def show_sla_summary(self):
        """Hiển thị tóm tắt SLA"""
        rules = self.get_sla_rules()

        if not rules:
            print("❌ Không có quy tắc SLA")
            return

        print("📋 QUY TẮC SLA HIỆN TẠI")
        print("=" * 50)

        for rule in rules:
            print(f"📦 {rule['loai_don']}")
            print(f"   ⏰ Xác nhận: {rule['thoi_gian_xac_nhan']}")
            print(f"   �� Giao hàng: {rule['thoi_gian_giao_hang']}")
            print(f"   🔥 Ưu tiên: {rule['muc_do_uu_tien']}")
            print(f"   👤 Phụ trách: {rule['nguoi_phu_trach']}")
            print(f"   📝 Ghi chú: {rule['ghi_chu']}")
            print()

    def show_recent_logs(self, limit=10):
        """Hiển thị log gần đây"""
        if not self.connect():
            return

        try:
            worksheet = self.spreadsheet.worksheet("Nhật ký tự động")
            values = worksheet.get_all_values()

            # Lấy log gần đây (bỏ qua header)
            logs = []
            for row in values[4:]:  # Bỏ qua header
                if row and row[0] and "/" in row[0]:  # Có thời gian
                    logs.append(row)

            # Lấy logs gần nhất
            recent_logs = logs[-limit:] if len(logs) > limit else logs

            print(f"📝 {len(recent_logs)} LOG GẦN NHẤT")
            print("=" * 60)

            for log in recent_logs:
                time = log[0] if len(log) > 0 else ""
                activity = log[1] if len(log) > 1 else ""
                status = log[2] if len(log) > 2 else ""
                user = log[7] if len(log) > 7 else ""
                details = log[8] if len(log) > 8 else ""

                print(f"🕐 {time}")
                print(f"📋 {activity}")
                print(f"📊 {status}")
                print(f"👤 {user}")
                if details:
                    print(f"💬 {details}")
                print("-" * 40)

        except Exception as e:
            print(f"❌ Lỗi đọc logs: {e}")

    def backup_sheets(self):
        """Backup Google Sheets"""
        if not self.connect():
            return False

        try:
            # Tạo bản sao
            backup_title = f"Backup - {self.spreadsheet.title} - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_sheet = self.client.copy(self.spreadsheet.id, title=backup_title)

            print(f"✅ Đã tạo backup: {backup_title}")
            print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{backup_sheet['id']}")

            # Ghi log
            self.log_activity(
                "Backup Google Sheets",
                "✅ Thành công",
                f"Tạo backup: {backup_title}"
            )

            return True

        except Exception as e:
            print(f"❌ Lỗi backup: {e}")
            return False

def main():
    """Menu chính"""
    manager = GoogleSheetsManager()

    while True:
        print("\n" + "=" * 50)
        print("📊 GOOGLE SHEETS MANAGER")
        print("=" * 50)
        print("1. 📋 Xem quy tắc SLA")
        print("2. 📝 Xem log gần đây")
        print("3. ✏️  Ghi log mới")
        print("4. 💾 Backup sheets")
        print("5. 🔗 Mở Google Sheets")
        print("6. ❌ Thoát")
        print()

        choice = input("👉 Chọn chức năng (1-6): ").strip()

        if choice == "1":
            manager.show_sla_summary()

        elif choice == "2":
            limit = input("Số log muốn xem (mặc định 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            manager.show_recent_logs(limit)

        elif choice == "3":
            activity = input("Hoạt động: ").strip()
            status = input("Trạng thái (✅ Thành công/❌ Lỗi): ").strip()
            details = input("Chi tiết (tùy chọn): ").strip()
            user = input("Người thực hiện (mặc định System): ").strip() or "System"

            if activity:
                manager.log_activity(activity, status, details, user)
            else:
                print("❌ Cần nhập hoạt động")

        elif choice == "4":
            confirm = input("Xác nhận backup? (y/N): ").strip().lower()
            if confirm == 'y':
                manager.backup_sheets()

        elif choice == "5":
            spreadsheet_id = manager.config.get("google_sheets", {}).get("spreadsheet_id")
            if spreadsheet_id:
                url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
                print(f"🔗 URL: {url}")
                print("💡 Copy URL trên và dán vào trình duyệt")
            else:
                print("❌ Không tìm thấy Spreadsheet ID")

        elif choice == "6":
            print("👋 Tạm biệt!")
            break

        else:
            print("❌ Lựa chọn không hợp lệ")

        input("\n⏎ Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
