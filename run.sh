#!/bin/bash

# ===================================
# MIA Fulfillment Dashboard v2.0 - Universal Launcher
# Thay thế tất cả scripts: run.sh, setup.sh, quick_start.sh
# Tối ưu hóa và thống nhất hệ thống
# ===================================

set -e  # Exit on error

echo "🚀 MIA Fulfillment Dashboard v2.0"
echo "=================================="

# Parse arguments
SETUP_ONLY=false
AUTOMATION_ONLY=false
TEST_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --setup)
            SETUP_ONLY=true
            shift
            ;;
        --automation)
            AUTOMATION_ONLY=true
            shift
            ;;
        --test)
            TEST_ONLY=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --setup        Setup system only"
            echo "  --automation   Run automation only"
            echo "  --test         Run tests only"
            echo "  --help         Show this help"
            echo ""
            echo "Examples:"
            echo "  $0             # Run dashboard (default)"
            echo "  $0 --setup     # Setup system"
            echo "  $0 --test      # Run tests"
            exit 0
            ;;
        *)
            echo "❌ Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    echo "💡 macOS: brew install python"
    echo "💡 Ubuntu: sudo apt install python3 python3-pip"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install/update requirements
echo "📦 Installing/updating dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Setup mode
if [ "$SETUP_ONLY" = true ]; then
    echo "🔧 Setting up system..."

    # Create directories
    mkdir -p data/{raw,processed,exports}
    mkdir -p logs/{dashboard,automation}
    mkdir -p src/{core,automation,components,utils,config}
    mkdir -p tests scripts docs/{api,user}

    echo "✅ Directory structure created"
    echo "🎉 Setup completed!"
    echo ""
    echo "Next steps:"
    echo "  1. Run: ./start.sh --test"
    echo "  2. Run: ./start.sh"
    exit 0
fi

# Test mode
if [ "$TEST_ONLY" = true ]; then
    echo "🧪 Running system tests..."

    if [ -f "main.py" ]; then
        python main.py --test
    else
        echo "❌ main.py not found"
        exit 1
    fi
    exit 0
fi

# Automation mode
if [ "$AUTOMATION_ONLY" = true ]; then
    echo "🤖 Running automation..."

    if [ -f "main.py" ]; then
        python main.py --automation
    else
        echo "❌ main.py not found"
        exit 1
    fi
    exit 0
fi

# Default: Run dashboard
echo "🌟 Starting dashboard..."

# Clean up any existing processes
echo "🔄 Cleaning up processes..."
pkill -f streamlit || true
sleep 2

# Check which entry point to use
if [ -f "main.py" ]; then
    echo "✅ Using new structure (v2.0)"
    python main.py
elif [ -f "app.py" ]; then
    echo "⚠️  Using legacy structure (v1.0)"
    echo "💡 Consider upgrading to v2.0"
    echo "🚀 Starting Streamlit on port 8502..."
    streamlit run app.py --server.port 8502 --server.address 0.0.0.0
else
    echo "❌ No valid entry point found"
    echo "Expected: main.py (v2.0) or app.py (v1.0)"
    exit 1
fi
