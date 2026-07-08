[app]

title = أغاني دارفور
package.name = darfursongs
package.domain = org.mahdi

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,mp3

version = 1.0

requirements = python3,kivy==2.3.0,kivymd,pillow,ffpyplayer,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

icon.filename = icon.png
presplash.filename = icon.png

android.api = 33
android.minapi = 24
android.ndk = 25b

android.archs = arm64-v8a

android.permissions = INTERNET,WAKE_LOCK

android.accept_sdk_license = True
android.enable_androidx = True
android.allow_backup = True

log_level = 2

[buildozer]

warn_on_root = 1
