#!/usr/bin/env python3
"""
Configuration Validation Script
Kiểm tra tính hợp lệ của cấu hình
"""

import json
import os
import sys
from pathlib import Path


def load_config():
    """Load and validate configuration"""
    config_path = Path("config/system_config.json")

    if not config_path.exists():
        print("❌ system_config.json not found!")
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print("✅ Configuration file loaded successfully")
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return None


def validate_structure(config):
    """Validate configuration structure"""
    required_sections = [
        "system",
        "credentials",
        "logging",
        "data_processing",
        "notifications",
        "scheduling",
        "google_sheets",
    ]

    missing_sections = []
    for section in required_sections:
        if section not in config:
            missing_sections.append(section)

    if missing_sections:
        print(f"❌ Missing sections: {', '.join(missing_sections)}")
        return False

    print("✅ All required sections present")
    return True


def validate_env_vars(config):
    """Check environment variables"""
    env_vars = [
        "ONE_USERNAME",
        "ONE_PASSWORD",
        "EMAIL_ADDRESS",
        "EMAIL_PASSWORD",
        "SLACK_WEBHOOK_URL",
    ]

    missing_vars = []
    for var in env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Create a .env file or set these variables")
    else:
        print("✅ All environment variables set")


def validate_google_sheets(config):
    """Validate Google Sheets configuration"""
    gs_config = config.get("google_sheets", {})

    if gs_config.get("enabled", False):
        spreadsheet_id = gs_config.get("spreadsheet_id")
        credentials_file = gs_config.get("credentials_file")

        if not spreadsheet_id:
            print("❌ Google Sheets enabled but no spreadsheet_id provided")
            return False

        if credentials_file and not Path(credentials_file).exists():
            print(f"⚠️  Credentials file not found: {credentials_file}")

        print("✅ Google Sheets configuration valid")
    else:
        print("ℹ️  Google Sheets integration disabled")

    return True


def main():
    """Main validation function"""
    print("🔍 Validating Configuration...")
    print("=" * 40)

    # Load configuration
    config = load_config()
    if not config:
        sys.exit(1)

    # Validate structure
    if not validate_structure(config):
        sys.exit(1)

    # Check environment variables
    validate_env_vars(config)

    # Validate Google Sheets
    validate_google_sheets(config)

    print("=" * 40)
    print("🎉 Configuration validation completed!")

    # Display summary
    print("\n📊 Configuration Summary:")
    print(f"- ONE URL: {config['system']['one_url']}")
    print(f"- Logging Level: {config['logging']['level']}")
    print(f"- Max Test Rows: {config['data_processing']['max_rows_for_testing']}")
    print(
        f"- Email Notifications: {'✅' if config['notifications']['email']['enabled'] else '❌'}"
    )
    print(
        f"- Slack Notifications: {'✅' if config['notifications']['slack']['enabled'] else '❌'}"
    )
    print(f"- Scheduling: {'✅' if config['scheduling']['enabled'] else '❌'}")
    print(f"- Google Sheets: {'✅' if config['google_sheets']['enabled'] else '❌'}")


if __name__ == "__main__":
    main()
