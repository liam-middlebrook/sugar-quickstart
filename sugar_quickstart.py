from string import Template
import os
import stat
import sys

def chmod_x(f):
    st = os.stat(f)
    os.chmod(f, st.st_mode | stat.S_IEXEC)

activity_activity_generic_svg = r"""<?xml version="1.0" ?><!-- Created with Inkscape (http://www.inkscape.org/) --><!DOCTYPE svg  PUBLIC '-//W3C//DTD SVG 1.1//EN'  'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd' [
	<!ENTITY stroke_color "#ff0000">
	<!ENTITY fill_color "#000000">
]><svg height="55" id="svg2" inkscape:output_extension="org.inkscape.output.svg.inkscape" inkscape:version="0.46+devel" sodipodi:docname="activity-generic.svg" sodipodi:version="0.32" style="" version="1.0" width="55" xmlns="http://www.w3.org/2000/svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:svg="http://www.w3.org/2000/svg">
  <metadata id="metadata20">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <sodipodi:namedview bordercolor="#666666" borderopacity="1" gridtolerance="10" guidetolerance="10" id="namedview18" inkscape:current-layer="svg2" inkscape:cx="-15.963983" inkscape:cy="27.5" inkscape:pageopacity="0" inkscape:pageshadow="2" inkscape:window-height="1125" inkscape:window-width="1920" inkscape:window-x="0" inkscape:window-y="25" inkscape:zoom="4.2909091" objecttolerance="10" pagecolor="#ffffff" showgrid="true">
    <inkscape:grid id="grid796" type="xygrid"/>
  </sodipodi:namedview>
  <defs id="defs4" style="">
    <inkscape:perspective id="perspective22" inkscape:persp3d-origin="27.5 : 18.333333 : 1" inkscape:vp_x="0 : 27.5 : 1" inkscape:vp_y="0 : 1000 : 0" inkscape:vp_z="55 : 27.5 : 1" sodipodi:type="inkscape:persp3d"/>
  </defs>
  <g id="layer1" style="fill:&fill_color;;fill-opacity:1;stroke:&stroke_color;;stroke-opacity:1;stroke-width:3.002554;stroke-miterlimit:4;stroke-dasharray:none" transform="matrix(1.1689037,0,0,1.1624538,-4.6448521,-4.3634813)">
    <rect height="35" id="rect16" style="fill:&fill_color;;fill-opacity:1;stroke:&stroke_color;;stroke-width:3.002554;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" width="35" x="10" y="10"/>
    <text id="text790" style="font-size:40px;font-style:normal;font-weight:normal;fill:&stroke_color;;fill-opacity:1;stroke:none;stroke-opacity:1;font-family:Bitstream Vera Sans;stroke-width:3.00255399999999995;stroke-miterlimit:4;stroke-dasharray:none" x="17.911133" xml:space="preserve" y="40"><tspan id="tspan792" style="font-size:36px;fill:&stroke_color;;fill-opacity:1;stroke:none;stroke-opacity:1;stroke-width:3.00255399999999995;stroke-miterlimit:4;stroke-dasharray:none" x="17.911133" y="40">?</tspan></text>
  </g>
</svg>
"""

activity_activity_info = r"""[Activity]
name = {project_display_name}
bundle_id = edu.rit.{project_name}
exec = sugar-activity {project_name}Activity.{project_name}Activity
icon = activity-generic
activity_version = 1
"""

activity_mimetypes_xml = r"""<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/x-physics-activity">
         <comment xml:lang="en">Physics Activity</comment>
         <glob pattern="*.physics"/>
  </mime-type>
</mime-info>
"""

