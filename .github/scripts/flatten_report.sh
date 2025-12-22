set -e  # Exit on any error

BROWSER=$1
TYPE=$2  # e.g., "latest-only" or "latest-with-history"
TEMP_DIR=$3
TARGET_DIR=$4
RUN_ID=$5

echo "Contents of $TEMP_DIR:"
ls -R "$TEMP_DIR/" || echo "Directory doesn't exist"

# Prefer the known build folder structure
BUILD_DIR="$TEMP_DIR/build-$BROWSER-$RUN_ID"
if [ -d "$BUILD_DIR" ]; then
  cp -r "$BUILD_DIR"/* "$TARGET_DIR/"
  echo "✅ $BROWSER $TYPE report deployed from build-$BROWSER-$RUN_ID"
else
  # Fallback: copy from the first subdirectory in the artifact path
  SUBDIR=$(find "$TEMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1 || true)
  if [ -n "$SUBDIR" ]; then
    echo "Using fallback subdir: $SUBDIR"
    cp -r "$SUBDIR"/* "$TARGET_DIR/"
    echo "✅ $BROWSER $TYPE report deployed from fallback directory"
  else
    echo "❌ $BROWSER $TYPE structure not found; no suitable directory to deploy"
  fi
fi