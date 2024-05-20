"""
Twelvety 
[12ty]
By Greg Gaughan
"""
import board

from kmk.extensions.LED import LED
from kmk.extensions.peg_oled_Display import (
    Oled,
    OledData,
    OledDisplayMode,
    OledReactionType,
)
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC, make_key
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.modules.combos import Combos, Chord, Sequence
from kmk.modules.holdtap import HoldTap
from kmk.modules.tapdance import TapDance
from kmk.modules.layers import Layers as _Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.media_keys import MediaKeys

combos = Combos()
holdtap = HoldTap()
tapdance = TapDance()
media_keys = MediaKeys()

#todo? holdtap.tap_time = 300
#todo? tapdance.tap_time = 750

keyboard = KMKKeyboard()

# I2C pins for the mini OLED display
keyboard.SCL = board.D5
keyboard.SDA = board.D4

keyboard.modules.append(combos)
keyboard.modules.append(holdtap)
keyboard.modules.append(tapdance)
keyboard.extensions.append(media_keys)

LD = [
    {'name':'Base'},
    {'name':'Move'},
    {'name':'Edit'},
    {'name':'Mouse'},
    {'name':'Function'},
    {'name':'Number'},
    {'name':'+ move'},
]


oled = Oled(
    OledData(
        corner_one={0: OledReactionType.STATIC, 1: ['      TWELVETY']},
        corner_two={0: OledReactionType.STATIC, 1: ['']},
        corner_three={0: OledReactionType.LAYER, 1: [l['name'] for l in LD]},
        corner_four={0: OledReactionType.STATIC, 1: [' ']},
    ),
    oWidth=128,
    oHeight=64,
    toDisplay=OledDisplayMode.TXT,
    flip=False,
)
keyboard.extensions.append(oled)


#keyboard.modules.append(layers)
#   Neopixel on XIAO RP2040
frontglow = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    #tgb_order=(0,1,2)  #default 1,0,2:GRB?
    val_limit=100,
    val_default=25,
    #animation_mode=AnimationModes.RAINBOW,
)
keyboard.extensions.append(frontglow)

#sat = 255
#val = 5
#layers = _Layers()
class Layers(_Layers):
    last_top_layer = 0
    
    def after_hid_send(self, keyboard):
        
        if keyboard.active_layers[0] != self.last_top_layer:
            oln = LD[self.last_top_layer]['name']
            self.last_top_layer = keyboard.active_layers[0]
            ln = LD[self.last_top_layer]['name']
            if ln.startswith('+'):
                ln = oln + " " + ln
            # ln = ln + " *{}*".format(len(keyboard.active_layers))
            # i.e. init data corner_three
            # oled._views[2][1][self.last_top_layer] = ln
            #ln = "+".join([LD[i]['name'] for i,l in enumerate(keyboard.active_layers)])
            oled._views[2][1][self.last_top_layer] = ln
            
            # todo get colour direct from LD
            if self.last_top_layer == 0:
                frontglow.set_rgb_fill((0,5,0))       # green
            elif self.last_top_layer == 1:
                frontglow.set_rgb_fill((5,5,0))       # yellow
            elif self.last_top_layer == 2:
                frontglow.set_rgb_fill((5,0,0))       # red
            elif self.last_top_layer == 3:
                frontglow.set_hsv_fill(0, 0, 5)     # white
            elif self.last_top_layer == 4:
                frontglow.set_rgb_fill((3,3,0))       # green/yellow
            elif self.last_top_layer == 5:
                frontglow.set_rgb_fill((0,5,5))       # turq
layers = Layers()
keyboard.modules.append(layers)


keyboard.modules.append(MouseKeys())


led = LED(
    led_pin=[
        board.D0,
    ],
    brightness=100,
    brightness_step=5,
    brightness_limit=100,
    breathe_center=1.5,
    animation_mode=AnimationModes.STATIC,
    animation_speed=1,
    user_animation=None,
    val=100,
)
#print("LEDs", led._leds)
#keyboard.extensions.append(led)

# WS2812B LED strips on the back
underglow = RGB(
    pixel_pin=board.D10,
    num_pixels=6,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,  #RGB_MODE_PLAIN, #
)
#underglow.off()
#keyboard.extensions.append(underglow)


