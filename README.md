# 🎵 أغاني دارفور

تطبيق أندرويد مبني باستخدام Python + KivyMD.

## المميزات

- 🎵 تشغيل الأغاني
- ❤️ المفضلة
- 🔀 تشغيل عشوائي
- 🔁 تكرار
- ⏭️ التالي والسابق
- 🌙 مؤقت النوم
- 📱 تصميم Material Design

## المتطلبات

- Python 3.11
- Kivy 2.3.0
- KivyMD 1.2.0
- Buildozer

## البناء محليًا

```bash
buildozer android debug
```

## البناء بواسطة GitHub Actions

ارفع المشروع إلى GitHub ثم افتح:

```
Actions
```

وشغّل:

```
Build Android APK
```

بعد انتهاء البناء ستجد ملف APK داخل:

```
Artifacts
```

## هيكل المشروع

```
.
├── main.py
├── main.kv
├── songs.py
├── player.py
├── buildozer.spec
├── icon.png
├── default_poster.png
├── mahdi.png
├── 50.mp3
├── 51.mp3
├── 52.mp3
├── 53.mp3
├── 54.mp3
└── .github/workflows/android.yml
```