project_activity_py = r"""from gettext import gettext as _

import sys
from gi.repository import Gtk
import pygame

import sugar3.activity.activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton


import sugargame.canvas

import {project_name}


class {project_name}Activity(sugar3.activity.activity.Activity):
    def __init__(self, handle):
        super({project_name}Activity, self).__init__(handle)

        self.paused = False

        # Create the game instance.
        self.game = {project_name}.{project_name}()

        # Build the activity toolbar.
        self.build_toolbar()

        # Build the Pygame canvas.
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)

        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self._pygamecanvas)

        # Start the game running (self.game.run is called when the
        # activity constructor returns).
        self._pygamecanvas.run_pygame(self.game.run)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        # Pause/Play button:

        stop_play = ToolButton('media-playback-stop')
        stop_play.set_tooltip(_("Stop"))
        stop_play.set_accelerator(_('<ctrl>space'))
        stop_play.connect('clicked', self._stop_play_cb)
        stop_play.show()

        toolbar_box.toolbar.insert(stop_play, -1)

        # Blank space (separator) and Stop button at the end:

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

    def _stop_play_cb(self, button):
        # Pause or unpause the game.
        self.paused = not self.paused
        self.game.set_paused(self.paused)

        # Update the button to show the next action.
        if self.paused:
            button.set_icon('media-playback-start')
            button.set_tooltip(_("Start"))
        else:
            button.set_icon('media-playback-stop')
            button.set_tooltip(_("Stop"))

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)
"""

project_py = r"""#!/usr/bin/python
import pygame
from gi.repository import Gtk


class {project_name}:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.x = -100
        self.y = 100

        self.vx = 10
        self.vy = 0

        self.paused = False
        self.direction = 1

    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    # The main game loop.
    def run(self):
        self.running = True

        screen = pygame.display.get_surface()

        while self.running:
            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = -1
                    elif event.key == pygame.K_RIGHT:
                        self.direction = 1

            # Move the ball
            if not self.paused:
                self.x += self.vx * self.direction
                if self.direction == 1 and self.x > screen.get_width() + 100:
                    self.x = -100
                elif self.direction == -1 and self.x < -100:
                    self.x = screen.get_width() + 100

                self.y += self.vy
                if self.y > screen.get_height() - 100:
                    self.y = screen.get_height() - 100
                    self.vy = -self.vy

                self.vy += 5

            # Clear Display
            screen.fill((255, 255, 255))  # 255 for white

            # Draw the ball
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 100)

            # Flip Display
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)


# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = {project_name}()
    game.run()

if __name__ == '__main__':
    main()
"""

setup_py = r"""#!/usr/bin/env python
from sugar3.activity import bundlebuilder
bundlebuilder.start()
"""

sugargame_canvas_py = r"""import os
from gi.repository import Gtk
from gi.repository import GObject
import pygame
import event

CANVAS = None

class PygameCanvas(Gtk.EventBox):
    
    '''
    mainwindow is the activity intself.
    '''
    def __init__(self, mainwindow, pointer_hint = True):
        GObject.GObject.__init__(self)

        global CANVAS
        assert CANVAS == None, "Only one PygameCanvas can be created, ever."
        CANVAS = self

        # Initialize Events translator before widget gets "realized".
        self.translator = event.Translator(mainwindow, self)
        
        self._mainwindow = mainwindow

        self.set_can_focus(True)
        
        self._socket = Gtk.Socket()
        self.add(self._socket)
        self.show_all()

    def run_pygame(self, main_fn):
        # Run the main loop after a short delay.  The reason for the delay is that the
        # Sugar activity is not properly created until after its constructor returns.
        # If the Pygame main loop is called from the activity constructor, the 
        # constructor never returns and the activity freezes.
        GObject.idle_add(self._run_pygame_cb, main_fn)

    def _run_pygame_cb(self, main_fn):
        assert pygame.display.get_surface() is None, "PygameCanvas.run_pygame can only be called once."
        
        # Preinitialize Pygame with the X window ID.
        assert pygame.display.get_init() == False, "Pygame must not be initialized before calling PygameCanvas.run_pygame."
        os.environ['SDL_WINDOWID'] = str(self._socket.get_id())
        pygame.init()
        
        # Restore the default cursor.
        self._socket.props.window.set_cursor(None)

        # Initialize the Pygame window.
        r = self.get_allocation()
        pygame.display.set_mode((r.width, r.height), pygame.RESIZABLE)

        # Hook certain Pygame functions with GTK equivalents.
        self.translator.hook_pygame()

        # Run the Pygame main loop.
        main_fn()
        return False

    def get_pygame_widget(self):
        return self._socket
"""

