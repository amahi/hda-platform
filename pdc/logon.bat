# Sync Windows clock with Samba clock
net time /set /yes
# Mount a samba share into x:
net use v: \\hda\pictures /persistent:no
net use w: \\hda\docs /persistent:no
net use x: \\hda\books /persistent:no
net use y: \\hda\movies /persistent:no
net use z: \\hda\music /persistent:no
