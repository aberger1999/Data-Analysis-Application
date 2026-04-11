"""
Windows 11 DWM helpers for the DataLens window chrome.

Only the DWM calls that actually affect the immersive (Win11) title bar
live here:
  * DWMWA_USE_IMMERSIVE_DARK_MODE / caption color / text color / border color
  * DWMWA_WINDOW_CORNER_PREFERENCE (rounded corners)
  * DwmExtendFrameIntoClientArea (preserves the drop shadow when the
    non-client area is collapsed via WM_NCCALCSIZE for a custom
    title bar implementation)

Everything that was previously here for SystemParametersInfoW /
NONCLIENTMETRICS / caption font / caption button width was removed —
those APIs only affect the classic Windows theme and have no effect on
the Win11 DWM-rendered title bar.
"""

import sys
import ctypes
import ctypes.wintypes

DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWA_BORDER_COLOR = 34
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36
DWMWCP_ROUND = 2


class _MARGINS(ctypes.Structure):
    _fields_ = [
        ("cxLeftWidth", ctypes.c_int),
        ("cxRightWidth", ctypes.c_int),
        ("cyTopHeight", ctypes.c_int),
        ("cyBottomHeight", ctypes.c_int),
    ]


def _dwm_set_attribute(hwnd, attribute, value):
    try:
        dwmapi = ctypes.windll.dwmapi
        val = ctypes.c_int(value)
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            attribute,
            ctypes.byref(val),
            ctypes.sizeof(val)
        )
        return True
    except Exception:
        return False


def _rgb_to_bgr_int(hex_color: str) -> int:
    """Convert #rrggbb hex to Windows COLORREF (BGR int)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return b | (g << 8) | (r << 16)


def extend_frame_for_shadow(hwnd: int, top: int = 1):
    """
    Extend the DWM frame 1px into the client area so Windows still draws
    its drop shadow and rounded corners after WM_NCCALCSIZE collapses the
    non-client area. Without this call, a custom-title-bar window loses
    its shadow.
    """
    if sys.platform != "win32":
        return
    try:
        margins = _MARGINS(0, 0, top, 0)
        ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(
            hwnd, ctypes.byref(margins)
        )
    except Exception:
        pass


def update_dwm_theme(hwnd: int, theme: str):
    """
    Lightweight theme update for an already-styled window.

    Only flips the two attributes that remain visible once
    WM_NCCALCSIZE has collapsed the non-client area:
      - immersive dark mode (affects the resize border look)
      - border color (the 1px outer border)

    Skips caption color / text color (invisible, because the caption
    is client-rendered) and skips rounded corners / extended frame
    (set once at startup, they don't change with theme).
    """
    if sys.platform != "win32":
        return
    if theme == "dark":
        _dwm_set_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 1)
        _dwm_set_attribute(
            hwnd, DWMWA_BORDER_COLOR, _rgb_to_bgr_int("#2d3148")
        )
    else:
        _dwm_set_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 0)
        _dwm_set_attribute(
            hwnd, DWMWA_BORDER_COLOR, _rgb_to_bgr_int("#d1d5db")
        )


def apply_modern_window_style(hwnd: int, theme: str):
    """
    Apply Windows 11 modern styling to a window. Must be called AFTER
    the window is visible (after show()).  hwnd = int(widget.winId())

    This only touches things DWM actually honors on Win11:
      - immersive dark mode
      - caption background / caption text / border colors
      - rounded corners
      - extended frame (for shadow retention under WM_NCCALCSIZE)
    """
    if sys.platform != "win32":
        return

    if theme == "dark":
        _dwm_set_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 1)
        _dwm_set_attribute(
            hwnd, DWMWA_CAPTION_COLOR, _rgb_to_bgr_int("#0f1117")
        )
        _dwm_set_attribute(
            hwnd, DWMWA_TEXT_COLOR, _rgb_to_bgr_int("#ffffff")
        )
        _dwm_set_attribute(
            hwnd, DWMWA_BORDER_COLOR, _rgb_to_bgr_int("#2d3148")
        )
    else:
        _dwm_set_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 0)
        _dwm_set_attribute(
            hwnd, DWMWA_CAPTION_COLOR, _rgb_to_bgr_int("#e8eaf0")
        )
        _dwm_set_attribute(
            hwnd, DWMWA_TEXT_COLOR, _rgb_to_bgr_int("#0f172a")
        )
        _dwm_set_attribute(
            hwnd, DWMWA_BORDER_COLOR, _rgb_to_bgr_int("#d1d5db")
        )

    # Rounded corners (Windows 11 style) — applies regardless of theme
    _dwm_set_attribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, DWMWCP_ROUND)

    # Keep drop shadow after WM_NCCALCSIZE removes the non-client area
    extend_frame_for_shadow(hwnd, top=1)