sugargame_event_py = r"""from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
import pygame
import pygame.event
import logging 

class _MockEvent(object):
    def __init__(self, keyval):
        self.keyval = keyval

class Translator(object):
    key_trans = {
        'Alt_L': pygame.K_LALT,
        'Alt_R': pygame.K_RALT,
        'Control_L': pygame.K_LCTRL,
        'Control_R': pygame.K_RCTRL,
        'Shift_L': pygame.K_LSHIFT,
        'Shift_R': pygame.K_RSHIFT,
        'Super_L': pygame.K_LSUPER,
        'Super_R': pygame.K_RSUPER,
        'KP_Page_Up' : pygame.K_KP9, 
        'KP_Page_Down' : pygame.K_KP3,
        'KP_End' : pygame.K_KP1, 
        'KP_Home' : pygame.K_KP7,
        'KP_Up' : pygame.K_KP8,
        'KP_Down' : pygame.K_KP2,
        'KP_Left' : pygame.K_KP4,
        'KP_Right' : pygame.K_KP6,

    }
    
    mod_map = {
        pygame.K_LALT: pygame.KMOD_LALT,
        pygame.K_RALT: pygame.KMOD_RALT,
        pygame.K_LCTRL: pygame.KMOD_LCTRL,
        pygame.K_RCTRL: pygame.KMOD_RCTRL,
        pygame.K_LSHIFT: pygame.KMOD_LSHIFT,
        pygame.K_RSHIFT: pygame.KMOD_RSHIFT,
    }
    
    def __init__(self, mainwindow, inner_evb):
        '''Initialise the Translator with the windows to which to listen'''
        self._mainwindow = mainwindow
        self._inner_evb = inner_evb

        # Enable events
        # (add instead of set here because the main window is already realized)
        self._mainwindow.add_events(
            Gdk.EventMask.KEY_PRESS_MASK | \
            Gdk.EventMask.KEY_RELEASE_MASK \
        )
        
        self._inner_evb.set_events(
            Gdk.EventMask.POINTER_MOTION_MASK | \
            Gdk.EventMask.POINTER_MOTION_HINT_MASK | \
            Gdk.EventMask.BUTTON_MOTION_MASK | \
            Gdk.EventMask.BUTTON_PRESS_MASK | \
            Gdk.EventMask.BUTTON_RELEASE_MASK 
        )

        self._mainwindow.set_can_focus(True)
        self._inner_evb.set_can_focus(True)
        
        # Callback functions to link the event systems
        self._mainwindow.connect('unrealize', self._quit_cb)
        self._inner_evb.connect('key_press_event', self._keydown_cb)
        self._inner_evb.connect('key_release_event', self._keyup_cb)
        self._inner_evb.connect('button_press_event', self._mousedown_cb)
        self._inner_evb.connect('button_release_event', self._mouseup_cb)
        self._inner_evb.connect('motion-notify-event', self._mousemove_cb)
        self._inner_evb.connect('draw', self._draw_cb)
        self._inner_evb.connect('configure-event', self._resize_cb)
        
        # Internal data
        self.__stopped = False
        self.__keystate = [0] * 323
        self.__button_state = [0,0,0]
        self.__mouse_pos = (0,0)
        self.__repeat = (None, None)
        self.__held = set()
        self.__held_time_left = {}
        self.__held_last_time = {}
        self.__tick_id = None

    def hook_pygame(self):
        pygame.key.get_pressed = self._get_pressed
        pygame.key.set_repeat = self._set_repeat
        pygame.mouse.get_pressed = self._get_mouse_pressed
        pygame.mouse.get_pos = self._get_mouse_pos
        
    def _draw_cb(self, widget, event):
        if pygame.display.get_init():
            pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE))
        return True

    def _resize_cb(self, widget, event):
        evt = pygame.event.Event(pygame.VIDEORESIZE, 
                                 size=(event.width,event.height), width=event.width, height=event.height)
        pygame.event.post(evt)
        return False # continue processing

    def _quit_cb(self, data=None):
        self.__stopped = True
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _keydown_cb(self, widget, event):
        key = event.keyval
        if key in self.__held:
            return True
        else:
            if self.__repeat[0] is not None:
                self.__held_last_time[key] = pygame.time.get_ticks()
                self.__held_time_left[key] = self.__repeat[0]
            self.__held.add(key)
            
        return self._keyevent(widget, event, pygame.KEYDOWN)
        
    def _keyup_cb(self, widget, event):
        key = event.keyval
        if self.__repeat[0] is not None:
            if key in self.__held:
                # This is possibly false if set_repeat() is called with a key held
                del self.__held_time_left[key]
                del self.__held_last_time[key]
        self.__held.discard(key)

        return self._keyevent(widget, event, pygame.KEYUP)
        
    def _keymods(self):
        mod = 0
        for key_val, mod_val in self.mod_map.iteritems():
            mod |= self.__keystate[key_val] and mod_val
        return mod
        
    def _keyevent(self, widget, event, type):
        key = Gdk.keyval_name(event.keyval)
        if key is None:
            # No idea what this key is.
            return False 
        
        keycode = None
        if key in self.key_trans:
            keycode = self.key_trans[key]
        elif hasattr(pygame, 'K_'+key.upper()):
            keycode = getattr(pygame, 'K_'+key.upper())
        elif hasattr(pygame, 'K_'+key.lower()):
            keycode = getattr(pygame, 'K_'+key.lower())
        elif key == 'XF86Start':
            # view source request, specially handled...
            self._mainwindow.view_source()
        else:
            print 'Key %s unrecognized' % key
            
        if keycode is not None:
            if type == pygame.KEYDOWN:
                mod = self._keymods()
            self.__keystate[keycode] = type == pygame.KEYDOWN
            if type == pygame.KEYUP:
                mod = self._keymods()
            ukey = unichr(Gdk.keyval_to_unicode(event.keyval))
            if ukey == '\000':
                ukey = ''
            evt = pygame.event.Event(type, key=keycode, unicode=ukey, mod=mod)
            self._post(evt)
            
        return True

    def _get_pressed(self):
        return self.__keystate

    def _get_mouse_pressed(self):
        return self.__button_state

    def _mousedown_cb(self, widget, event):
        self.__button_state[event.button-1] = 1
        return self._mouseevent(widget, event, pygame.MOUSEBUTTONDOWN)

    def _mouseup_cb(self, widget, event):
        self.__button_state[event.button-1] = 0
        return self._mouseevent(widget, event, pygame.MOUSEBUTTONUP)
        
    def _mouseevent(self, widget, event, type):
        evt = pygame.event.Event(type, button=event.button, pos=(event.x, event.y))
        self._post(evt)
        return True
        
    def _mousemove_cb(self, widget, event):
        # From http://www.learningpython.com/2006/07/25/writing-a-custom-widget-using-pygtk/
        # if this is a hint, then let's get all the necessary 
        # information, if not it's all we need.
        if event.is_hint:
            win, x, y, state = event.window.get_device_position(event.device)
        else:
            x = event.x
            y = event.y
            state = event.get_state()

        rel = (x - self.__mouse_pos[0], y - self.__mouse_pos[1])
        self.__mouse_pos = (x, y)
        
        self.__button_state = [
            state & Gdk.ModifierType.BUTTON1_MASK and 1 or 0,
            state & Gdk.ModifierType.BUTTON2_MASK and 1 or 0,
            state & Gdk.ModifierType.BUTTON3_MASK and 1 or 0,
        ]
        
        evt = pygame.event.Event(pygame.MOUSEMOTION,
                                 pos=self.__mouse_pos, rel=rel, buttons=self.__button_state)
        self._post(evt)
        return True
        
    def _tick_cb(self):
        cur_time = pygame.time.get_ticks()
        for key in self.__held:
            delta = cur_time - self.__held_last_time[key] 
            self.__held_last_time[key] = cur_time
            
            self.__held_time_left[key] -= delta
            if self.__held_time_left[key] <= 0:
                self.__held_time_left[key] = self.__repeat[1]
                self._keyevent(None, _MockEvent(key), pygame.KEYDOWN)
                
        return True
        
    def _set_repeat(self, delay=None, interval=None):
        if delay is not None and self.__repeat[0] is None:
            self.__tick_id = GObject.timeout_add(10, self._tick_cb)
        elif delay is None and self.__repeat[0] is not None:
            GObject.source_remove(self.__tick_id)
        self.__repeat = (delay, interval)
        
    def _get_mouse_pos(self):
        return self.__mouse_pos

    def _post(self, evt):
        try:
            pygame.event.post(evt)
        except pygame.error, e:
            if str(e) == 'Event queue full':
                print "Event queue full!"
                pass
            else:
                raise e
"""

