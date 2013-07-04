#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Widgets.py
#
#  Copyright 2013 Ignacio Rodríguez <ignacio@sugarlabs.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import mimetypes
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GConf
from gi.repository import GObject

from sugar3.graphics.icon import Icon
from sugar3.graphics.xocolor import XoColor


def get_current_icon():
    client = GConf.Client.get_default()
    path = "/desktop/sugar/user/icon"
    value = client.get_string(path)
    if value:
        return value
    else:
        return "computer-xo"


def get_icons(path):
    if not os.path.exists(path):
        os.mkdir(path)

    icon_theme = Gtk.IconTheme.get_default()
    if not path in icon_theme.get_search_path():
        icon_theme.append_search_path(path)

    list_icons = os.listdir(path)
    list_icons.sort()

    icons = ['computer-xo']
    for icon in list_icons:
        icon_path = os.path.join(path, icon)
        if not icon_path:
            continue

        mimetype = mimetypes.guess_type(icon_path)[0]
        if "svg" in mimetype:
            icon_name = icon[:-4]
            if not icon_name in icons:
                icons.append(icon_name)
    return icons


class XoHome(Gtk.Fixed):
    """
    Simulate XO Home with custom icon.
    """
    def __init__(self, icon):
        super(XoHome, self).__init__()

        self.home = Gtk.Image()
        self.home.set_from_file("images/Home.png")

        self.home_box = Gtk.EventBox()
        x = Gdk.Screen.width()
        self.home_box.set_size_request(x, -1)
        self.home_box.add(self.home)

        self.put(self.home_box, 0, 0)

        self.last_icon = icon
        self.update(None, icon)

        self.show_all()

    def update(self, widget, icon):
        self.remove(self.last_icon)
        self.last_icon = icon
        # Classmate:  X = 431
        # XO: X = 521
        X = 521
        Y = 240

        self.put(icon, X, Y)
        self.show_all()


class XoIcons(Gtk.Box):

    __gsignals__ = {
    'icon_changed': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}

    def __init__(self):
        super(XoIcons, self).__init__(orientation=Gtk.Orientation.HORIZONTAL)

        path = os.path.join(os.path.expanduser("~"), ".icons")
        self.list_icons = get_icons(path)
        self.icons = {}
        self.fill_list(self.list_icons)
        self.show_all()

    def fill_list(self, icons):

        client = GConf.Client.get_default()
        path = "/desktop/sugar/user/color"
        color = client.get_string(path)
        xocolor = XoColor(color)
        current = get_current_icon()

        for icon_name in icons:
            icon = Icon(icon_name=icon_name, xo_color=xocolor,
                                pixel_size=100)

            icon_box = Gtk.EventBox()
            icon_box.add(icon)
            icon_box.connect("button-press-event", self.update)

            icon_fixed = Icon(icon_name=icon_name, xo_color=xocolor,
                                pixel_size=146)
            icon_box.set_tooltip_text(icon_name)
            icon_box.set_property("has-tooltip", False)

            self.pack_start(icon_box, True, True, 0)
            self.pack_start(Gtk.VSeparator(), False, False, 3)

            if icon_name == current:
                self.icon = icon_fixed
            self.icons[icon_box] = icon_fixed

    def get_icon(self):
        return self.icon

    def update(self, widget, event):
        self.emit('icon_changed', self.icons[widget])


class XoIcon(Gtk.Box):
    def __init__(self):
        super(XoIcon, self).__init__(orientation=Gtk.Orientation.VERTICAL)

        self.icons = XoIcons()
        self.home = XoHome(self.icons.get_icon())

        self.icons.connect("icon_changed", self.home.update)

        self.home_box = Gtk.EventBox()
        self.home_box.modify_bg(Gtk.StateType.NORMAL,
                            Gdk.color_parse("white"))
        self.home_box.add(self.home)

        self.icons_box = Gtk.EventBox()
        self.icons_box.modify_bg(Gtk.StateType.NORMAL,
                            Gdk.color_parse("white"))
        self.icons_box.add(self.icons)

        self.icons_scroll = Gtk.ScrolledWindow()
        self.icons_scroll.set_policy(Gtk.PolicyType.AUTOMATIC,
                                    Gtk.PolicyType.AUTOMATIC)
        self.icons_scroll.add_with_viewport(self.icons_box)

        self.icons_scroll.set_size_request(-1, 143)

        self.pack_start(self.home_box, True, True, 0)
        self.pack_start(self.icons_scroll, False, False, 0)
        self.show_all()
