"""Inline SVG icon set (24x24, stroke-based). Original simple geometric drawings."""

P = {
    "drop": '<path d="M12 2.8S5 10.2 5 14.6a7 7 0 0 0 14 0C19 10.2 12 2.8 12 2.8z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
    "flame": '<path d="M12 22c3.9 0 7-2.8 7-7 0-3.4-2.3-5.9-3.8-7.9-.2 2-1 3.4-2.4 4.1C12.6 8 11 5 8.2 2.2 8.5 5.3 7 7.4 5.7 9.3 4.9 10.5 5 12.6 5 15c0 4.2 3.1 7 7 7z"/>',
    "snow": '<path d="M12 2v20M3.3 7l17.4 10M3.3 17 20.7 7"/><path d="m9 4 3 2 3-2M9 20l3-2 3 2"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3 20 3M16 7l3 3M14 9l2 2"/>',
    "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/><path d="M10 20v-5h4v5"/>',
    "roof": '<path d="M2 13 12 5l10 8"/><path d="M5 11v9h14v-9"/><path d="M14 3h3v4"/>',
    "tree": '<path d="M12 2 5.5 11H9l-3.5 6h13L15 11h3.5z"/><path d="M12 17v5"/>',
    "wrench": '<path d="M14.6 6.4a4 4 0 0 0-5.3 5.2L3.5 17.4a1.5 1.5 0 0 0 0 2.1l1 1a1.5 1.5 0 0 0 2.1 0l5.8-5.8a4 4 0 0 0 5.2-5.3l-2.4 2.4-2.3-.6-.6-2.3z"/>',
    "fan": '<circle cx="12" cy="12" r="2"/><path d="M12 10c-.4-3.6.7-6.5 3.3-6.5 2.4 0 2.6 3.7-1.3 6.5M14 12c3.6-.4 6.5.7 6.5 3.3 0 2.4-3.7 2.6-6.5-1.3M12 14c.4 3.6-.7 6.5-3.3 6.5-2.4 0-2.6-3.7 1.3-6.5M10 12c-3.6.4-6.5-.7-6.5-3.3 0-2.4 3.7-2.6 6.5 1.3"/>',
    "alert": '<path d="M12 3.5 2.5 20h19z"/><path d="M12 10v4.5M12 17.2v.1"/>',
    "garage": '<path d="M3 21V9.5L12 4l9 5.5V21"/><path d="M7 21v-8h10v8M7 15.5h10M7 18h10"/>',
    "spore": '<circle cx="8" cy="9" r="3"/><circle cx="16" cy="8" r="2"/><circle cx="15" cy="16" r="3.5"/><circle cx="7" cy="17" r="1.6"/>',
    "pipe": '<path d="M3 6h7v5H3zM10 8.5h4a3 3 0 0 1 3 3V15"/><path d="M14.5 15h5v5h-5z"/>',
    "fridge": '<rect x="6" y="2.5" width="12" height="19" rx="2"/><path d="M6 9.5h12M9 5.5v2M9 12.5v3"/>',
    "shield": '<path d="M12 2.5 4.5 5.5v6c0 4.6 3.2 8.4 7.5 10 4.3-1.6 7.5-5.4 7.5-10v-6z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "dollar": '<circle cx="12" cy="12" r="9"/><path d="M15 9.2c-.6-1-1.7-1.5-3-1.5-1.7 0-3 .9-3 2.2 0 3 6 1.6 6 4.4 0 1.3-1.3 2.2-3 2.2-1.4 0-2.6-.6-3.1-1.6M12 6v1.7M12 16.5v1.6"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20.5 20.5-4.8-4.8"/>',
    "phone": '<path d="M5 3.5h3.5l1.5 4.5-2.2 1.5a11 11 0 0 0 5.7 5.7l1.5-2.2 4.5 1.5V18a2.5 2.5 0 0 1-2.5 2.5A15.5 15.5 0 0 1 2.5 6 2.5 2.5 0 0 1 5 3.5z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 7 8.5-7"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "heart": '<path d="M12 20.5S3.5 15.3 3.5 9.3A4.8 4.8 0 0 1 12 6.5a4.8 4.8 0 0 1 8.5 2.8c0 6-8.5 11.2-8.5 11.2z"/>',
    "trophy": '<path d="M7.5 4h9v5a4.5 4.5 0 0 1-9 0z"/><path d="M7.5 6H4.5a3 3 0 0 0 3 4M16.5 6h3a3 3 0 0 1-3 4M12 13.5V17M8.5 20.5h7M9.5 17h5v3.5h-5z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 5v2M3 12.5h18"/>',
    "megaphone": '<path d="M3.5 10v4h3l8 4.5v-13l-8 4.5z"/><path d="M6.5 14l1.5 5.5h2.5L9.5 14M18 9a4 4 0 0 1 0 6"/>',
    "play": '<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="m10 9 5 3-5 3z"/>',
    "calc": '<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M8 6.5h8M8 11h.01M12 11h.01M16 11h.01M8 14.5h.01M12 14.5h.01M16 14.5v3.5M8 18h.01M12 18h.01"/>',
    "list": '<path d="M9 6.5h11M9 12h11M9 17.5h11"/><path d="m3.5 6.5 1.2 1.2L7 5.3M3.5 12l1.2 1.2L7 10.8M3.5 17.5l1.2 1.2L7 16.3"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4M7.5 13.5h3v3h-3z"/>',
    "pin": '<path d="M12 21.5s-7-6.2-7-11.5a7 7 0 0 1 14 0c0 5.3-7 11.5-7 11.5z"/><circle cx="12" cy="10" r="2.5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14a6.5 6.5 0 0 1 3.5 6"/>',
    "check": '<path d="m4.5 12.5 4.5 4.5 10.5-11"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "arrow": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/>',
    "moon": '<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>',
    "menu": '<path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17"/>',
    "plug": '<path d="M8 2.5v5M16 2.5v5M5.5 7.5h13v3a6.5 6.5 0 0 1-13 0zM12 17v4.5"/>',
    "hammer": '<path d="M13.5 6.5 4 16a2 2 0 0 0 2.8 2.8l9.5-9.5"/><path d="m12 5 3-3 7 7-3 3-2-2-2 2-3-3 2-2z"/>',
    "gift": '<rect x="3.5" y="8" width="17" height="4.5" rx="1"/><path d="M5 12.5V21h14v-8.5M12 8v13M12 8S10.5 3.5 8 4.2C5.5 5 7.5 8 12 8zM12 8s1.5-4.5 4-3.8C18.5 5 16.5 8 12 8z"/>',
    "printer": '<path d="M7 8V3h10v5"/><rect x="3" y="8" width="18" height="9" rx="2"/><path d="M7 14h10v7H7z"/>',
    "share": '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.2 10.8 7.6-3.6M8.2 13.2l7.6 3.6"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.5v.1"/>',
    "door": '<path d="M5 21V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v17M3 21h18"/><circle cx="15.5" cy="12" r=".8"/>',
    "sewer": '<circle cx="12" cy="12" r="8.5"/><path d="M5 9.5h14M5 14.5h14M9.5 5v14M14.5 5v14"/>',
    "thermo": '<path d="M10 14.5V4.5a2 2 0 0 1 4 0v10a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
    "lightning": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
}


def icon(name, cls="i", size=None):
    inner = P.get(name, P["info"])
    style = f' width="{size}" height="{size}"' if size else ""
    return f'<svg class="{cls}" viewBox="0 0 24 24"{style} aria-hidden="true" focusable="false">{inner}</svg>'


LOGO = (
    '<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
    '<rect width="40" height="40" rx="11" fill="#0B1B2B"/>'
    '<circle cx="18" cy="18" r="10" fill="none" stroke="#FFB703" stroke-width="3.2"/>'
    '<path d="M25.5 25.5 32 32" stroke="#FFB703" stroke-width="3.6" stroke-linecap="round"/>'
    '<path d="M19.6 10.5 13.8 19h4.4l-1.6 7.5 6.2-9.2h-4.5z" fill="#fff"/>'
    "</svg>"
)