keyboard.col_pins = (board.D6, board.D8, board.D9)
keyboard.row_pins = (board.D1, board.D2, board.D3, board.D7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# todo remove: double-tap ctrl to toggle numbers instead - else reduces typing speed!
# note: wraps: so alt,ctrl gets to numbers plus will add some combos!
# K1 = KC.TD(KC.A, KC.N1)
# K2 = KC.TD(KC.N, KC.N2)
# K3 = KC.TD(KC.R, KC.N3)
# K4 = KC.TD(KC.H, KC.N4)
# K5 = KC.TD(KC.O, KC.N5)
# K6 = KC.TD(KC.E, KC.N6)
# K7 = KC.TD(KC.T, KC.N7)
# K8 = KC.TD(KC.I, KC.N8)
# K9 = KC.TD(KC.S, KC.N9)
K1 = KC.A
K2 = KC.N
K3 = KC.R
K4 = KC.H
K5 = KC.O
K6 = KC.E
K7 = KC.T
K8 = KC.I
K9 = KC.S


KMOD0 = KC.TD(
            KC.HT(KC.TG(len(LD)-1), KC.LCTRL), #, tap_time=50, prefer_hold=True),
            KC.MO(5),  # i.e. press twice + hold (then auto bounce back)
            #KC.ESC,  # todo perhaps TG(6)? mouse move?
            #KC.BSPACE,
)
KMOD0b = KC.TD(
            KC.LCTRL,   # no len(LD)-1 to avoid Move+move
            KC.MO(5),
)
KMOD0c = KMOD0
KMOD0d = KMOD0
KMOD0e = KMOD0
KMOD0f = KC.TD(
            KC.HT(KC.TG(len(LD)-1), KC.LCTRL),
            # no 5 to avoid recursion
)

#KMOD0 = KC.TD(
#            KC.HT(KC.TO(0), KC.LCTRL), #, prefer_hold=True),
#            KC.TO(1),
#            KC.TO(2),
#        )

##KMOD0 = KC.TD(
            ##KC.HT(KC.TG(1), KC.LCTRL), #, prefer_hold=True),
            ##KC.TG(0),
        ##)
##KMOD1 = KC.TD(
            ##KC.HT(KC.TG(2), KC.LCTRL), #, prefer_hold=True),
            ##KC.TG(0),
        ##)

KMOD1 = KC.HT(KC.SPACE, KC.LALT)
KMOD1b = KC.HT(KC.SPACE, KC.LALT)
KMOD1c = KC.HT(KC.SPACE, KC.LALT)
KMOD1d = KC.HT(KC.SPACE, KC.LALT)
KMOD1e = KC.HT(KC.SPACE, KC.LALT)
KMOD1f = KC.HT(KC.SPACE, KC.LALT)


KMOD2 = KC.HT(KC.ENTER, KC.LSHIFT)

# todo move to LD? and build here
# Matrix 4x3 keymap, 12 keys in total
keyboard.keymap = [
    [ # Base 0
        KMOD0,
        KMOD1,
        KMOD2,
        K1,
        K2,
        K3,
        K4,
        K5,
        K6,
        K7,
        K8,
        K9,
    ],
    
    [ # Move 1
        KMOD0b,
        KMOD1b,
        KMOD2,
        KC.LEFT,
        KC.DOWN,
        KC.RIGHT,
        KC.HOME,
        KC.UP,
        KC.END,
        KC.PGUP,
        KC.INSERT,  # todo review/replace
        KC.PGDN,
    ],
    
    [ # Edit 2
        KMOD0c,
        KMOD1c,
        KMOD2,
        KC.LEFT,
        KC.DOWN,
        KC.RIGHT,
        KC.HOME,
        KC.UP,
        KC.END,
        KC.LCTRL(KC.X),
        KC.LCTRL(KC.C),
        KC.LCTRL(KC.V),
    ],
    
    [ # Mouse 3
        KMOD0d,
        KMOD1d,
        KMOD2,
        KC.MS_LEFT,
        KC.MS_DOWN,
        KC.MS_RIGHT,
        KC.MB_LMB,
        KC.MS_UP,
        KC.MB_RMB,
        KC.MW_DOWN,
        KC.MB_MMB,
        KC.MW_UP,
    ],

    [ # Function 4
        KMOD0e,
        KMOD1e,
        KMOD2,
        KC.F1,
        KC.F2,
        KC.F3,
        KC.F4,
        KC.F5,
        KC.F6,
        KC.F7,
        KC.F8,
        KC.F9,
    ],


    [ # Number 5
        KMOD0f,
        KMOD1f,
        KMOD2,
        KC.N1,
        KC.N2,
        KC.N3,
        KC.N4,
        KC.N5,
        KC.N6,
        KC.N7,
        KC.N8,
        KC.N9,
    ],
    
    # Media?
    # WASD / Pico-play (use device buttons!)
    #        - maybe Move + move does WASD? no need: already doing the transformation via hardware



    [ # Move overlay (for Base and Number mainly) - prefix name with '+' in LD
        KC.TRNS,
        KC.TRNS,
        KC.TRNS,
        KC.LEFT,
        KC.DOWN,
        KC.RIGHT,
        KC.HOME,
        KC.UP,
        KC.END,
        KC.PGUP,
        KC.INSERT,  # todo review/replace
        KC.PGDN,
    ],


]

make_key(
    names=('NUM',),
    #on_press=lambda *args: print('I pressed MYKEY'),
    #on_press=keyboard.keys_pressed.add(KC.LEADER),
)

combos.combos = [
    Chord((KC.LSHIFT, KC.LALT), KC.LGUI),
    
    # Base
    Chord((K6, K3), KC.B),
    Chord((K9, K3), KC.C),
    Chord((K7, K8), KC.D),
    Chord((K9, K6), KC.F),
    Chord((K5, K6), KC.G),
    Chord((K8, K1), KC.J),
    Chord((K9, K5), KC.K),
    Chord((K2, K3), KC.L),
    Chord((K7, K9), KC.W),
    Chord((K8, K9), KC.P),
    Chord((K5, K2, K3), KC.Q),
    Chord((K4, K2), KC.U),
    Chord((K2, K6), KC.V),
    Chord((K1, K3), KC.M),
    Chord((K5, K3), KC.X),
    Chord((K7, K5), KC.Y),
    Chord((K7, K3), KC.Z),
    # todo rethink: clash with #
    # Base numbers  - after other chords, e.g. Hash for precedence
    Chord((K4, K1), KC.NUM),
    Sequence((KC.NUM, KC.A), KC.N1),
    Sequence((KC.NUM, K2), KC.N2),
    Sequence((KC.NUM, K3), KC.N3),
    Sequence((KC.NUM, K4), KC.N4),
    Sequence((KC.NUM, K5), KC.N5),
    Sequence((KC.NUM, K6), KC.N6),
    Sequence((KC.NUM, K7), KC.N7),
    Sequence((KC.NUM, K8), KC.N8),
    Sequence((KC.NUM, K9), KC.N9),
    Sequence((KC.NUM, K9), KC.N9),
    # todo 0

    # Chord((K4, K6), KC.N0),
    # Chord((K7, K9, K1), KC.N1),
    # Chord((K7, K9, K2), KC.N2),
    # Chord((K7, K9, K3), KC.N3),
    # Chord((K1, K3, K4), KC.N4),
    # Chord((K1, K3, K5), KC.N5),
    # Chord((K1, K3, K6), KC.N6),
    # Chord((K1, K3, K7), KC.N7),
    # Chord((K1, K3, K8), KC.N8),
    # Chord((K1, K3, K9), KC.N9),

    # todo add more Chords to function layer, maybe media?, F13..F24?
    Chord((KC.F4, KC.F6), KC.F10),
    Chord((KC.F4, KC.F7), KC.F11),
    Chord((KC.F4, KC.F8), KC.F12),

    Chord((KC.F1, KC.F7), KC.PSCREEN),
    Chord((KC.F1, KC.F8), KC.SCROLLLOCK),
    Chord((KC.F1, KC.F9), KC.PAUSE),

    Chord((KC.F1, KC.F5), KC.MEDIA_PLAY_PAUSE),  # mnemonic: comma = pause  # todo: same as KC.PAUSE for me (i.e. map in OS)


    # todo copy these to other layers... ? programmatically? via a chord template + LD[*]['keys'][0..8]
    Chord((K1, K2, K3), KC.SPACE),
    Chord((K4, K5), KC.TAB),
    Chord((K9, K6, K3), KC.ENTER),
    Chord((K7, K4, K1), KC.ESC),
    Chord((K6, K1, K2), KC.DEL),
    Chord((K1, K2), KC.BSPACE),
    Chord((K8, K5, K2), KC.PLUS),
    Chord((K4, K5, K6), KC.MINUS),
    Chord((K7, K5, K9), KC.ASTERISK),
    Chord((K9, K5, K1), KC.SLASH),
    Chord((K7, K8, K9), KC.EQUAL),
    Chord((K5, K2), KC.DOT),
    Chord((K8, K4, K1), KC.LEFT_PAREN),
    Chord((K8, K6, K3), KC.RIGHT_PAREN),
    Chord((K1, K2, K3), KC.UNDERSCORE),
    Chord((K8, K7, K4), KC.LBRACKET),
    Chord((K8, K9, K6), KC.RBRACKET),
    Chord((K7, K5, K1), KC.LEFT_CURLY_BRACE),
    Chord((K9, K5, K3), KC.RIGHT_CURLY_BRACE),
    Chord((K8, K5, K1), KC.SCOLON),
    Chord((K8, K2), KC.COLON),
    Chord((K9, K7, K3, K1), KC.NONUS_HASH),
    Chord((K8, K4, K2), KC.LEFT_ANGLE_BRACKET),
    Chord((K8, K6, K2), KC.RIGHT_ANGLE_BRACKET),
    Chord((K7, K8, K5), KC.QUESTION),
    Chord((K7, K5, K3), KC.NONUS_BSLASH),
    Chord((K8, K4), KC.QUOTE),
    Chord((K8, K5), KC.DOUBLE_QUOTE),
    Chord((K5, K1), KC.COMMA),
    Chord((K8, K6), KC.GRAVE),

    # Move layer
    Chord((KC.PGUP, KC.HOME, KC.LEFT), KC.ESC),
    Chord((KC.END, KC.LEFT, KC.DOWN,), KC.DEL),
    Chord((KC.LEFT, KC.DOWN,), KC.BSPACE),
    # todo more
    
    # Function layer
    Chord((KC.F1, KC.F2, KC.F3), KC.SPACE),
    Chord((KC.F4, KC.F5), KC.TAB),
    Chord((KC.F9, KC.F6, KC.F3), KC.ENTER),
    Chord((KC.F7, KC.F4, KC.F1), KC.ESC),
    Chord((KC.F6, KC.F1, KC.F2), KC.DEL),
    Chord((KC.F1, KC.F2), KC.BSPACE),
    Chord((KC.F8, KC.F5, KC.F2), KC.PLUS),
    Chord((KC.F4, KC.F5, KC.F6), KC.MINUS),
    Chord((KC.F7, KC.F5, KC.F9), KC.ASTERISK),
    Chord((KC.F9, KC.F5, KC.F1), KC.SLASH),
    Chord((KC.F7, KC.F8, KC.F9), KC.EQUAL),
    Chord((KC.F5, KC.F2), KC.DOT),
    Chord((KC.F8, KC.F4, KC.F1), KC.LEFT_PAREN),
    Chord((KC.F8, KC.F6, KC.F3), KC.RIGHT_PAREN),
    Chord((KC.F1, KC.F2, KC.F3), KC.UNDERSCORE),
    Chord((KC.F8, KC.F7, KC.F4), KC.LBRACKET),
    Chord((KC.F8, KC.F9, KC.F6), KC.RBRACKET),
    Chord((KC.F7, KC.F5, KC.F1), KC.LEFT_CURLY_BRACE),
    Chord((KC.F9, KC.F5, KC.F3), KC.RIGHT_CURLY_BRACE),
    Chord((KC.F8, KC.F5, KC.F1), KC.SCOLON),
    Chord((KC.F8, KC.F2), KC.COLON),
    Chord((KC.F9, KC.F7, KC.F3, K1), KC.NONUS_HASH),
    Chord((KC.F8, KC.F4, KC.F2), KC.LEFT_ANGLE_BRACKET),
    Chord((KC.F8, KC.F6, KC.F2), KC.RIGHT_ANGLE_BRACKET),
    Chord((KC.F7, KC.F8, KC.F5), KC.QUESTION),
    Chord((KC.F7, KC.F5, KC.F3), KC.NONUS_BSLASH),
    Chord((KC.F8, KC.F4), KC.QUOTE),
    Chord((KC.F8, KC.F5), KC.DOUBLE_QUOTE),
    Chord((KC.F5, KC.F1), KC.COMMA),
    Chord((KC.F8, KC.F6), KC.GRAVE),
   


    # Number layer
    Chord((KC.N4, KC.N6), KC.N0),
    Chord((KC.N1, KC.N2, KC.N3), KC.SPACE),
    Chord((KC.N4, KC.N5), KC.TAB),
    Chord((KC.N9, KC.N6, KC.N3), KC.ENTER),
    Chord((KC.N7, KC.N4, KC.N1), KC.ESC),
    Chord((KC.N6, KC.N1, KC.N2), KC.DEL),
    Chord((KC.N1, KC.N2), KC.BSPACE),
    Chord((KC.N8, KC.N5, KC.N2), KC.PLUS),
    Chord((KC.N4, KC.N5, KC.N6), KC.MINUS),
    Chord((KC.N7, KC.N5, KC.N9), KC.ASTERISK),
    Chord((KC.N9, KC.N5, KC.N1), KC.SLASH),
    Chord((KC.N7, KC.N8, KC.N9), KC.EQUAL),
    Chord((KC.N5, KC.N2), KC.DOT),
    Chord((KC.N8, KC.N4, KC.N1), KC.LEFT_PAREN),
    Chord((KC.N8, KC.N6, KC.N3), KC.RIGHT_PAREN),
    Chord((KC.N1, KC.N2, KC.N3), KC.UNDERSCORE),
    Chord((KC.N8, KC.N7, KC.N4), KC.LBRACKET),
    Chord((KC.N8, KC.N9, KC.N6), KC.RBRACKET),
    Chord((KC.N7, KC.N5, KC.N1), KC.LEFT_CURLY_BRACE),
    Chord((KC.N9, KC.N5, KC.N3), KC.RIGHT_CURLY_BRACE),
    Chord((KC.N8, KC.N5, KC.N1), KC.SCOLON),
    Chord((KC.N8, KC.N2), KC.COLON),
    #Chord((KC.N9, KC.N7, KC.N3, KC.N1), KC.NONUS_HASH),
    Chord((KC.N9, KC.N7, KC.N3, KC.N1), KC.HASH),  # note: alternative
    Chord((KC.N8, KC.N4, KC.N2), KC.LEFT_ANGLE_BRACKET),
    Chord((KC.N8, KC.N6, KC.N2), KC.RIGHT_ANGLE_BRACKET),
    Chord((KC.N7, KC.N8, KC.N5), KC.QUESTION),
    #Chord((KC.N7, KC.N5, KC.N3), KC.NONUS_BSLASH),
    Chord((KC.N7, KC.N5, KC.N3), KC.BSLASH),  # note: alternative
    Chord((KC.N8, KC.N4), KC.QUOTE),
    Chord((KC.N8, KC.N5), KC.DOUBLE_QUOTE),
    Chord((KC.N5, KC.N1), KC.COMMA),
    Chord((KC.N8, KC.N6), KC.GRAVE),


    # Layer switching - todo build from LD
    Sequence((KMOD0, KMOD1), KC.TO(1), timeout=100), # , per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD0b, KMOD1b), KC.TO(2), timeout=100), #, per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD0c, KMOD1c), KC.TO(3), timeout=100), #, per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD0d, KMOD1d), KC.TO(4), timeout=100),
    Sequence((KMOD0e, KMOD1e), KC.TO(5), timeout=100), # wrap
    Sequence((KMOD0f, KMOD1f), KC.TO(0), timeout=100), # wrap
    Sequence((KMOD1f, KMOD0f), KC.TO(4), timeout=100), #, per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD1e, KMOD0e), KC.TO(3), timeout=100), #, per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD1d, KMOD0d), KC.TO(2), timeout=100), #, per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD1c, KMOD0c), KC.TO(1), timeout=100), #, per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD1b, KMOD0b), KC.TO(0), timeout=100), #, per_key_timeout=False), #, fast_reset=False)
    Sequence((KMOD1, KMOD0), KC.TO(len(LD)-2), timeout=100), # wrap (ignore last +Move)
]


if __name__ == '__main__':
    keyboard.go()
