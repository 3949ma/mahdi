[app]

title = أغاني مريم أمو

package.name = amosongs

package.domain = org.mahdi

source.dir = .

source.include_exts = py,kv,png,jpg,jpeg,ttf,mp3,json

version = 1.0

orientation = portrait

fullscreen = 0

android.api = 33

android.minapi = 23

android.ndk = 25b

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,arabic-reshaper,python-bidi,pyjnius
android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET,WAKE_LOCK

android.accept_sdk_license = True

p4a.fork = kivy

p4a.branch = develop

log_level = 2

warn_on_root = 1


[buildozer]

log_level = 2

warn_on_root = 1