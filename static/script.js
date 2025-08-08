/**
 * 🚀 TGA Enterprise Dashboard JavaScript - Phiên bản Việt hóa
 * Nâng cấp tương tác và hiệu ứng cho Streamlit Dashboard
 */

// 🌟 Global configuration
const TGA_Config = {
    notifications: {
        duration: 5000,
        position: 'top-right'
    },
    animations: {
        duration: 300,
        easing: 'ease'
    },
    colors: {
        primary: '#2563eb',
        success: '#16a34a',
        warning: '#d97706',
        danger: '#dc2626',
        info: '#0891b2'
    }
};

// 🔔 Advanced Notification System
class TGANotification {
    constructor() {
        this.container = this.createContainer();
        this.notifications = [];
    }

    createContainer() {
        let container = document.getElementById('tga-notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'tga-notification-container';
            container.className = 'toast-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
                pointer-events: none;
            `;
            document.body.appendChild(container);
        }
        return container;
    }

    show(type, title, message, duration = TGA_Config.notifications.duration) {
        const notification = this.createNotification(type, title, message);
        
        notification.style.pointerEvents = 'auto';
        this.container.appendChild(notification);
        this.notifications.push(notification);

        // Animation in
        requestAnimationFrame(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        });

        // Auto remove
        setTimeout(() => {
            this.remove(notification);
        }, duration);

        // Click to dismiss
        notification.addEventListener('click', () => {
            this.remove(notification);
        });

        return notification;
    }

    createNotification(type, title, message) {
        const notification = document.createElement('div');
        notification.className = `toast ${type}`;
        
        const icons = {
            success: '✅',
            error: '❌', 
            warning: '⚠️',
            info: 'ℹ️'
        };

        notification.innerHTML = `
            <div style="display: flex; align-items: center; width: 100%;">
                <div style="font-size: 1.2rem; margin-right: 1rem;">
                    ${icons[type] || '📢'}
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; margin-bottom: 0.25rem; color: #1e293b;">
                        ${title}
                    </div>
                    <div style="font-size: 0.9rem; color: #64748b;">
                        ${message}
                    </div>
                </div>
                <div style="margin-left: 1rem; cursor: pointer; opacity: 0.6; font-size: 1.2rem;">
                    ×
                </div>
            </div>
        `;

        notification.style.cssText = `
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid ${TGA_Config.colors[type] || TGA_Config.colors.info};
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s ease;
            cursor: pointer;
        `;

        return notification;
    }

    remove(notification) {
        if (notification && notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
                const index = this.notifications.indexOf(notification);
                if (index > -1) {
                    this.notifications.splice(index, 1);
                }
            }, 300);
        }
    }

    // Shorthand methods
    success(title, message) { return this.show('success', title, message); }
    error(title, message) { return this.show('error', title, message); }
    warning(title, message) { return this.show('warning', title, message); }
    info(title, message) { return this.show('info', title, message); }
}

// 🚀 Loading Manager
class TGALoader {
    constructor() {
        this.overlay = this.createOverlay();
        this.isVisible = false;
    }

    createOverlay() {
        let overlay = document.getElementById('tga-loading-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'tga-loading-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(5px);
                z-index: 9998;
                display: none;
                justify-content: center;
                align-items: center;
            `;

            const spinner = document.createElement('div');
            spinner.className = 'spinner';
            spinner.style.cssText = `
                width: 60px;
                height: 60px;
                border: 6px solid #f3f3f3;
                border-top: 6px solid ${TGA_Config.colors.primary};
                border-radius: 50%;
                animation: spin 1s linear infinite;
            `;

            overlay.appendChild(spinner);
            document.body.appendChild(overlay);
        }
        return overlay;
    }

    show(message = 'Đang tải...') {
        if (!this.isVisible) {
            this.overlay.style.display = 'flex';
            this.isVisible = true;
            
            // Add loading message if provided
            let messageEl = this.overlay.querySelector('.loading-message');
            if (message && !messageEl) {
                messageEl = document.createElement('div');
                messageEl.className = 'loading-message';
                messageEl.style.cssText = `
                    color: white;
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-top: 2rem;
                    text-align: center;
                `;
                this.overlay.appendChild(messageEl);
            }
            if (messageEl) {
                messageEl.textContent = message;
            }
        }
    }

    hide() {
        if (this.isVisible) {
            this.overlay.style.display = 'none';
            this.isVisible = false;
        }
    }
}

