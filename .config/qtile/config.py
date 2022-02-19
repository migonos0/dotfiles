# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
import subprocess

writeCurrentLayoutNameFilePath = '/home/miguel/.config/qtile/writeCurrentLayoutName.py'
mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "a", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "d", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "s", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "w", lazy.layout.up(), desc="Move focus up"),

    # Switch with alt tab
    Key(['mod1'], 'Tab', lazy.group.next_window()),
    Key(['mod1', 'shift'], 'Tab', lazy.group.prev_window()),

    # Move the windows
    # Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
    #     desc="Move window to the left"),
    # Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
    #     desc="Move window to the right"),
    Key([mod, "shift"], "s", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "w", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "a", lazy.layout.swap_left()),
    Key([mod, "shift"], "d", lazy.layout.swap_right()),

    # Grow windows
    # Key([mod, "control"], "h", lazy.layout.grow_left(),
    #     desc="Grow window to the left"),
    # Key([mod, "control"], "l", lazy.layout.grow_right(),
    #     desc="Grow window to the right"),
    # Key([mod, "control"], "j", lazy.layout.grow_down(),
    #     desc="Grow window down"),
    # Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "e", lazy.layout.grow()),
    Key([mod], "q", lazy.layout.shrink()),

    # Normalize, maximize
    Key([mod, 'shift'], "f", lazy.layout.normalize(),
        desc="Reset all window sizes"),
    Key([mod], "f", lazy.layout.maximize()),

    # On columns
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    # Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
    #     desc="Toggle between split and unsplit sides of stack"),

    # Toggle floating window
    Key([mod, 'control'], 'Tab', lazy.window.toggle_floating()),

    # Move to the last visited group
    Key([mod], "Tab", lazy.screen.toggle_group()),

    # On monad tall put change the master column betweeen the left or the right one.
    #Key([mod, "shift"], "space", lazy.layout.flip()),

    # Spawn terminals
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod, 'shift'], "Tab", lazy.next_layout(), lazy.spawn('python {}'.format(
        writeCurrentLayoutNameFilePath)), desc="Toggle between layouts"),

    # Kill
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    # Qtile
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # rofi
    Key([mod], "r", lazy.spawn('rofi -show run'),
        desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "r", lazy.spawn('rofi -show windowcd'),
        desc="Spawn a command using a prompt widget"),
    Key([mod, "control"], "f", lazy.spawn('rofi -show filebrowser'),
        desc="Spawn a command using a prompt widget"),


    # Sound
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pulseaudio-control --volume-max 153 down")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pulseaudio-control --volume-max 153 up")),

    # Backlight
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +10%")),

    # Screenshot
    Key([mod], "dead_grave", lazy.spawn("flameshot gui")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(
            toggle=False), desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    # layout.Columns(border_focus_stack='#d75f5f'),
    layout.MonadTall(single_border_width=0, new_client_position='top',
                     border_width=1, border_focus='#0000ff', ratio=0.618, margin=0),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(bg_color="282a33", active_bg="0000ff",
    #                sections=[''], section_top=0, section_fg="282a33", panel_width=68),
    # layout.VerticalTile(),
    # layout.Zoomy(columnwidth=68, margin=[4, 0, 4, 0]),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(top=bar.Gap(19))
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry')
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Autostart


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen(['{}/.config/qtile/autostart'.format(home)])

# On group change


@hook.subscribe.setgroup
def writeCurrentLayoutName():
    subprocess.Popen(['python', writeCurrentLayoutNameFilePath])
