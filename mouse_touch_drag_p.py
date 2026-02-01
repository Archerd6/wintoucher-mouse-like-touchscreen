import time
import win32api
from pynput import keyboard, mouse

from wintoucher.util.touch import TouchManager, TouchError

touch = TouchManager(1)

TOUCH_ID = 0
UPDATE_INTERVAL = 0.015  # 15 ms → seguro para Windows
DRAG_KEY = keyboard.Key.shift

dragging = False
last_pos = None
last_update = 0


def start_drag():
    global dragging, last_pos, last_update

    if dragging:
        return

    x, y = win32api.GetCursorPos()
    print(f"TOUCH DOWN en {x}, {y}")

    touch.down(TOUCH_ID, x, y)
    touch.apply_touches()

    dragging = True
    last_pos = (x, y)
    last_update = time.time()


def update_drag(x, y):
    global last_pos, last_update

    if not dragging:
        return

    now = time.time()

    # 1️⃣ No enviar si no hay movimiento real
    if last_pos == (x, y):
        return

    # 2️⃣ Limitar frecuencia
    if now - last_update < UPDATE_INTERVAL:
        return

    try:
        touch.move(TOUCH_ID, x, y)
        touch.apply_touches()
        last_pos = (x, y)
        last_update = now
    except TouchError:
        # Silencioso: evita crash si Windows rechaza un frame
        pass


def end_drag():
    global dragging

    if not dragging:
        return

    print("TOUCH UP")

    try:
        touch.up(TOUCH_ID)
        touch.apply_touches()
    except TouchError:
        pass

    dragging = False


def on_key_press(key):
    if key == DRAG_KEY:
        start_drag()


def on_key_release(key):
    if key == keyboard.Key.esc:
        print("Saliendo…")
        return False

    if key == DRAG_KEY:
        end_drag()


def on_move(x, y):
    update_drag(x, y)


print("Mantén SHIFT → dedo abajo (long press / drag)")
print("Mueve ratón → deslizar")
print("Suelta SHIFT → dedo arriba")
print("ESC → salir")

with keyboard.Listener(
    on_press=on_key_press,
    on_release=on_key_release,
) as k_listener, mouse.Listener(
    on_move=on_move,
) as m_listener:
    k_listener.join()
    m_listener.join()
