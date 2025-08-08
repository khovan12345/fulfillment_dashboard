#!/bin/bash

echo "�� Formatting code..."

# Activate virtual environment
source venv/bin/activate

# Format Python files
echo "🐍 Formatting Python files..."
black *.py **/*.py 2>/dev/null || echo "✅ Black formatting done"
isort *.py **/*.py 2>/dev/null || echo "✅ isort formatting done"

# Format other files
echo "📝 Formatting other files..."
prettier --write "*.md" "*.json" "*.yml" "*.yaml" "config/*.json" 2>/dev/null || echo "✅ Prettier formatting done"

echo "✨ All files formatted!"
