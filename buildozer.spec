[app]

title = أغاني دارفور

package.name = darfursongs
package.domain = org.mahdi

source.dir = .
source.include_exts = py,kv,png,mp3

version = 1.0

requirements = python3,kivy==2.2.1,kivymd==1.2.0,pillow,python-bidi,pyjnius,legacy-cgi, setuptools

orientation = portrait
fullscreen = 0

icon.filename = icon.png
presplash.filename = icon.png

android.api = 33
android.minapi = 24
android.ndk = 25b
#android.ndk_api = 24

android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET,WAKE_LOCK

android.accept_sdk_license = True
android.enable_androidx = True
android.allow_backup = True

log_level = 2

[buildozer]

warn_on_root = 1
