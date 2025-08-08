"""
Utility functions for Fulfillment Dashboard
Các hàm tiện ích cho Dashboard
"""

import pandas as pd
import plotly.express as px
import streamlit as st


def load_data(file_path):
    """Tải dữ liệu từ file CSV"""
    try:
        df = pd.read_csv(file_path)
        df["order_date"] = pd.to_datetime(df["order_date"])
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None


def calculate_kpis(df):
    """Tính toán các KPIs chính"""
    if df is None or df.empty:
        return {}

    total_orders = len(df)
    confirmed_ontime = df["is_confirmed_ontime"].sum()
    delivered_ontime = df["is_delivered_ontime"].sum()
    cancelled_orders = len(df[df["status"] == "cancelled"])
    pending_orders = len(df[df["status"] == "pending"])

    # Tính tỷ lệ phần trăm
    confirmation_rate = (
        (confirmed_ontime / total_orders * 100) if total_orders > 0 else 0
    )
    delivery_rate = (delivered_ontime / total_orders * 100) if total_orders > 0 else 0
    cancellation_rate = (
        (cancelled_orders / total_orders * 100) if total_orders > 0 else 0
    )

    return {
        "total_orders": total_orders,
        "confirmation_rate": confirmation_rate,
        "delivery_rate": delivery_rate,
        "cancelled_orders": cancelled_orders,
        "pending_orders": pending_orders,
        "cancellation_rate": cancellation_rate,
        "avg_order_value": df["order_value"].mean() if not df.empty else 0,
    }


def create_kpi_card(title, value, delta=None, format_type="number"):
    """Tạo KPI card với Streamlit metrics"""
    if format_type == "percentage":
        return f"{value:.1f}%"
    elif format_type == "currency":
        return f"{value:,.0f} VND"
    else:
        return f"{value:,.0f}"


def create_trend_chart(df, date_col, value_col, title):
    """Tạo biểu đồ xu hướng theo thời gian"""
    daily_data = df.groupby(df[date_col].dt.date)[value_col].sum().reset_index()

    fig = px.line(daily_data, x=date_col, y=value_col, title=title, markers=True)

    fig.update_layout(xaxis_title="Ngày", yaxis_title="Số lượng", hovermode="x")

    return fig


def create_status_pie_chart(df):
    """Tạo biểu đồ tròn trạng thái đơn hàng"""
    status_counts = df["status"].value_counts()

    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Phân bố trạng thái đơn hàng",
    )

    return fig


def create_region_bar_chart(df):
    """Tạo biểu đồ cột theo vùng"""
    region_data = (
        df.groupby("region")
        .agg(
            {
                "order_id": "count",
                "order_value": "sum",
                "is_confirmed_ontime": "mean",
                "is_delivered_ontime": "mean",
            }
        )
        .reset_index()
    )

    region_data.columns = [
        "Vùng",
        "Số đơn",
        "Tổng giá trị",
        "Tỷ lệ xác nhận",
        "Tỷ lệ giao hàng",
    ]

    fig = px.bar(
        region_data, x="Vùng", y="Số đơn", title="Đơn hàng theo vùng", text="Số đơn"
    )

    fig.update_traces(texttemplate="%{text}", textposition="outside")

    return fig


def format_number(num):
    """Format số với dấu phẩy"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return f"{num:.0f}"
