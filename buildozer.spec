[app]

title = أغاني دارفور

package.name = darfursongs
package.domain = org.mahdi

source.dir = .
source.include_exts = py,kv,png,ttf,mp3

version = 1.0

requirements = python3,kivy==master,kivymd==1.2.0,pillow,arabic-reshaper,python-bidi,pyjnius

orientation = portrait

fullscreen = 0

icon.filename = icon.png

presplash.filename = icon.png

android.ndk_api = 24
android.minapi = 24
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET,WAKE_LOCK

android.accept_sdk_license = True

android.enable_androidx = True

android.allow_backup = True

p4a.branch = master

log_level = 2

[buildozer]

warn_on_root = 1
