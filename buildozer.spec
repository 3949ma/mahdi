[app]

title = أغاني دارفور

package.name = darfursongs
package.domain = org.mahdi

source.dir = .
source.include_exts = py,kv,png,ttf,mp3

version = 1.0

requirements = python3==3.11.9,kivy==2.3.0,kivymd==1.2.0,pillow,arabic-reshaper,python-bidi,pyjnius

orientation = portrait

fullscreen = 0

icon.filename = icon.png

presplash.filename = icon.png

android.api = 33
android.minapi = 23
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET,WAKE_LOCK

android.accept_sdk_license = True

android.enable_androidx = True

android.allow_backup = True

log_level = 2

[buildozer]

warn_on_root = 1
