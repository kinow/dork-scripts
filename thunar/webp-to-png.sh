# Ref: https://docs.xfce.org/xfce/thunar/4.14/custom-actions
#
# 1. Open Thunar
# 2. Select "Edit" / "Configure custom actions..."
# 3. Enter the name "WebP/Avif to PNG"
# 4. Description "Convert WebP and Avif images to PNG and delete the WebP image"
# 5. Set the command to the example below
# 6. Grab an icon for the context menu shortcut, e.g. https://www.flaticon.com

find . -maxdepth 1 -regex ".*\(\.webp\|\.avif\)" -exec bash -c 'convert "{}" "$(basename "{}" | rev | cut -d. -f2- | rev).png" && rm "{}"' \;
