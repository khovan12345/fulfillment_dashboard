import React, { useState, useEffect, useMemo, useCallback } from 'react';
import {
  Package, Users, BarChart3, Calendar, Settings, Bell, Search, Menu, X,
  LogOut, Eye, EyeOff, Shield, Clock, TrendingUp, AlertTriangle,
  CheckCircle, RefreshCw, Filter, Download, ChevronDown, ChevronRight,
  MapPin, Zap, Play, Pause, MoreHorizontal, PieChart, Activity,
  Truck, Inbox, FileText, Star, Target, Coffee, Home, Moon, Sun,
  Map, Route, Layers, Navigation, Warehouse, ShoppingCart, Archive,
  AlertCircle, CheckSquare, ClipboardList, History, Camera, Scan,
  BarChart2, Lightbulb, Gauge, ArrowUpDown, Timer, User, Maximize2,
  Minimize2, Grid3X3, LayoutDashboard, Database, Cpu, Wifi, WifiOff
} from 'lucide-react';

// ==================== MAIN DASHBOARD STRUCTURE ====================
const DashboardMainStructure = () => {
  // Trạng thái chính của hệ thống
  const [activeModule, setActiveModule] = useState('overview');
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('connected');
  const [notifications, setNotifications] = useState([]);
  const [userProfile, setUserProfile] = useState({
    name: 'Trưởng phòng Kho vận',
    role: 'Warehouse Manager',
    avatar: 'TK',
    shift: 'Ca sáng 6:00-14:00'
  });

  // Cấu hình modules chính của hệ thống
  const MODULES_CONFIG = useMemo(() => ({
    overview: {
      id: 'overview',
      title: 'Tổng Quan',
      subtitle: 'Dashboard chính & KPI',
      icon: LayoutDashboard,
      color: 'from-blue-500 to-cyan-500',
      badge: null,
      shortcut: 'Ctrl+1'
    },
    orders: {
      id: 'orders',
      title: 'Quản Lý Đơn Hàng',
      subtitle: 'SLA tracking & workflow',
      icon: Package,
      color: 'from-green-500 to-emerald-500',
      badge: 15, // Số đơn P1 cần xử lý
      shortcut: 'Ctrl+2'
    },
    picking: {
      id: 'picking',
      title: 'Hệ Thống Lấy Hàng',
      subtitle: 'Route optimization & scanning',
      icon: Navigation,
      color: 'from-purple-500 to-violet-500',
      badge: 12, // Route đang active
      shortcut: 'Ctrl+3'
    },
    warehouse: {
      id: 'warehouse',
      title: 'Quản Lý Kho',
      subtitle: 'Layout & inventory mapping',
      icon: Warehouse,
      color: 'from-orange-500 to-red-500',
      badge: null,
      shortcut: 'Ctrl+4'
    },
    analytics: {
      id: 'analytics',
      title: 'Phân Tích & Báo Cáo',
      subtitle: 'Performance insights',
      icon: BarChart3,
      color: 'from-indigo-500 to-purple-500',
      badge: null,
      shortcut: 'Ctrl+5'
    },
    alerts: {
      id: 'alerts',
      title: 'Cảnh Báo & Thông Báo',
      subtitle: 'Real-time monitoring',
      icon: Bell,
      color: 'from-yellow-500 to-orange-500',
      badge: 7, // Số cảnh báo active
      shortcut: 'Ctrl+6'
    },
    staff: {
      id: 'staff',
      title: 'Quản Lý Nhân Sự',
      subtitle: 'Schedule & performance',
      icon: Users,
      color: 'from-teal-500 to-green-500',
      badge: null,
      shortcut: 'Ctrl+7'
    },
    settings: {
      id: 'settings',
      title: 'Cài Đặt Hệ Thống',
      subtitle: 'Configuration & admin',
      icon: Settings,
      color: 'from-gray-500 to-slate-500',
      badge: null,
      shortcut: 'Ctrl+8'
    }
  }), []);

  // Theme configuration
  const themeClasses = useMemo(() => ({
    background: isDarkMode ? 'bg-gray-900' : 'bg-gray-50',
    surface: isDarkMode ? 'bg-gray-800' : 'bg-white',
    surfaceHover: isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50',
    surfaceActive: isDarkMode ? 'bg-gray-700' : 'bg-gray-100',
    border: isDarkMode ? 'border-gray-700' : 'border-gray-200',
    text: {
      primary: isDarkMode ? 'text-white' : 'text-gray-900',
      secondary: isDarkMode ? 'text-gray-300' : 'text-gray-600',
      muted: isDarkMode ? 'text-gray-400' : 'text-gray-500'
    },
    accent: 'from-blue-500 to-purple-600'
  }), [isDarkMode]);

  // Keyboard shortcuts handler
  useEffect(() => {
    const handleKeyboard = (e) => {
      if (e.ctrlKey) {
        const shortcuts = {
          '1': 'overview', '2': 'orders', '3': 'picking', '4': 'warehouse',
          '5': 'analytics', '6': 'alerts', '7': 'staff', '8': 'settings'
        };
        if (shortcuts[e.key]) {
          e.preventDefault();
          setActiveModule(shortcuts[e.key]);
        }
      }
      if (e.key === 'F11') {
        e.preventDefault();
        setIsFullscreen(!isFullscreen);
      }
    };

    document.addEventListener('keydown', handleKeyboard);
    return () => document.removeEventListener('keydown', handleKeyboard);
  }, [isFullscreen]);

  // Mock real-time data simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setConnectionStatus(prev => prev === 'connected' ? 'connected' : 'connected');
      // Simulate notification updates
      if (Math.random() > 0.95) {
        setNotifications(prev => [...prev.slice(-4), {
          id: Date.now(),
          type: Math.random() > 0.7 ? 'warning' : 'info',
          message: 'Đơn hàng mới cần xử lý',
          time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
        }]);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const handleModuleChange = useCallback((moduleId) => {
    setActiveModule(moduleId);
  }, []);

  return (
    <div className={`h-screen flex overflow-hidden transition-colors duration-200 ${themeClasses.background}`}>
      {/* SIDEBAR - Navigation chính */}
      <div className={`${sidebarCollapsed ? 'w-16' : 'w-64'} ${themeClasses.surface} ${themeClasses.border} border-r transition-all duration-300 flex flex-col`}>
        {/* Header sidebar */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            {!sidebarCollapsed && (
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
                  MIA Dashboard
                </h1>
                <p className={`text-xs ${themeClasses.text.muted}`}>SLA Warehouse System</p>
              </div>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className={`p-2 rounded-lg ${themeClasses.surfaceHover} transition-colors`}
            >
              {sidebarCollapsed ? <ChevronRight size={16} /> : <ChevronDown size={16} />}
            </button>
          </div>
        </div>

        {/* Navigation menu */}
        <nav className="flex-1 overflow-y-auto py-4">
          <div className="space-y-1 px-2">
            {Object.values(MODULES_CONFIG).map((module) => (
              <NavItem
                key={module.id}
                module={module}
                isActive={activeModule === module.id}
                isCollapsed={sidebarCollapsed}
                onClick={() => handleModuleChange(module.id)}
                themeClasses={themeClasses}
              />
            ))}
          </div>
        </nav>

        {/* Sidebar footer - User info */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className={`flex items-center ${sidebarCollapsed ? 'justify-center' : 'space-x-3'}`}>
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm">
              {userProfile.avatar}
            </div>
            {!sidebarCollapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{userProfile.name}</p>
                <p className={`text-xs ${themeClasses.text.muted} truncate`}>{userProfile.shift}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* TOP HEADER - Controls & status */}
        <TopHeader
          activeModule={MODULES_CONFIG[activeModule]}
          isDarkMode={isDarkMode}
          isFullscreen={isFullscreen}
          connectionStatus={connectionStatus}
          notifications={notifications}
          themeClasses={themeClasses}
          onThemeToggle={() => setIsDarkMode(!isDarkMode)}
          onFullscreenToggle={() => setIsFullscreen(!isFullscreen)}
        />

        {/* CONTENT AREA - Module content */}
        <main className="flex-1 overflow-hidden">
          <ContentArea
            activeModule={activeModule}
            themeClasses={themeClasses}
          />
        </main>

        {/* BOTTOM STATUS BAR */}
        <StatusBar
          connectionStatus={connectionStatus}
          themeClasses={themeClasses}
        />
      </div>
    </div>
  );
};

// ==================== NAVIGATION ITEM COMPONENT ====================
const NavItem = ({ module, isActive, isCollapsed, onClick, themeClasses }) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center ${isCollapsed ? 'justify-center p-2' : 'px-3 py-2'} rounded-lg transition-all group ${
      isActive
        ? `bg-gradient-to-r ${module.color} text-white shadow-lg`
        : `${themeClasses.surfaceHover} ${themeClasses.text.secondary}`
    }`}
    title={isCollapsed ? `${module.title} (${module.shortcut})` : undefined}
  >
    <div className="relative">
      <module.icon size={20} className={isActive ? 'text-white' : ''} />
      {module.badge && (
        <div className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
          {module.badge > 99 ? '99+' : module.badge}
        </div>
      )}
    </div>

    {!isCollapsed && (
      <div className="ml-3 flex-1 text-left">
        <p className={`text-sm font-medium ${isActive ? 'text-white' : ''}`}>
          {module.title}
        </p>
        <p className={`text-xs ${isActive ? 'text-blue-100' : themeClasses.text.muted}`}>
          {module.subtitle}
        </p>
      </div>
    )}

    {!isCollapsed && (
      <span className={`text-xs ${isActive ? 'text-blue-100' : themeClasses.text.muted}`}>
        {module.shortcut.replace('Ctrl+', '⌘')}
      </span>
    )}
  </button>
);

// ==================== TOP HEADER COMPONENT ====================
const TopHeader = ({
  activeModule, isDarkMode, isFullscreen, connectionStatus,
  notifications, themeClasses, onThemeToggle, onFullscreenToggle
}) => {
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className={`${themeClasses.surface} ${themeClasses.border} border-b px-6 py-3 flex items-center justify-between`}>
      {/* Left section - Module info */}
      <div className="flex items-center space-x-4">
        <div className={`p-2 rounded-lg bg-gradient-to-r ${activeModule.color} bg-opacity-10`}>
          <activeModule.icon size={24} className={`text-blue-600 dark:text-blue-400`} />
        </div>
        <div>
          <h2 className="text-lg font-semibold">{activeModule.title}</h2>
          <p className={`text-sm ${themeClasses.text.muted}`}>
            {activeModule.subtitle} • Cập nhật: {new Date().toLocaleTimeString('vi-VN')}
          </p>
        </div>
      </div>

      {/* Right section - Controls */}
      <div className="flex items-center space-x-2">
        {/* Search */}
        <div className="relative">
          <input
            type="text"
            placeholder="Tìm kiếm..."
            className={`w-64 pl-8 pr-3 py-2 rounded-lg ${themeClasses.surface} ${themeClasses.border} border focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
          />
          <Search size={16} className={`absolute left-2.5 top-3 ${themeClasses.text.muted}`} />
        </div>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className={`p-2 rounded-lg ${themeClasses.surfaceHover} transition-colors relative`}
          >
            <Bell size={20} />
            {notifications.length > 0 && (
              <div className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {notifications.length}
              </div>
            )}
          </button>

          {showNotifications && (
            <div className={`absolute right-0 top-12 w-80 ${themeClasses.surface} ${themeClasses.border} border rounded-lg shadow-lg z-50`}>
              <div className="p-3 border-b border-gray-200 dark:border-gray-700">
                <h3 className="font-semibold">Thông báo</h3>
              </div>
              <div className="max-h-64 overflow-y-auto">
                {notifications.length > 0 ? notifications.map(notif => (
                  <div key={notif.id} className="p-3 border-b border-gray-100 dark:border-gray-800 last:border-0">
                    <p className="text-sm">{notif.message}</p>
                    <p className={`text-xs ${themeClasses.text.muted} mt-1`}>{notif.time}</p>
                  </div>
                )) : (
                  <p className={`p-3 text-sm ${themeClasses.text.muted}`}>Không có thông báo mới</p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Connection status */}
        <div className="flex items-center space-x-1">
          {connectionStatus === 'connected' ?
            <Wifi size={16} className="text-green-500" /> :
            <WifiOff size={16} className="text-red-500" />
          }
          <span className={`text-xs ${connectionStatus === 'connected' ? 'text-green-500' : 'text-red-500'}`}>
            {connectionStatus === 'connected' ? 'Online' : 'Offline'}
          </span>
        </div>

        {/* Theme toggle */}
        <button
          onClick={onThemeToggle}
          className={`p-2 rounded-lg ${themeClasses.surfaceHover} transition-colors`}
        >
          {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>

        {/* Fullscreen toggle */}
        <button
          onClick={onFullscreenToggle}
          className={`p-2 rounded-lg ${themeClasses.surfaceHover} transition-colors`}
        >
          {isFullscreen ? <Minimize2 size={20} /> : <Maximize2 size={20} />}
        </button>

        {/* Settings menu */}
        <button className={`p-2 rounded-lg ${themeClasses.surfaceHover} transition-colors`}>
          <MoreHorizontal size={20} />
        </button>
      </div>
    </header>
  );
};

// ==================== CONTENT AREA COMPONENT ====================
const ContentArea = ({ activeModule, themeClasses }) => {
  // Mock content cho từng module
  const renderModuleContent = () => {
    switch (activeModule) {
      case 'overview':
        return <OverviewContent themeClasses={themeClasses} />;
      case 'orders':
        return <OrdersContent themeClasses={themeClasses} />;
      case 'picking':
        return <PickingContent themeClasses={themeClasses} />;
      case 'warehouse':
        return <WarehouseContent themeClasses={themeClasses} />;
      case 'analytics':
        return <AnalyticsContent themeClasses={themeClasses} />;
      case 'alerts':
        return <AlertsContent themeClasses={themeClasses} />;
      case 'staff':
        return <StaffContent themeClasses={themeClasses} />;
      case 'settings':
        return <SettingsContent themeClasses={themeClasses} />;
      default:
        return <OverviewContent themeClasses={themeClasses} />;
    }
  };

  return (
    <div className="h-full overflow-auto p-6">
      {renderModuleContent()}
    </div>
  );
};

// ==================== STATUS BAR COMPONENT ====================
const StatusBar = ({ connectionStatus, themeClasses }) => (
  <div className={`${themeClasses.surface} ${themeClasses.border} border-t px-6 py-2 flex items-center justify-between text-xs ${themeClasses.text.muted}`}>
    <div className="flex items-center space-x-4">
      <span>Dashboard SLA Kho Vận v2.0</span>
      <span>•</span>
      <span>Phiên bản: 01/06/2025</span>
      <span>•</span>
      <span className={connectionStatus === 'connected' ? 'text-green-500' : 'text-red-500'}>
        {connectionStatus === 'connected' ? 'Kết nối ổn định' : 'Mất kết nối'}
      </span>
    </div>

    <div className="flex items-center space-x-4">
      <span>Server: Asia-Southeast-1</span>
      <span>•</span>
      <span>Latency: 12ms</span>
      <span>•</span>
      <span>Memory: 67%</span>
    </div>
  </div>
);

// ==================== MODULE CONTENT COMPONENTS ====================
const OverviewContent = ({ themeClasses }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* KPI Cards */}
      {[
        { label: 'Tổng đơn hôm nay', value: '1,247', change: '+12%', color: 'blue' },
        { label: 'SLA Compliance', value: '94.2%', change: '+2.1%', color: 'green' },
        { label: 'Đơn P1 chờ xử lý', value: '15', change: '-8', color: 'red' },
        { label: 'Hiệu suất trung bình', value: '87%', change: '+5%', color: 'purple' }
      ].map((kpi, index) => (
        <div key={index} className={`p-4 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
          <p className={`text-sm ${themeClasses.text.muted} mb-1`}>{kpi.label}</p>
          <p className="text-2xl font-bold mb-1">{kpi.value}</p>
          <p className={`text-xs ${kpi.change.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
            {kpi.change} từ hôm qua
          </p>
        </div>
      ))}
    </div>

    <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
      <h3 className="text-lg font-semibold mb-4">🏗️ Đây là khu vực hiển thị tổng quan</h3>
      <p className={themeClasses.text.muted}>
        Nội dung chi tiết của từng module sẽ được phát triển trong các giai đoạn tiếp theo.
        Hiện tại chúng ta đang tập trung vào việc xây dựng cấu trúc chính của dashboard.
      </p>
    </div>
  </div>
);

const OrdersContent = ({ themeClasses }) => (
  <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
    <h3 className="text-lg font-semibold mb-4">📦 Module Quản Lý Đơn Hàng</h3>
    <p className={themeClasses.text.muted}>
      Module này sẽ chứa: SLA tracking, workflow automation, order management, bulk operations...
    </p>
  </div>
);

const PickingContent = ({ themeClasses }) => (
  <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
    <h3 className="text-lg font-semibold mb-4">🎯 Module Hệ Thống Lấy Hàng</h3>
    <p className={themeClasses.text.muted}>
      Module này sẽ chứa: Route optimization, barcode scanning, voice picking, error prevention...
    </p>
  </div>
);

const WarehouseContent = ({ themeClasses }) => (
  <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
    <h3 className="text-lg font-semibold mb-4">🏭 Module Quản Lý Kho</h3>
    <p className={themeClasses.text.muted}>
      Module này sẽ chứa: 3D warehouse map, inventory management, space optimization...
    </p>
  </div>
);

const AnalyticsContent = ({ themeClasses }) => (
  <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
    <h3 className="text-lg font-semibold mb-4">📊 Module Phân Tích & Báo Cáo</h3>
    <p className={themeClasses.text.muted}>
      Module này sẽ chứa: Interactive charts, predictive analytics, custom dashboards...
    </p>
  </div>
);

const AlertsContent = ({ themeClasses }) => (
  <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
    <h3 className="text-lg font-semibold mb-4">🚨 Module Cảnh Báo & Thông Báo</h3>
    <p className={themeClasses.text.muted}>
      Module này sẽ chứa: Real-time alerts, escalation rules, multi-channel notifications...
    </p>
  </div>
);

const StaffContent = ({ themeClasses }) => (
  <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
    <h3 className="text-lg font-semibold mb-4">👥 Module Quản Lý Nhân Sự</h3>
    <p className={themeClasses.text.muted}>
      Module này sẽ chứa: Schedule management, performance tracking, skill matrix...
    </p>
  </div>
);

const SettingsContent = ({ themeClasses }) => (
  <div className={`p-6 rounded-xl ${themeClasses.surface} ${themeClasses.border} border`}>
    <h3 className="text-lg font-semibold mb-4">⚙️ Module Cài Đặt Hệ Thống</h3>
    <p className={themeClasses.text.muted}>
      Module này sẽ chứa: System configuration, user management, permissions, integrations...
    </p>
  </div>
);

export default DashboardMainStructure;
