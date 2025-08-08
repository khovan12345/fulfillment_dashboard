#!/usr/bin/env python3
"""
Configuration Manager
Quản lý cấu hình hệ thống
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class ConfigManager:
    def __init__(self):
        self.config_dir = Path("config")
        self.system_config_path = self.config_dir / "system_config.json"
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def backup_config(self):
        """Backup current configuration"""
        if self.system_config_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"system_config_{timestamp}.json"
            shutil.copy2(self.system_config_path, backup_path)
            print(f"✅ Configuration backed up to: {backup_path}")
            return backup_path
        return None

    def load_config(self):
        """Load current configuration"""
        try:
            with open(self.system_config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Configuration file not found")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return None

    def save_config(self, config):
        """Save configuration with backup"""
        # Create backup first
        self.backup_config()

        # Save new configuration
        with open(self.system_config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print("✅ Configuration saved successfully")

    def update_setting(self, section, key, value):
        """Update a specific setting"""
        config = self.load_config()
        if not config:
            return False

        if section not in config:
            config[section] = {}

        config[section][key] = value
        self.save_config(config)
        print(f"✅ Updated {section}.{key} = {value}")
        return True

    def enable_feature(self, feature):
        """Enable a specific feature"""
        features = {
            "email": ("notifications.email", "enabled", True),
            "slack": ("notifications.slack", "enabled", True),
            "scheduling": ("scheduling", "enabled", True),
            "google_sheets": ("google_sheets", "enabled", True),
            "fast_mode": ("data_processing", "enable_fast_mode", True),
        }

        if feature in features:
            section, key, value = features[feature]
            if "." in section:
                main_section, sub_section = section.split(".")
                config = self.load_config()
                if main_section not in config:
                    config[main_section] = {}
                if sub_section not in config[main_section]:
                    config[main_section][sub_section] = {}
                config[main_section][sub_section][key] = value
                self.save_config(config)
            else:
                self.update_setting(section, key, value)
            print(f"✅ Enabled {feature}")
        else:
            print(f"❌ Unknown feature: {feature}")

    def disable_feature(self, feature):
        """Disable a specific feature"""
        features = {
            "email": ("notifications.email", "enabled", False),
            "slack": ("notifications.slack", "enabled", False),
            "scheduling": ("scheduling", "enabled", False),
            "google_sheets": ("google_sheets", "enabled", False),
            "fast_mode": ("data_processing", "enable_fast_mode", False),
        }

        if feature in features:
            section, key, value = features[feature]
            if "." in section:
                main_section, sub_section = section.split(".")
                config = self.load_config()
                if main_section in config and sub_section in config[main_section]:
                    config[main_section][sub_section][key] = value
                    self.save_config(config)
            else:
                self.update_setting(section, key, value)
            print(f"❌ Disabled {feature}")
        else:
            print(f"❌ Unknown feature: {feature}")

    def show_status(self):
        """Show current configuration status"""
        config = self.load_config()
        if not config:
            return

        print("📊 Current Configuration Status:")
        print("=" * 40)

        # System settings
        system = config.get("system", {})
        print(f"🌐 ONE URL: {system.get('one_url', 'N/A')}")
        print(
            f"⏱️  Timeouts: Login={system.get('login_timeout', 'N/A')}s, Page={system.get('page_load_timeout', 'N/A')}s"
        )

        # Features status
        email_enabled = (
            config.get("notifications", {}).get("email", {}).get("enabled", False)
        )
        slack_enabled = (
            config.get("notifications", {}).get("slack", {}).get("enabled", False)
        )
        scheduling_enabled = config.get("scheduling", {}).get("enabled", False)
        gs_enabled = config.get("google_sheets", {}).get("enabled", False)
        fast_mode = config.get("data_processing", {}).get("enable_fast_mode", False)

        print(f"📧 Email: {'✅' if email_enabled else '❌'}")
        print(f"💬 Slack: {'✅' if slack_enabled else '❌'}")
        print(f"⏰ Scheduling: {'✅' if scheduling_enabled else '❌'}")
        print(f"📊 Google Sheets: {'✅' if gs_enabled else '❌'}")
        print(f"🚀 Fast Mode: {'✅' if fast_mode else '❌'}")

        # Environment variables
        env_vars = [
            "ONE_USERNAME",
            "ONE_PASSWORD",
            "EMAIL_ADDRESS",
            "SLACK_WEBHOOK_URL",
        ]
        missing_vars = [var for var in env_vars if not os.getenv(var)]

        if missing_vars:
            print(f"⚠️  Missing env vars: {', '.join(missing_vars)}")
        else:
            print("✅ All environment variables set")


def main():
    """Main CLI interface"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python config_manager.py status")
        print("  python config_manager.py enable <feature>")
        print("  python config_manager.py disable <feature>")
        print("  python config_manager.py backup")
        print("")
        print("Features: email, slack, scheduling, google_sheets, fast_mode")
        return

    manager = ConfigManager()
    command = sys.argv[1]

    if command == "status":
        manager.show_status()
    elif command == "backup":
        manager.backup_config()
    elif command == "enable" and len(sys.argv) > 2:
        manager.enable_feature(sys.argv[2])
    elif command == "disable" and len(sys.argv) > 2:
        manager.disable_feature(sys.argv[2])
    else:
        print("❌ Invalid command")


if __name__ == "__main__":
    main()
