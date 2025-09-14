#!/bin/bash
# Deploy webview build to Anki add-on location

set -e

ANKI_ADDON_DIR="/Users/jeremyparker/Library/Application Support/Anki2/addons21/1915225457"
DEV_WEBVIEW_DIR="./webview"

echo "🚀 Deploying webview to Anki add-on..."

# Check if development webview build exists
if [ ! -d "$DEV_WEBVIEW_DIR/build" ]; then
    echo "❌ No build directory found. Running npm run build first..."
    cd "$DEV_WEBVIEW_DIR"
    npm run build
    cd ..
fi

# Check if Anki add-on directory exists
if [ ! -d "$ANKI_ADDON_DIR" ]; then
    echo "❌ AnkiBrain add-on not found in Anki. Please install the add-on first."
    echo "Expected location: $ANKI_ADDON_DIR"
    exit 1
fi

# Create webview directory if it doesn't exist
if [ ! -d "$ANKI_ADDON_DIR/webview" ]; then
    echo "📁 Creating webview directory in add-on..."
    mkdir -p "$ANKI_ADDON_DIR/webview"
fi

# Copy build files
echo "📦 Copying build files..."
cp -r "$DEV_WEBVIEW_DIR/build/"* "$ANKI_ADDON_DIR/webview/build/"

# Verify deployment
if grep -q "gpt-5" "$ANKI_ADDON_DIR/webview/build/static/js/main."*.js 2>/dev/null; then
    echo "✅ Deployment successful! ChatGPT 5 models are included."
    echo "📋 Please restart Anki to see the changes."
else
    echo "⚠️  Deployment completed but ChatGPT 5 models not detected in build."
fi

echo "🎉 Webview deployment complete!"