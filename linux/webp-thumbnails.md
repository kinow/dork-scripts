You need XFCE and ImageMagick and `libwebpmux3` for this.

```bash
$ apt install imagemagick libwebpmux3
```

Create the file `/usr/share/thumbnailers/webp.thumbnailer`.

```ini
[Thumbnailer Entry]
Version=1.0
Encoding=UTF-8
Type=X-Thumbnailer
Name=webp Thumbnailer
MimeType=image/webp;
Exec=/usr/local/bin/webpthumbs %s %i %o
```
Then create `/usr/local/bin/webpthumbs`.

```bash
#!/bin/bash

if tempfile=$(mktemp) && /usr/bin/webpmux -get frame 1 "$2" -o "$tempfile"; then
  /usr/bin/convert -thumbnail "$1" "$tempfile" "$3"
else
  /usr/bin/convert -thumbnail "$1" "$2" "$3"
fi

[ -f "$tempfile" ] && rm "$tempfile"[/quote]
```

Log out and log in again, or run `xfdesktop --reload`.
