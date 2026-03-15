#!/bin/bash

# TODO: For XFCE this needs a better integration... a widget? A button somewhere? Shortcut?

wmctrl -r "São Paulo - Wikipedia" -b add,skip_taskbar,skip_pager

wmctrl -r "São Paulo - Wikipedia" -b remove,skip_taskbar,skip_pager
