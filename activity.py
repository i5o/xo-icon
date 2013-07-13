#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  activity.py
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

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import _create_activity_icon as ActivityIcon
from sugar3.graphics.alert import NotifyAlert

from gi.repository import GConf
from gi.repository import Gtk
from Widgets import XoIcon

from gettext import gettext as _


class IconChangeActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle, False)
        self.max_participants = 1

        self.toolbar_box = ToolbarBox()
        self.toolbar = self.toolbar_box.toolbar

        activity_button = ToolButton()
        icon = ActivityIcon(None)
        activity_button.set_icon_widget(icon)
        activity_button.set_tooltip(self.get_title())
        stop_button = StopButton(self)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)

        self.confirm_button = ToolButton("dialog-ok")
        self.confirm_button.set_tooltip(_("Apply changes"))
        self.confirm_button.connect("clicked", self.apply_changes)

        self.toolbar.insert(activity_button, 0)
        self.toolbar.insert(Gtk.SeparatorToolItem(), -1)
        self.toolbar.insert(self.confirm_button, -1)

        self.toolbar.insert(separator, -1)
        self.toolbar.insert(stop_button, -1)

        self.canvas = XoIcon()

        self.set_toolbar_box(self.toolbar_box)
        self.set_canvas(self.canvas)
        self.show_all()

    def apply_changes(self, widget):
        self.write(self.canvas.get_icon())
        self.notify_alert()

    def write(self, icon):
        client = GConf.Client.get_default()
        path = "/desktop/sugar/user/icon"
        client.set_string(path, icon)
        return True

    def notify_alert(self):
        alert = NotifyAlert()
        alert.props.title = _('Saving icon...')
        msg = _('A restart is required before your new icon will appear.')
        alert.props.msg = msg

        def remove_alert(alert, response_id):
            self.remove_alert(alert)

        alert.connect('response', remove_alert)
        self.add_alert(alert)
