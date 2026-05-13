---
name: reference_brother_scanner_workflow
description: "How to scan from Scott's Brother printer on his Windows PC (no scan app installed; drive it via WIA from PowerShell)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a33f9aa1-d73e-4b26-8cb9-302ad35769c2
---

Scott's scanner is a **Brother MFC-L3770CDW** (USB/network, recognised by Windows as a WIA + eSCL device). His PC has **no scan GUI installed** — no Windows Scan app, no Brother iPrint&Scan/ControlCenter (only "Brother Print Support App", print-only). Windows Fax and Scan (`WFS.exe`) is also absent.

**To scan for him:** drive WIA directly from PowerShell — `New-Object -ComObject WIA.DeviceManager`, find the device whose Name is `*Brother*`, `.Connect()`, `$device.Items.Item(1).Transfer("{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}")` (JPEG GUID), `$image.SaveFile(...)`. Defaults used: colour, 200 DPI. Output goes to `C:\Users\smckennie\Pictures\Scan_<timestamp>.jpg`. Page sits on the **flatbed glass** unless told it's in the **ADF feeder** (multi-page). It scans whatever is physically on the glass — same page each call until he swaps it.

**Image → PDF:** Python 3.13 at `C:\Python313` with **Pillow 12** is installed → `Image.open(f).convert("RGB").rotate(180, expand=True)` then `pages[0].save(out_pdf, save_all=True, append_images=pages[1:], resolution=200.0, quality=82)`. (Also available if needed: Ghostscript `C:\GDAL\bin\gswin64c.exe`, Word interop.) 2026-05-12 first use: scanned Audrey's THUNDER basketball Individual Performance Plan (4 pages, were upside-down → rotated 180°), combined to `Pictures\Scanned_2026-05-12.pdf` (~750 KB) to send to her coach.