// 🎨 Animation Utilities
class TGAAnimations {
    static fadeIn(element, duration = TGA_Config.animations.duration) {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ${TGA_Config.animations.easing}`;
        
        requestAnimationFrame(() => {
            element.style.opacity = '1';
        });
    }

    static slideUp(element, duration = TGA_Config.animations.duration) {
        element.style.transform = 'translateY(20px)';
        element.style.opacity = '0';
        element.style.transition = `all ${duration}ms ${TGA_Config.animations.easing}`;
        
        requestAnimationFrame(() => {
            element.style.transform = 'translateY(0)';
            element.style.opacity = '1';
        });
    }

    static bounce(element) {
        element.style.animation = 'bounce 0.6s ease';
        setTimeout(() => {
            element.style.animation = '';
        }, 600);
    }

    static pulse(element) {
        element.style.animation = 'pulse 2s infinite';
    }

    static shake(element) {
        element.style.animation = 'shake 0.5s ease';
        setTimeout(() => {
            element.style.animation = '';
        }, 500);
    }
}

// 📊 Chart Enhancement Utilities
class TGAChartUtils {
    static enhanceMetrics() {
        // Add hover effects to metric cards
        const metrics = document.querySelectorAll('[data-testid="metric-container"]');
        metrics.forEach((metric, index) => {
            metric.classList.add('metric-container');
            
            // Add different themes based on index
            const themes = ['primary', 'success', 'warning', 'info'];
            metric.classList.add(themes[index % themes.length]);

            // Add icon based on content
            const label = metric.querySelector('label');
            if (label) {
                const text = label.textContent.toLowerCase();
                let icon = '📊';
                
                if (text.includes('đơn') || text.includes('order')) icon = '📦';
                if (text.includes('hoàn thành') || text.includes('complete')) icon = '✅';
                if (text.includes('doanh thu') || text.includes('revenue')) icon = '💰';
                if (text.includes('chờ') || text.includes('pending')) icon = '⏳';
                
                label.innerHTML = `${icon} ${label.textContent}`;
            }
        });
    }

    static addChartToolbar(container, chartId) {
        const toolbar = document.createElement('div');
        toolbar.className = 'chart-toolbar';
        toolbar.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 10px;
        `;

        toolbar.innerHTML = `
            <h3 class="chart-title" style="margin: 0; color: #1e293b; font-size: 1.25rem; font-weight: 600;">
                📈 Biểu đồ phân tích
            </h3>
            <div class="chart-controls" style="display: flex; gap: 0.5rem;">
                <button class="control-btn active" data-period="7" style="padding: 0.5rem 1rem; border: 1px solid #e2e8f0; background: #2563eb; color: white; border-radius: 8px; font-size: 0.85rem; cursor: pointer;">
                    7 ngày
                </button>
                <button class="control-btn" data-period="30" style="padding: 0.5rem 1rem; border: 1px solid #e2e8f0; background: white; color: #64748b; border-radius: 8px; font-size: 0.85rem; cursor: pointer;">
                    30 ngày
                </button>
                <button class="control-btn" data-period="90" style="padding: 0.5rem 1rem; border: 1px solid #e2e8f0; background: white; color: #64748b; border-radius: 8px; font-size: 0.85rem; cursor: pointer;">
                    90 ngày
                </button>
            </div>
        `;

        container.insertBefore(toolbar, container.firstChild);

        // Add click handlers
        toolbar.querySelectorAll('.control-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                toolbar.querySelectorAll('.control-btn').forEach(b => {
                    b.style.background = 'white';
                    b.style.color = '#64748b';
                    b.classList.remove('active');
                });
                btn.style.background = '#2563eb';
                btn.style.color = 'white';
                btn.classList.add('active');
                
                // Trigger chart update
                const period = btn.getAttribute('data-period');
                TGA.notifications.info('Cập nhật biểu đồ', `Đang tải dữ liệu ${period} ngày...`);
            });
        });
    }
}

