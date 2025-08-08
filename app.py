"""
🚀 Fulfillment Dashboard - Hệ thống ONE
Dashboard theo dõi tiến độ xác nhận đơn hàng và bàn giao vận chuyển

Author: AI Assistant
Created: 2024
"""

import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Thêm đường dẫn để import các module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.dashboard_components import *
from config.config import *
from utils.helpers import *

# Cấu hình trang
st.set_page_config(
    page_title="Fulfillment Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }

    .success-metric {
        border-left-color: #2ca02c !important;
    }

    .warning-metric {
        border-left-color: #ff7f0e !important;
    }

    .danger-metric {
        border-left-color: #d62728 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    """Main dashboard function"""

    # Header
    st.markdown(
        '<div class="main-header">🚀 Fulfillment Dashboard - Hệ thống ONE</div>',
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.markdown("## 📊 Điều Khiển Dashboard")

        # Refresh button
        if st.button("🔄 Làm mới dữ liệu", use_container_width=True):
            st.rerun()

        st.markdown("---")

        # Thời gian cập nhật
        st.info(f"⏰ Cập nhật lần cuối: {datetime.now().strftime('%H:%M:%S')}")

        # Menu navigation
        menu_options = [
            "📊 Tổng quan",
            "📈 Biểu đồ chi tiết",
            "📋 Bảng dữ liệu",
            "⚙️ Cài đặt",
        ]

        selected_page = st.selectbox("Chọn trang", menu_options)

    # Load data
    try:
        df = load_data(DATA_PATH)
        if df is None:
            st.error("❌ Không thể tải dữ liệu. Vui lòng kiểm tra file dữ liệu.")
            return

        kpis = calculate_kpis(df)

    except Exception as e:
        st.error(f"❌ Lỗi: {e}")
        return

    # Main content based on selected page
    if selected_page == "📊 Tổng quan":
        render_overview_page(df, kpis)
    elif selected_page == "📈 Biểu đồ chi tiết":
        render_charts_page(df)
    elif selected_page == "📋 Bảng dữ liệu":
        render_data_page(df)
    elif selected_page == "⚙️ Cài đặt":
        render_settings_page()


def render_overview_page(df, kpis):
    """Trang tổng quan"""

    # KPI Cards
    render_kpi_section(kpis)

    st.markdown("---")

    # Performance charts
    render_performance_charts(df)

    st.markdown("---")

    # Timeline
    render_timeline_chart(df)

    # Thống kê nhanh
    st.markdown("## 📋 Thống Kê Nhanh")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Mục Tiêu KPI")
        target_data = {
            "KPI": ["Xác nhận đúng hạn", "Giao hàng đúng hạn", "Tỷ lệ hủy"],
            "Mục tiêu": ["≥90%", "≥85%", "≤10%"],
            "Thực tế": [
                f"{kpis['confirmation_rate']:.1f}%",
                f"{kpis['delivery_rate']:.1f}%",
                f"{kpis['cancellation_rate']:.1f}%",
            ],
            "Trạng thái": [
                "✅" if kpis["confirmation_rate"] >= 90 else "❌",
                "✅" if kpis["delivery_rate"] >= 85 else "❌",
                "✅" if kpis["cancellation_rate"] <= 10 else "❌",
            ],
        }
        st.dataframe(
            pd.DataFrame(target_data), hide_index=True, use_container_width=True
        )

    with col2:
        st.markdown("### 💰 Thống Kê Giá Trị")
        value_stats = {
            "Chỉ số": [
                "Tổng giá trị đơn hàng",
                "Giá trị trung bình/đơn",
                "Đơn hàng cao nhất",
                "Đơn hàng thấp nhất",
            ],
            "Giá trị": [
                f"{df['order_value'].sum():,.0f} VND",
                f"{df['order_value'].mean():,.0f} VND",
                f"{df['order_value'].max():,.0f} VND",
                f"{df['order_value'].min():,.0f} VND",
            ],
        }
        st.dataframe(
            pd.DataFrame(value_stats), hide_index=True, use_container_width=True
        )


def render_charts_page(df):
    """Trang biểu đồ chi tiết"""
    st.markdown("## 📈 Phân Tích Chi Tiết")

    # Advanced charts
    col1, col2 = st.columns(2)

    with col1:
        # Biểu đồ hiệu suất theo giờ
        hourly_perf = df.copy()
        hourly_perf["hour"] = hourly_perf["order_date"].dt.hour
        hourly_data = (
            hourly_perf.groupby("hour")
            .agg({"order_id": "count", "is_confirmed_ontime": "mean"})
            .reset_index()
        )

        fig_hourly = px.bar(
            hourly_data,
            x="hour",
            y="order_id",
            title="Đơn hàng theo giờ trong ngày",
            labels={"hour": "Giờ", "order_id": "Số đơn hàng"},
        )
        st.plotly_chart(fig_hourly, use_container_width=True)

    with col2:
        # Biểu đồ heatmap theo ngày trong tuần
        df_copy = df.copy()
        df_copy["weekday"] = df_copy["order_date"].dt.day_name()
        df_copy["hour"] = df_copy["order_date"].dt.hour

        heatmap_data = (
            df_copy.groupby(["weekday", "hour"])["order_id"].count().reset_index()
        )
        heatmap_pivot = heatmap_data.pivot(
            index="weekday", columns="hour", values="order_id"
        ).fillna(0)

        fig_heatmap = px.imshow(
            heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            title="Phân bố đơn hàng theo ngày & giờ",
            color_continuous_scale="viridis",
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # Biểu đồ funnel
    st.markdown("### 🔄 Funnel Analysis")
    funnel_data = {
        "Stage": ["Đơn hàng tạo", "Đã xác nhận", "Đã giao hàng", "Hoàn thành"],
        "Count": [
            len(df),
            len(df[df["status"] != "pending"]),
            len(df[df["status"] == "delivered"]),
            len(df[df["status"] == "delivered"]),
        ],
    }

    fig_funnel = px.funnel(
        pd.DataFrame(funnel_data),
        x="Count",
        y="Stage",
        title="Phễu chuyển đổi đơn hàng",
    )
    st.plotly_chart(fig_funnel, use_container_width=True)


def render_data_page(df):
    """Trang dữ liệu chi tiết"""
    render_detailed_table(df)


def render_settings_page():
    """Trang cài đặt"""
    render_settings_panel()

if __name__ == "__main__":
    main()
