"""
Fulfillment Dashboard Configuration
Cấu hình cho Dashboard theo dõi đơn hàng
"""

import json
import os
from pathlib import Path

# Load system configuration from JSON
CONFIG_DIR = Path(__file__).parent
SYSTEM_CONFIG_PATH = CONFIG_DIR / "system_config.json"


def load_system_config():
    """Load system configuration from JSON file"""
    try:
        with open(SYSTEM_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Warning: {SYSTEM_CONFIG_PATH} not found, using defaults")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing {SYSTEM_CONFIG_PATH}: {e}")
        return {}


# Load .env if present
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

# Load system config
SYSTEM_CONFIG = load_system_config()


# Extract environment variables
def get_env_var(var_name, default=None):
    """Get environment variable with fallback"""
    return os.getenv(var_name, default)


# System Settings
ONE_URL = SYSTEM_CONFIG.get("system", {}).get("one_url", "https://one.tga.com.vn")
ORDERS_URL = SYSTEM_CONFIG.get("system", {}).get(
    "orders_url", "https://one.tga.com.vn/so/"
)
IMPLICIT_WAIT = SYSTEM_CONFIG.get("system", {}).get("implicit_wait", 3)
PAGE_LOAD_TIMEOUT = SYSTEM_CONFIG.get("system", {}).get("page_load_timeout", 15)
LOGIN_TIMEOUT = SYSTEM_CONFIG.get("system", {}).get("login_timeout", 8)
USE_JAVASCRIPT_OPTIMIZATION = SYSTEM_CONFIG.get("system", {}).get(
    "use_javascript_optimization", True
)
SESSION_TIMEOUT = SYSTEM_CONFIG.get("system", {}).get("session_timeout", 3600)

# Credentials (from environment variables)
ONE_USERNAME = get_env_var("ONE_USERNAME")
ONE_PASSWORD = get_env_var("ONE_PASSWORD")
EMAIL_ADDRESS = get_env_var("EMAIL_ADDRESS")
EMAIL_PASSWORD = get_env_var("EMAIL_PASSWORD")
SLACK_WEBHOOK_URL = get_env_var("SLACK_WEBHOOK_URL")

# Logging
LOG_LEVEL = SYSTEM_CONFIG.get("logging", {}).get("level", "INFO")

# Data Processing
MAX_ROWS_FOR_TESTING = SYSTEM_CONFIG.get("data_processing", {}).get(
    "max_rows_for_testing", 2000
)
ENABLE_FAST_MODE = SYSTEM_CONFIG.get("data_processing", {}).get(
    "enable_fast_mode", False
)
EXPORT_FORMATS = SYSTEM_CONFIG.get("data_processing", {}).get(
    "export_formats", ["json", "excel"]
)

# Notifications
EMAIL_ENABLED = (
    SYSTEM_CONFIG.get("notifications", {}).get("email", {}).get("enabled", False)
)
SMTP_SERVER = (
    SYSTEM_CONFIG.get("notifications", {})
    .get("email", {})
    .get("smtp_server", "smtp.gmail.com")
)
SMTP_PORT = (
    SYSTEM_CONFIG.get("notifications", {}).get("email", {}).get("smtp_port", 587)
)
EMAIL_RECIPIENTS = (
    SYSTEM_CONFIG.get("notifications", {}).get("email", {}).get("recipients", [])
)

SLACK_ENABLED = (
    SYSTEM_CONFIG.get("notifications", {}).get("slack", {}).get("enabled", False)
)

# Scheduling
SCHEDULING_ENABLED = SYSTEM_CONFIG.get("scheduling", {}).get("enabled", False)
INTERVAL_HOURS = SYSTEM_CONFIG.get("scheduling", {}).get("interval_hours", 2)

# Google Sheets
GOOGLE_SHEETS_ENABLED = SYSTEM_CONFIG.get("google_sheets", {}).get("enabled", True)
SPREADSHEET_ID = SYSTEM_CONFIG.get("google_sheets", {}).get("spreadsheet_id", "")
# Ưu tiên lấy đường dẫn credentials từ biến môi trường GOOGLE_CREDENTIALS_FILE (hỗ trợ .env)
CREDENTIALS_FILE = os.getenv(
    "GOOGLE_CREDENTIALS_FILE",
    SYSTEM_CONFIG.get("google_sheets", {}).get("credentials_file", "config/service_account.json"),
)
AUTO_SYNC = SYSTEM_CONFIG.get("google_sheets", {}).get("auto_sync", True)
WORKSHEETS = SYSTEM_CONFIG.get("google_sheets", {}).get("worksheets", {})

# Dashboard Settings (legacy compatibility)
DASHBOARD_TITLE = "🚀 Fulfillment Dashboard - Hệ thống ONE"
SIDEBAR_TITLE = "📊 Điều Khiển Dashboard"

# KPI Thresholds
KPI_THRESHOLDS = {
    "confirmation_target": 0.90,  # 90% đúng hạn
    "delivery_target": 0.85,  # 85% đúng hạn
    "cancellation_limit": 0.10,  # Tối đa 10% hủy
    "pending_hours_limit": 12,  # Tối đa 12 giờ chờ
}

# Colors
COLORS = {
    "primary": "#1f77b4",
    "success": "#2ca02c",
    "warning": "#ff7f0e",
    "danger": "#d62728",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
}

# Chart Settings
CHART_CONFIG = {
    "height": 400,
    "showlegend": True,
    "margin": dict(l=50, r=50, t=50, b=50),
}

# Data Settings
DATA_PATH = "data/orders_sample.csv"
REFRESH_INTERVAL = 300  # 5 phút

# Export configuration for external use
CONFIG_EXPORT = {
    "system": {
        "one_url": ONE_URL,
        "orders_url": ORDERS_URL,
        "implicit_wait": IMPLICIT_WAIT,
        "page_load_timeout": PAGE_LOAD_TIMEOUT,
        "login_timeout": LOGIN_TIMEOUT,
        "use_javascript_optimization": USE_JAVASCRIPT_OPTIMIZATION,
        "session_timeout": SESSION_TIMEOUT,
    },
    "credentials": {"username_env": "ONE_USERNAME", "password_env": "ONE_PASSWORD"},
    "logging": {"level": LOG_LEVEL},
    "data_processing": {
        "max_rows_for_testing": MAX_ROWS_FOR_TESTING,
        "enable_fast_mode": ENABLE_FAST_MODE,
        "export_formats": EXPORT_FORMATS,
    },
    "notifications": {"email_enabled": EMAIL_ENABLED, "slack_enabled": SLACK_ENABLED},
    "google_sheets": {
        "enabled": GOOGLE_SHEETS_ENABLED,
        "spreadsheet_id": SPREADSHEET_ID,
        "auto_sync": AUTO_SYNC,
    },
}
