#!/bin/bash
xgettext --join-existing -L python ../llx-guest-gui.install/usr/share/llx-guest/llx-guest-gui -o ../translations/llx-guest/llx-guest.pot
xgettext -kde -ki18nd:2 ../llx-guest-gui.install/usr/share/llx-guest/rsrc/llx-guest.qml -o ..../translations/llx-guest/llx-guest.pot
xgettext --join-existing -kde -ki18nd:2 ../llx-guest-gui.install/usr/share/llx-guest/rsrc/ApplicationOptions.qml -o ../translations/llx-guest/llx-guest.pot
xgettext --join-existing -kde -ki18nd:2 ../llx-guest-gui.install/usr/share/llx-guest/rsrc/Settings.qml -o ../translations/llx-guest/llx-guest.pot
xgettext --join-existing -kde -ki18nd:2 ../llx-guest-gui.install/usr/share/llx-guest/rsrc/Loading.qml -o ../translations/llx-guest/llx-guest.pot
xgettext --join-existing -kde -ki18nd:2 ../llx-guest-gui.install/usr/share/llx-guest/rsrc/ChangesDialog.qml -o ../translations/llx-guest/llx-guest.pot