sugargame_init_py = r"""__version__ = '1.1'
"""

readme_md = r"""{project_display_name}
======
## Prerequisites

>   ./setup.py genpot
>   ./setup.py build

## Running

>   ./{project_name}.py

## Deploying

### On the XO

>   ./setup.py install

### On another computer

If you want to distribute the game onto an XOPC

>   ./setup.py dist_xo

If you want to distribute the game onto a regular computer

>   ./setup.py dist
"""

project_display_name = raw_input("Project Name: ")
project_name = raw_input("Project Class Name: ")

if len(sys.argv) < 2:
    print("No argument for output_dir given!")
    os.exit(1)

output_dir = sys.argv[1]

activity_dir = os.path.join(output_dir, "activity")
sugargame_dir = os.path.join(output_dir, "sugargame")

if not os.path.exists(activity_dir):
    os.makedirs(activity_dir)

if not os.path.exists(sugargame_dir):
    os.makedirs(sugargame_dir)

with open(os.path.join(activity_dir, "activity-generic.svg"), "w+") as text_file:
    text_file.write(activity_activity_generic_svg)

with open(os.path.join(activity_dir, "mimetypes.xml"), "w+") as text_file:
    text_file.write(activity_mimetypes_xml)

with open(os.path.join(activity_dir, "activity.info"), "w+") as text_file:
    text_file.write(
        activity_activity_info.format(
            project_name=project_name,
            project_display_name=project_display_name
        )
    )

with open(os.path.join(output_dir, project_name + "Activity.py"), "w+") as text_file:
    text_file.write(
        project_activity_py.format(
            project_name=project_name,
            project_display_name=project_display_name
        )
    )

with open(os.path.join(output_dir, project_name + ".py"), "w+") as text_file:
    text_file.write(
        project_py.format(
            project_name=project_name,
            project_display_name=project_display_name
        )
    )

chmod_x(os.path.join(output_dir, project_name + ".py"))

with open(os.path.join(output_dir, "setup.py"), "w+") as text_file:
    text_file.write(setup_py)

chmod_x(os.path.join(output_dir, "setup.py"))

with open(os.path.join(sugargame_dir, "canvas.py"), "w+") as text_file:
    text_file.write(sugargame_canvas_py)

with open(os.path.join(sugargame_dir, "event.py"), "w+") as text_file:
    text_file.write(sugargame_event_py)

with open(os.path.join(sugargame_dir, "__init__.py"), "w+") as text_file:
    text_file.write(sugargame_init_py)

with open(os.path.join(output_dir, "README.md"), "w+") as text_file:
    text_file.write(
        readme_md.format(
            project_name=project_name,
            project_display_name=project_display_name
        )
    )
