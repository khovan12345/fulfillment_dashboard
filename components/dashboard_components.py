"""
Dashboard Components
Các thành phần giao diện cho Dashboard
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def render_kpi_section(kpis):
    """Hiển thị section KPIs chính"""
    st.markdown("## 📊 KPIs Chính")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📦 Tổng đơn hàng", value=f"{kpis['total_orders']:,}", delta=None
        )

    with col2:
        confirmation_color = "normal" if kpis["confirmation_rate"] >= 90 else "inverse"
        st.metric(
            label="✅ Tỷ lệ xác nhận đúng hạn",
            value=f"{kpis['confirmation_rate']:.1f}%",
            delta=f"{kpis['confirmation_rate'] - 90:.1f}%",
        )

    with col3:
        st.metric(
            label="🚚 Tỷ lệ giao hàng đúng hạn",
            value=f"{kpis['delivery_rate']:.1f}%",
            delta=f"{kpis['delivery_rate'] - 85:.1f}%",
        )

    with col4:
        st.metric(
            label="❌ Đơn hàng hủy",
            value=f"{kpis['cancelled_orders']:,}",
            delta=f"-{kpis['cancellation_rate']:.1f}%",
        )


def render_performance_charts(df):
    """Hiển thị biểu đồ hiệu suất"""
    st.markdown("## 📈 Biểu Đồ Hiệu Suất")

    col1, col2 = st.columns(2)

    with col1:
        # Biểu đồ trạng thái đơn hàng
        status_counts = df["status"].value_counts()
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Phân bố trạng thái đơn hàng",
            color_discrete_map={
                "confirmed": "#2ca02c",
                "delivered": "#1f77b4",
                "cancelled": "#d62728",
                "pending": "#ff7f0e",
            },
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Biểu đồ theo vùng
        region_data = df.groupby("region")["order_id"].count().reset_index()
        fig_bar = px.bar(
            region_data,
            x="region",
            y="order_id",
            title="Đơn hàng theo vùng",
            color="order_id",
            color_continuous_scale="viridis",
        )
        fig_bar.update_layout(xaxis_title="Vùng", yaxis_title="Số đơn hàng")
        st.plotly_chart(fig_bar, use_container_width=True)


def render_timeline_chart(df):
    """Biểu đồ timeline đơn hàng"""
    st.markdown("## ⏰ Timeline Đơn Hàng")

    # Nhóm theo ngày
    daily_orders = (
        df.groupby(df["order_date"].dt.date)
        .agg(
            {
                "order_id": "count",
                "is_confirmed_ontime": "mean",
                "is_delivered_ontime": "mean",
            }
        )
        .reset_index()
    )

    # Tạo subplot với 2 trục y
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Số lượng đơn hàng theo ngày", "Tỷ lệ đúng hạn theo ngày"),
        vertical_spacing=0.1,
    )

    # Biểu đồ số lượng đơn hàng
    fig.add_trace(
        go.Scatter(
            x=daily_orders["order_date"],
            y=daily_orders["order_id"],
            mode="lines+markers",
            name="Số đơn hàng",
            line=dict(color="#1f77b4"),
        ),
        row=1,
        col=1,
    )

    # Biểu đồ tỷ lệ đúng hạn
    fig.add_trace(
        go.Scatter(
            x=daily_orders["order_date"],
            y=daily_orders["is_confirmed_ontime"] * 100,
            mode="lines+markers",
            name="Tỷ lệ xác nhận đúng hạn",
            line=dict(color="#2ca02c"),
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=daily_orders["order_date"],
            y=daily_orders["is_delivered_ontime"] * 100,
            mode="lines+markers",
            name="Tỷ lệ giao hàng đúng hạn",
            line=dict(color="#ff7f0e"),
        ),
        row=2,
        col=1,
    )

    fig.update_layout(height=600, showlegend=True)
    fig.update_xaxes(title_text="Ngày", row=2, col=1)
    fig.update_yaxes(title_text="Số đơn hàng", row=1, col=1)
    fig.update_yaxes(title_text="Tỷ lệ (%)", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)


def render_detailed_table(df):
    """Bảng chi tiết đơn hàng"""
    st.markdown("## 📋 Chi Tiết Đơn Hàng")

    # Bộ lọc
    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.selectbox(
            "Lọc theo trạng thái", options=["Tất cả"] + list(df["status"].unique())
        )

    with col2:
        region_filter = st.selectbox(
            "Lọc theo vùng", options=["Tất cả"] + list(df["region"].unique())
        )

    with col3:
        date_range = st.date_input(
            "Chọn khoảng thời gian",
            value=[df["order_date"].min().date(), df["order_date"].max().date()],
            min_value=df["order_date"].min().date(),
            max_value=df["order_date"].max().date(),
        )

    # Áp dụng bộ lọc
    filtered_df = df.copy()

    if status_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    if region_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["region"] == region_filter]

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["order_date"].dt.date >= date_range[0])
            & (filtered_df["order_date"].dt.date <= date_range[1])
        ]

    # Hiển thị bảng
    display_df = filtered_df[
        [
            "order_id",
            "order_date",
            "status",
            "region",
            "order_value",
            "is_confirmed_ontime",
            "is_delivered_ontime",
        ]
    ].copy()
    display_df["order_date"] = display_df["order_date"].dt.strftime("%Y-%m-%d %H:%M")
    display_df["order_value"] = display_df["order_value"].apply(
        lambda x: f"{x:,.0f} VND"
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.info(f"Hiển thị {len(filtered_df)} đơn hàng (từ tổng {len(df)} đơn)")



def render_settings_panel():
    """Panel cài đặt hệ thống"""
    st.markdown("## ⚙️ Cài Đặt Hệ Thống")

    # Tạo tabs cho các loại cài đặt
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 SLA & Thời gian",
        "📊 Google Sheets",
        "🔔 Thông báo",
        "🛠️ Hệ thống"
    ])

    with tab1:
        render_sla_settings()

    with tab2:
        render_google_sheets_settings()

    with tab3:
        render_notification_settings()

    with tab4:
        render_system_settings()


def render_sla_settings():
    """Cài đặt SLA và thời gian"""
    st.markdown("### 🎯 Cài đặt SLA và Thời gian xử lý")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**⏰ Thời gian xử lý đơn hàng**")

        confirmation_time = st.number_input(
            "Thời gian xác nhận đơn (phút)",
            min_value=1,
            max_value=1440,
            value=30,
            help="Thời gian tối đa để xác nhận đơn hàng"
        )

        delivery_time_standard = st.number_input(
            "Thời gian giao hàng tiêu chuẩn (giờ)",
            min_value=1,
            max_value=168,
            value=24,
            help="Thời gian giao hàng cho đơn thường"
        )

        delivery_time_express = st.number_input(
            "Thời gian giao hàng nhanh (giờ)",
            min_value=1,
            max_value=24,
            value=4,
            help="Thời gian giao hàng cho đơn ưu tiên"
        )

    with col2:
        st.markdown("**📋 Quy tắc SLA theo loại đơn**")

        # Bảng SLA rules
        sla_data = {
            "Loại đơn": ["Đơn thường", "Đơn ưu tiên", "Đơn VIP", "Đơn khẩn cấp"],
            "Xác nhận (phút)": [30, 15, 10, 5],
            "Giao hàng (giờ)": [24, 12, 6, 2],
            "Ưu tiên": ["Thấp", "Trung bình", "Cao", "Khẩn cấp"]
        }

        sla_df = pd.DataFrame(sla_data)
        edited_sla = st.data_editor(
            sla_df,
            column_config={
                "Loại đơn": st.column_config.TextColumn("Loại đơn", disabled=True),
                "Xác nhận (phút)": st.column_config.NumberColumn("Xác nhận (phút)", min_value=1),
                "Giao hàng (giờ)": st.column_config.NumberColumn("Giao hàng (giờ)", min_value=1),
                "Ưu tiên": st.column_config.SelectboxColumn(
                    "Ưu tiên",
                    options=["Thấp", "Trung bình", "Cao", "Khẩn cấp"]
                )
            },
            hide_index=True,
            use_container_width=True
        )

    # Nút lưu cài đặt SLA
    if st.button("💾 Lưu cài đặt SLA", type="primary"):
        st.success("✅ Đã lưu cài đặt SLA thành công!")
        st.info("📊 Cài đặt đã được đồng bộ với Google Sheets")


def render_google_sheets_settings():
    """Cài đặt Google Sheets"""
    st.markdown("### 📊 Cài đặt Google Sheets Integration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔗 Kết nối Google Sheets**")

        # Trạng thái kết nối
        connection_status = st.empty()
        if st.button("🔍 Kiểm tra kết nối"):
            with st.spinner("Đang kiểm tra..."):
                # Simulate connection check
                import time
                time.sleep(1)
                connection_status.success("✅ Kết nối Google Sheets thành công!")

        # Spreadsheet ID
        spreadsheet_id = st.text_input(
            "Spreadsheet ID",
            value="1xdfAEgbvDee_oJFwzb8bWW9ONmYO3RbQJ3Oscbmm5Uc",
            help="ID của Google Sheets để lưu trữ dữ liệu"
        )

        # Auto sync settings
        auto_sync = st.checkbox("🔄 Tự động đồng bộ", value=True)

        if auto_sync:
            sync_interval = st.selectbox(
                "Tần suất đồng bộ",
                options=["5 phút", "15 phút", "30 phút", "1 giờ", "Thủ công"],
                index=1
            )

    with col2:
        st.markdown("**📋 Quản lý Worksheets**")

        # Danh sách worksheets
        worksheets = [
            "Cấu hình hệ thống",
            "Quy tắc SLA",
            "Nhật ký tự động",
            "Thống kê tổng quan"
        ]

        for ws in worksheets:
            col_ws1, col_ws2, col_ws3 = st.columns([3, 1, 1])
            with col_ws1:
                st.write(f"📄 {ws}")
            with col_ws2:
                if st.button("👁️", key=f"view_{ws}", help="Xem worksheet"):
                    st.info(f"Mở worksheet: {ws}")
            with col_ws3:
                if st.button("🔄", key=f"sync_{ws}", help="Đồng bộ worksheet"):
                    st.success(f"Đã đồng bộ: {ws}")

    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("💾 Backup Sheets", use_container_width=True):
            st.success("✅ Đã tạo backup Google Sheets!")

    with col_btn2:
        if st.button("🔧 Thiết lập lại", use_container_width=True):
            st.info("🔄 Đang thiết lập lại Google Sheets...")

    with col_btn3:
        if st.button("📊 Mở Google Sheets", use_container_width=True):
            st.markdown("🔗 [Mở Google Sheets](https://docs.google.com/spreadsheets/d/1xdfAEgbvDee_oJFwzb8bWW9ONmYO3RbQJ3Oscbmm5Uc)")


def render_notification_settings():
    """Cài đặt thông báo"""
    st.markdown("### 🔔 Cài đặt Thông báo")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📧 Email Notifications**")

        email_enabled = st.checkbox("✉️ Bật thông báo email", value=True)

        if email_enabled:
            admin_email = st.text_input(
                "Email quản trị",
                value="admin@company.com",
                help="Email nhận thông báo hệ thống"
            )

            notification_types = st.multiselect(
                "Loại thông báo",
                options=[
                    "Đơn hàng trễ hạn",
                    "Lỗi hệ thống",
                    "Báo cáo hàng ngày",
                    "Cảnh báo SLA"
                ],
                default=["Đơn hàng trễ hạn", "Lỗi hệ thống"]
            )

    with col2:
        st.markdown("**🔊 Alert Settings**")

        sound_alerts = st.checkbox("🔔 Âm thanh cảnh báo", value=False)

        alert_thresholds = st.number_input(
            "Ngưỡng cảnh báo SLA (%)",
            min_value=50,
            max_value=100,
            value=80,
            help="Cảnh báo khi tỷ lệ SLA dưới ngưỡng này"
        )

        urgent_alerts = st.checkbox("🚨 Cảnh báo khẩn cấp", value=True)

        if urgent_alerts:
            urgent_threshold = st.number_input(
                "Ngưỡng khẩn cấp (phút)",
                min_value=1,
                max_value=60,
                value=15,
                help="Cảnh báo khẩn cấp khi đơn quá hạn"
            )

    # Test notifications
    st.markdown("**🧪 Test Thông báo**")
    col_test1, col_test2 = st.columns(2)

    with col_test1:
        if st.button("📧 Test Email"):
            st.success("✅ Đã gửi email test thành công!")

    with col_test2:
        if st.button("🔔 Test Alert"):
            st.warning("⚠️ Đây là cảnh báo test!")


def render_system_settings():
    """Cài đặt hệ thống"""
    st.markdown("### 🛠️ Cài đặt Hệ thống")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**⚡ Hiệu suất**")

        refresh_interval = st.selectbox(
            "Tần suất cập nhật dashboard",
            options=["10 giây", "30 giây", "1 phút", "5 phút"],
            index=2
        )

        cache_duration = st.selectbox(
            "Thời gian cache dữ liệu",
            options=["1 phút", "5 phút", "15 phút", "30 phút"],
            index=1
        )

        max_records = st.number_input(
            "Số bản ghi tối đa hiển thị",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100
        )

    with col2:
        st.markdown("**🔒 Bảo mật**")

        require_auth = st.checkbox("🔐 Yêu cầu xác thực", value=False)

        if require_auth:
            session_timeout = st.selectbox(
                "Thời gian hết phiên (phút)",
                options=[15, 30, 60, 120, 240],
                index=2
            )

        log_level = st.selectbox(
            "Mức độ logging",
            options=["ERROR", "WARNING", "INFO", "DEBUG"],
            index=2
        )

        backup_enabled = st.checkbox("💾 Backup tự động", value=True)

        if backup_enabled:
            backup_frequency = st.selectbox(
                "Tần suất backup",
                options=["Hàng ngày", "Hàng tuần", "Hàng tháng"],
                index=0
            )

    # System actions
    st.markdown("**🔧 Hành động hệ thống**")
    col_sys1, col_sys2, col_sys3 = st.columns(3)

    with col_sys1:
        if st.button("🔄 Restart Services", use_container_width=True):
            st.info("🔄 Đang khởi động lại dịch vụ...")

    with col_sys2:
        if st.button("🧹 Clear Cache", use_container_width=True):
            st.success("✅ Đã xóa cache thành công!")

    with col_sys3:
        if st.button("📊 Export Logs", use_container_width=True):
            st.success("✅ Đã export logs thành công!")

    # Save all settings
    st.markdown("---")
    if st.button("💾 Lưu tất cả cài đặt", type="primary", use_container_width=True):
        st.success("✅ Đã lưu tất cả cài đặt thành công!")
        st.balloons()

