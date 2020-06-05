import os
import shutil
import ctypes
from ctypes import wintypes
def install_font(src_path):
    # copy the font to the Windows Fonts folder
    dst_path = os.path.join(os.environ['SystemRoot'], 'Fonts',
                            os.path.basename(src_path))
    shutil.copy(src_path, dst_path)
    # load the font in the current session
    if not gdi32.AddFontResourceW(dst_path):
        os.remove(dst_path)
        raise WindowsError('AddFontResource failed to load "%s"' % src_path)
    # notify running programs
    user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0,
                               SMTO_ABORTIFHUNG, 1000, None)
    # store the fontname/filename in the registry
    filename = os.path.basename(dst_path)
    fontname = os.path.splitext(filename)[0]
    # try to get the font's real name
    cb = wintypes.DWORD()
    if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), None,
                                  GFRI_DESCRIPTION):
        buf = (ctypes.c_wchar * cb.value)()
        if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), buf,
                                      GFRI_DESCRIPTION):
            fontname = buf.value
    is_truetype = wintypes.BOOL()
    cb.value = ctypes.sizeof(is_truetype)
    gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb),
        ctypes.byref(is_truetype), GFRI_ISTRUETYPE)
    if is_truetype:
        fontname += ' (TrueType)'
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, FONTS_REG_PATH, 0,
                        winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)

# if __name__=="__main__": 
#     path = (r"assets\fonts\SF-Pro-Display-Regular.otf")
#     install_font(path)