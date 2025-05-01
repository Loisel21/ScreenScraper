import win32gui
import win32con
import win32com.client

# Callback-Funktion zum Sammeln von Fenstern
def enum_windows_callback(hwnd, window_list):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:  # Nur Fenster mit Titel
            window_list.append((hwnd, title))

# Fenster mit bestimmtem Titelteil suchen
def find_windows_by_title_part(part):
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    matching = [(hwnd, title) for hwnd, title in windows if part.lower() in title.lower()]
    return matching

# Fenster in den Vordergrund bringen
def bring_window_to_front_by_hwnd(hwnd):
    shell = win32com.client.Dispatch("WScript.Shell")
    try:
        # Trick: Aktiviere kurz dein eigenes Fenster, um Fokusrechte zu bekommen
        shell.SendKeys('%')  # Sendet ALT-Taste (öffnet nichts, beeinflusst Fokusrechte)

        # Wenn minimiert: wiederherstellen
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        # Dann in den Vordergrund bringen
        win32gui.SetForegroundWindow(hwnd)

    except Exception as e:
        print(f"Fehler beim Aktivieren des Fensters: {e}")

def is_window_in_foreground(hwnd):
    foreground_hwnd = win32gui.GetForegroundWindow()
    return hwnd == foreground_hwnd

# Beispielverwendung
def dingtalk_window():
    search_term = "ding"  # z.B. nach Notepad/Editor suchen
    matches = find_windows_by_title_part(search_term)

    if matches:
        #print("Gefundene Fenster:")
        # for i, (hwnd, title) in enumerate(matches):
        #     print(f"{i}: {title} (HWND: {hwnd})")
        
        # Erstes passendes Fenster in den Vordergrund holen

        if is_window_in_foreground(matches[0][0]):
            #print("Das Fenster ist bereits im Vordergrund.")
            return True
        else:
            bring_window_to_front_by_hwnd(matches[0][0])
            return True
    else:
        return False
