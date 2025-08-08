"""
Setup script for Fulfillment Dashboard
Script cài đặt cho Dashboard
"""

from setuptools import find_packages, setup

setup(
    name="fulfillment-dashboard",
    version="1.0.0",
    description="Dashboard theo dõi tiến độ xác nhận đơn hàng và bàn giao vận chuyển",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="AI Assistant",
    author_email="support@company.com",
    packages=find_packages(),
    # Để tránh trùng lặp nguồn phụ thuộc, sử dụng requirements.txt cho môi trường runtime.
    # Nếu phát hành package lên PyPI, thêm lại install_requires tối thiểu cho người dùng cuối.
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "fulfillment-dashboard=app:main",
        ],
    },
)
