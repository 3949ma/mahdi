import os
import random
import traceback
import json

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
)
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from kivy.core.audio import SoundLoader

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import (
    MDFlatButton,
    MDRaisedButton,
    MDIconButton,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

import arabic_reshaper
from bidi.algorithm import get_display


def fix_arabic(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(str(text)))


# استخدام خط النظام الافتراضي مباشرة لتفادي مشاكل التحميل
FONT_NAME = "Roboto"
# الاعتماد على خط النظام الافتراضي مباشرة وتجاوز كتلة التسجيل
FONT_NAME = "Roboto"
    

class SplashScreen(Screen):
    pass


class ListScreen(Screen):
    pass


class PlayerScreen(Screen):
    pass


class FavoriteScreen(Screen):
    pass


class DeveloperScreen(Screen):
    pass


class NaderKhadrApp(MDApp):

    # تعريف المتغيرات كنصوص عادية، وسيتم تشفيرها باللغة العربية داخل دالة build الآمنة
    app_title = StringProperty("")
    current_song_title = StringProperty("")
    current_lyrics = StringProperty("")
    current_poster = StringProperty("default_poster.png")

    time_label = StringProperty("00:00 / 00:00")
    next_song_preview = StringProperty("")
    smart_mood_tag = StringProperty("")

    song_length = NumericProperty(100)
    song_position = NumericProperty(0)

    image_angle = NumericProperty(0)

    is_playing = BooleanProperty(False)
    is_favorite = BooleanProperty(False)
    repeat_mode = BooleanProperty(False)
    shuffle_mode = BooleanProperty(False)
    sleep_timer_active = BooleanProperty(False)
    is_player_ready = BooleanProperty(False)

    def build(self):
        # تطبيق دالة fix_arabic هنا بشكل آمن تماماً بعد تهيئة التطبيق
        self.app_title = fix_arabic("موسوعة الأغاني السودانية")
        self.current_song_title = fix_arabic("اختر أغنية")

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        self.sound = None
        self.player = None
        self.current_index = 0
        self.updating_track = None
        self.timer_dialog = None

        self.songs_list = []
        self.displayed_songs = []

        return Builder.load_file("main.kv")

    def on_start(self):
        self.songs_list = [
            {
                "title": "دالدومينق كو تراث دارفور",
                "file": "50.mp3",
                "poster": "default_poster.png",
                "lyrics": "دالدومينق كو",
                "mood": "تراث أصيل",
                "fav": False,
            },
            {
                "title": "شرطاي سكيو",
                "file": "51.mp3",
                "poster": "default_poster.png",
                "lyrics": "شرطاي سكيو",
                "mood": "تراث أصيل",
                "fav": False,
            },
            {
                "title": "كيلمانقا بقي",
                "file": "52.mp3",
                "poster": "default_poster.png",
                "lyrics": "كيلمانقا بقي",
                "mood": "تراث أصيل",
                "fav": False,
            },
            {
                "title": "ناس دارفور كفاية المعاناة",
                "file": "53.mp3",
                "poster": "default_poster.png",
                "lyrics": "ناس دارفور كفاية المعاناة",
                "mood": "رسالة إنسانية",
                "fav": False,
            },
            {
                "title": "من أعلى مكان شفت أبعد مكان",
                "file": "54.mp3",
                "poster": "default_poster.png",
                "lyrics": "من أعلى مكان شفت أبعد مكان",
                "mood": "روائع مريم أمو",
                "fav": False,
            },
        ]
        self.load_favorites()
        self.displayed_songs = self.songs_list.copy()

        self.load_songs_menu()
        self.update_next_preview()

        Clock.schedule_once(self.switch_to_main, 2.5)
        
       
    def switch_to_main(self, dt):
        self.root.current = "list_screen"

    def format_time(self, seconds):
        seconds = max(0, int(seconds))
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02d}:{seconds:02d}"

    def update_next_preview(self):
        if not self.songs_list:
            self.next_song_preview = ""
            return

        if self.shuffle_mode:
            self.next_song_preview = fix_arabic("التالي: تشغيل عشوائي")
        else:
            next_index = (self.current_index + 1) % len(self.songs_list)
            self.next_song_preview = fix_arabic(
                self.songs_list[next_index]["title"]
            )
            
    def load_songs_menu(self):
        from kivymd.uix.list import (
            OneLineAvatarIconListItem,
            IconRightWidget,
        )
        from functools import partial  # استيراد أداة الربط الصحيح

        container = self.root.get_screen(
            "list_screen"
        ).ids.songs_container

        container.clear_widgets()

        for song in self.displayed_songs:

            item = OneLineAvatarIconListItem(
                text=fix_arabic(song["title"])
            )

            item.add_widget(
                IconRightWidget(icon="music-circle")
            )

            # الربط الآمن لكل أغنية لمنع التكرار والخلط
            item.bind(
                on_release=partial(lambda title, instance: self.select_song_by_title(title), song["title"])
            )

            container.add_widget(item)

    def select_song_by_title(self, title):

        for index, song in enumerate(self.songs_list):
            if song["title"] == title:
                self.current_index = index
                break

        self.play_current()
        self.root.current = "player_screen"
      
      
    def play_current(self):

        if self.sound:
            self.sound.stop()

        song = self.songs_list[self.current_index]

        filepath = song["file"]
        
        if not os.path.exists(filepath):
            self.current_song_title = fix_arabic("ملف الأغنية غير موجود")
            return

        self.sound = SoundLoader.load(filepath)
        self.current_song_title = fix_arabic(song["title"])
        self.current_lyrics = fix_arabic(song["lyrics"])

        if os.path.exists(song["poster"]):
            self.current_poster = song["poster"]
        else:
            self.current_poster = "default_poster.png"

        self.smart_mood_tag = fix_arabic(song["mood"])
        self.is_favorite = song["fav"]

        self.song_position = 0
        self.is_playing = True
        self.is_player_ready = True

        self.update_next_preview()

        if self.updating_track:
            self.updating_track.cancel()

        self.updating_track = Clock.schedule_interval(
            self.update_progress,
            1,
        )

        if self.sound:
            self.sound.play()
            self.song_length = int(self.sound.length)
        else:
            self.song_length = 0

    def update_progress(self, dt):

        if not self.is_playing:
            return

        if self.sound:
            
            pos = self.sound.get_pos()
           
            if pos >= 0:
                self.song_position = int(pos)

        if self.song_position > self.song_length:
            self.song_position = self.song_length

        self.time_label = (
            f"{self.format_time(self.song_position)} / "
            f"{self.format_time(self.song_length)}"
        )

        if self.song_position >= self.song_length:
            if self.repeat_mode:
                self.song_position = 0
            else:
                self.next_song()
      
      
    def next_song(self):

        if not self.songs_list:
            return

        if self.shuffle_mode:
            self.current_index = random.randint(
                0,
                len(self.songs_list) - 1,
            )
        else:
            self.current_index = (
                self.current_index + 1
            ) % len(self.songs_list)

        self.play_current()

    def previous_song(self):

        if not self.songs_list:
            return

        self.current_index = (
            self.current_index - 1
        ) % len(self.songs_list)

        self.play_current()

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        self.update_next_preview()

    def toggle_play(self):
        if not self.sound:
            self.play_current()
            return

        if self.is_playing:
            self.sound.stop()
            self.is_playing = False
        else:
            self.sound.play()
            self.is_playing = True
            
    def stop_song(self):
        if self.sound:
            self.sound.stop()

        self.is_playing = False
        self.song_position = 0
        self.time_label = "00:00 / 00:00"

        if self.updating_track:
            self.updating_track.cancel()
            self.updating_track = None
        
    def seek_song(self, value):

        self.song_position = int(value)

        self.time_label = (
            f"{self.format_time(self.song_position)} / "
            f"{self.format_time(self.song_length)}"
        )


    def filter_songs(self, query):

        query = query.strip().lower()

        if not query:
            self.displayed_songs = self.songs_list.copy()
        else:
            self.displayed_songs = [
                song
                for song in self.songs_list
                if query in song["title"].lower()
            ]

        self.load_songs_menu()

    def toggle_favorite(self):

        if not self.songs_list:
            return

        song = self.songs_list[self.current_index]

        song["fav"] = not song["fav"]
        self.save_favorites()
        self.is_favorite = song["fav"]

        self.load_songs_menu()
        self.load_favorite_menu()

    def save_favorites(self):
        with open("favorites.json","w",encoding="utf8") as f:
            json.dump(self.songs_list,f,ensure_ascii=False)

    def load_favorites(self):
        if os.path.exists("favorites.json"):
            try:
                with open("favorites.json", "r", encoding="utf8") as f:
                    self.songs_list = json.load(f)
            except Exception:
                pass

    def load_favorite_menu(self):

        from kivymd.uix.list import (
            OneLineAvatarIconListItem,
            IconRightWidget,
        )
        from functools import partial

        container = self.root.get_screen(
            "favorite_screen"
        ).ids.fav_songs_container

        container.clear_widgets()

        favorites = [
            song
            for song in self.songs_list
            if song["fav"]
        ]

        for song in favorites:

            item = OneLineAvatarIconListItem(
                text=fix_arabic(song["title"])
            )

            item.add_widget(
                IconRightWidget(icon="heart")
            )

            # تطبيق الربط الآمن في قائمة المفضلة أيضاً
            item.bind(
                on_release=partial(lambda title, instance: self.select_song_by_title(title), song["title"])
            )

            container.add_widget(item)

    def set_sleep_timer(self):

        self.sleep_timer_active = not self.sleep_timer_active

        if self.sleep_timer_active:
            Clock.schedule_once(
                self.trigger_sleep,
                600,
            )

    def trigger_sleep(self, dt):

        self.sleep_timer_active = False

        self.stop_song()

        self.current_song_title = fix_arabic(
            "تم إيقاف التشغيل بواسطة مؤقت النوم"
        )

    def share_app(self):

        if platform != "android":
            return

        try:
            from jnius import autoclass

            Intent = autoclass("android.content.Intent")
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")

            intent.putExtra(
                Intent.EXTRA_TEXT,
                "موسوعة الأغاني السودانية"
            )

            chooser = Intent.createChooser(
                intent,
                "مشاركة التطبيق"
            )

            activity.startActivity(chooser)

        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    NaderKhadrApp().run()
