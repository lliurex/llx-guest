#!/bin/bash

UI_FILES="../llx-guest-gui.install/usr/share/llx-guest/rsrc/llx-guest.ui"
PYTHON_FILES="../llx-guest-gui.install/usr/share/llx-guest/LlxGuest.py"

xgettext $UI_FILES $PYTHON_FILES -o llx-guest/llx-guest.pot

