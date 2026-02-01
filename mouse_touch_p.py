import time
import win32api
from pynput import keyboard

from wintoucher.util.touch import TouchManager

# Inicializamos el inyector táctil (1 dedo)
touch = TouchManager(1)

TOUCH_ID = 0
TAP_DELAY = 0.03  # 30 ms


def tap_at_mouse():
    x, y = win32api.GetCursorPos()
    print(f"TAP táctil en {x}, {y}")

    touch.down(TOUCH_ID, x, y)
    touch.apply_touches()

    time.sleep(TAP_DELAY)

    touch.up(TOUCH_ID)
    touch.apply_touches()


def on_press(key):
    try:
        # Tecla normal
        if key.char == "p":
            tap_at_mouse()
    except AttributeError:
        # Teclas especiales (ignoramos)
        pass


def on_release(key):
    # ESC para salir limpiamente
    if key == keyboard.Key.esc:
        print("Saliendo…")
        return False


print("P   → toque táctil en la posición del ratón")
print("ESC → salir")
print("Ejecuta como ADMINISTRADOR")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
