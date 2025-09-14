#!/bin/bash
# Deploy AnkiBrain changes to actual Anki addon directory

echo "🚀 Deploying AnkiBrain changes to runtime directory..."

RUNTIME_DIR="$HOME/Library/Application Support/Anki2/addons21/1915225457"

# Copy core files
echo "📁 Copying model compatibility layer..."
cp model_compatibility.py "$RUNTIME_DIR/"

echo "📁 Copying ChatAI directory..."
cp -r ChatAI/* "$RUNTIME_DIR/ChatAI/"

echo "📁 Copying test files..."
cp test_model_compatibility.py "$RUNTIME_DIR/"

echo "✅ Deployment complete!"
echo "🔄 Please restart Anki to load the changes."
echo ""
echo "📍 Runtime directory: $RUNTIME_DIR"
