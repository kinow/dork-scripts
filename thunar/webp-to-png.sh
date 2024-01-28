# 1. Open Thunar
# 2. Select "Edit" / "Configure custom actions..."
# 3. Enter the name "WebP to PNG"
# 4. Description "Convert WebP images to PNG and delete the WebP image"
# 5. Set the command to the example below
# 6. Grab an icon for the context menu shortcut, e.g. https://www.flaticon.com

find . -maxdepth 1 -name "*.webp" -exec bash -c 'convert {}  $(basename "{}" | rev | cut -d. -f2- | rev).png && rm {}' \;