// 🛠️ Utility Functions
class TGAUtils {
    static formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(amount);
    }

    static formatDate(date) {
        return new Intl.DateTimeFormat('vi-VN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// 🎯 Main TGA Dashboard Class
class TGADashboard {
    constructor() {
        this.notifications = new TGANotification();
        this.loader = new TGALoader();
        this.animations = TGAAnimations;
        this.chartUtils = TGAChartUtils;
        this.utils = TGAUtils;
        
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeEnhancements());
        } else {
            this.initializeEnhancements();
        }

        // Add CSS animations
        this.addAnimationCSS();
    }

    initializeEnhancements() {
        // Enhance metrics
        this.chartUtils.enhanceMetrics();
        
        // Add chart toolbars
        const chartContainers = document.querySelectorAll('.js-plotly-plot');
        chartContainers.forEach((container, index) => {
            if (!container.querySelector('.chart-toolbar')) {
                this.chartUtils.addChartToolbar(container.parentElement, `chart-${index}`);
            }
        });

        // Add loading CSS
        this.addLoadingCSS();
        
        // Animate page load
        this.animatePageLoad();
        
        // Show welcome notification
        setTimeout(() => {
            this.notifications.success(
                '🎉 Chào mừng đến với TGA Dashboard!',
                'Hệ thống đã được nâng cấp với giao diện mới'
            );
        }, 1000);
    }

    addAnimationCSS() {
        const animationCSS = `
            <style id="tga-animations">
                @keyframes bounce {
                    0%, 20%, 53%, 80%, to { transform: translate3d(0,0,0); }
                    40%, 43% { transform: translate3d(0,-30px,0); }
                    70% { transform: translate3d(0,-15px,0); }
                    90% { transform: translate3d(0,-4px,0); }
                }
                
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
                
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
                    20%, 40%, 60%, 80% { transform: translateX(10px); }
                }
                
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .fade-in { animation: fadeIn 0.5s ease; }
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                
                .slide-up { animation: slideUp 0.5s ease; }
                @keyframes slideUp {
                    from { transform: translateY(20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
            </style>
        `;
        
        if (!document.getElementById('tga-animations')) {
            document.head.insertAdjacentHTML('beforeend', animationCSS);
        }
    }

    addLoadingCSS() {
        const loadingCSS = `
            <style id="tga-loading-styles">
                .loading-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background: rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(5px);
                    z-index: 9998;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                }
                
                .spinner {
                    width: 60px;
                    height: 60px;
                    border: 6px solid #f3f3f3;
                    border-top: 6px solid #2563eb;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
            </style>
        `;
        
        if (!document.getElementById('tga-loading-styles')) {
            document.head.insertAdjacentHTML('beforeend', loadingCSS);
        }
    }

    animatePageLoad() {
        // Animate elements as they come into view
        const elements = document.querySelectorAll('.metric-container, .js-plotly-plot, [data-testid="stDataFrame"]');
        elements.forEach((el, index) => {
            setTimeout(() => {
                this.animations.slideUp(el, 600);
            }, index * 100);
        });
    }

    // Public API methods
    showSuccess(title, message) {
        return this.notifications.success(title, message);
    }

    showError(title, message) {
        return this.notifications.error(title, message);
    }

    showWarning(title, message) {
        return this.notifications.warning(title, message);
    }

    showInfo(title, message) {
        return this.notifications.info(title, message);
    }

    showLoader(message) {
        this.loader.show(message);
    }

    hideLoader() {
        this.loader.hide();
    }
}

// 🚀 Initialize TGA Dashboard globally
window.TGA = new TGADashboard();

// 🔄 Auto-refresh enhancements
let refreshInterval;
function startAutoRefresh() {
    refreshInterval = setInterval(() => {
        TGA.chartUtils.enhanceMetrics();
        
        // Re-add chart toolbars if needed
        const chartContainers = document.querySelectorAll('.js-plotly-plot');
        chartContainers.forEach((container, index) => {
            if (!container.parentElement.querySelector('.chart-toolbar')) {
                TGA.chartUtils.addChartToolbar(container.parentElement, `chart-${index}`);
            }
        });
    }, 2000);
}

// Start auto-refresh after page load
setTimeout(startAutoRefresh, 3000);

// 🎉 Export for use in Streamlit
window.TGANotifications = {
    success: (title, message) => TGA.showSuccess(title, message),
    error: (title, message) => TGA.showError(title, message),
    warning: (title, message) => TGA.showWarning(title, message),
    info: (title, message) => TGA.showInfo(title, message),
    showLoader: (message) => TGA.showLoader(message),
    hideLoader: () => TGA.hideLoader()
};

console.log('🚀 TGA Enterprise Dashboard JavaScript đã được tải thành công!');
