import random
import traceback

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
)
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivy.core.audio import SoundLoader

from kivymd.app import MDApp

import arabic_reshaper
from bidi.algorithm import get_display

from songs import songs_list

def fix_arabic(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(str(text)))
    
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

    app_title = StringProperty("")
    current_song_title = StringProperty("")
    current_lyrics = StringProperty("")
    current_poster = StringProperty("default_poster.png")
    next_song_preview = StringProperty("")
    smart_mood_tag = StringProperty("")
    time_label = StringProperty("00:00 / 00:00")

    song_length = NumericProperty(0)
    song_position = NumericProperty(0)

    image_angle = NumericProperty(0)

    is_playing = BooleanProperty(False)
    is_player_ready = BooleanProperty(False)
    repeat_mode = BooleanProperty(False)
    shuffle_mode = BooleanProperty(False)
    is_favorite = BooleanProperty(False)
    
    def build(self):

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.app_title = fix_arabic("موسوعة الأغاني السودانية")

        self.current_index = 0

        self.sound = None

        self.progress_event = None

        self.songs_list = songs_list
        self.displayed_songs = songs_list.copy()

        return Builder.load_file("main.kv")
    
    def on_start(self):

        self.load_songs_menu()
        self.update_next_preview()

        Clock.schedule_once(self.switch_to_main, 2.5)


    def switch_to_main(self, dt):
        self.root.current = "list_screen"


    def format_time(self, seconds):

        seconds = int(max(0, seconds))

        m = seconds // 60
        s = seconds % 60

        return f"{m:02d}:{s:02d}"


    def update_next_preview(self):

        if not self.songs_list:
            self.next_song_preview = ""
            return

        if self.shuffle_mode:
            self.next_song_preview = fix_arabic("تشغيل عشوائي")
            return

        index = (self.current_index + 1) % len(self.songs_list)

        self.next_song_preview = fix_arabic(
            self.songs_list[index]["title"]
        )
        
    def play_current(self):

       song = self.songs_list[self.current_index]

       self.current_song_title = fix_arabic(song["title"])
       self.current_lyrics = fix_arabic(song["lyrics"])
       self.current_poster = song["poster"]
       self.smart_mood_tag = fix_arabic(song["mood"])
       self.is_favorite = song["fav"]

       if self.sound:
           self.sound.stop()

       self.sound = SoundLoader.load(song["file"])
       
       if self.sound:
           
           self.sound.play()

           self.is_playing = True
           self.is_player_ready = True

           self.song_position = 0

       if self.sound and self.sound.length:
           self.song_length = int(self.sound.length)
       else:
           self.song_length = 0

       self.update_next_preview()

       if self.progress_event:
           self.progress_event.cancel()

       self.progress_event = Clock.schedule_interval(
       self.update_progress,
       0.5,
       )
     
    def update_progress(self, dt):
        
        if not self.sound:
            return

        pos = self.sound.get_pos()

        if pos < 0:
            return

        self.song_position = pos

        self.time_label = (
            f"{self.format_time(pos)} / "
            f"{self.format_time(self.song_length)}"
        )

        if (
            self.song_length > 0
            and pos >= self.song_length - 1
        ):

            if self.repeat_mode:

                self.play_current()

            else:

                self.next_song()
     
    def toggle_play(self):
        
        if not self.sound:
            
            self.play_current()
            return

        if self.is_playing:

            self.sound.stop()
            self.is_playing = False

        else:

            self.play_current()
     
    def next_song(self):
        
        if not self.songs_list:
            return

        if self.shuffle_mode:
            
            self.current_index = random.randint(
            0,
            len(self.songs_list) - 1
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
     
    def seek_song(self, value):
        if not self.sound:
            return

        try:
            
            self.sound.seek(float(value))
           
            self.song_position = value

        except Exception:
            
            pass
     
    def toggle_repeat(self):
        
        self.repeat_mode = not self.repeat_mode
     
    def toggle_shuffle(self):
        
        self.shuffle_mode = not self.shuffle_mode

        self.update_next_preview()
     
    def toggle_favorite(self):
        
        song = self.songs_list[self.current_index]

        song["fav"] = not song["fav"]

        self.is_favorite = song["fav"]

        self.load_favorite_menu()
     
     
     
    def filter_songs(self, query):
        
        query = query.strip().lower()

        if query == "":
            
            self.displayed_songs = self.songs_list.copy()

        else:

            self.displayed_songs = [

            song

            for song in self.songs_list

            if query in song["title"].lower()

            ]

        self.load_songs_menu()
     
    def select_song_by_title(self, title):
        
        for i, song in enumerate(self.songs_list):
            
            if song["title"] == title:
                
                self.current_index = i

                break

        self.play_current()

        self.root.current = "player_screen"
     
    def load_songs_menu(self):
        
        from kivymd.uix.list import OneLineAvatarIconListItem
        from kivymd.uix.list import IconRightWidget

        container = self.root.get_screen(
        "list_screen"
        ).ids.songs_container

        container.clear_widgets()

        for song in self.displayed_songs:
            
            item = OneLineAvatarIconListItem(
            text=fix_arabic(song["title"])
            )

            item.add_widget(
                 IconRightWidget(
                      icon="music-circle"
                 )
            )
            
            item.bind(
            on_release=lambda x, t=song["title"]:
                self.select_song_by_title(t)
                )

            container.add_widget(item)
     
    def load_favorite_menu(self):
        
         from kivymd.uix.list import OneLineAvatarIconListItem
         from kivymd.uix.list import IconRightWidget

         container = self.root.get_screen(
         "favorite_screen"
         ).ids.fav_songs_container

         container.clear_widgets()

         for song in self.songs_list:
             
             if not song["fav"]:
                 continue

             item = OneLineAvatarIconListItem(
             text=fix_arabic(song["title"])
             )

             item.add_widget(
             IconRightWidget(
             icon="heart"
             )
             )

             item.bind(
             on_release=lambda x, t=song["title"]:
             self.select_song_by_title(t)
             )

             container.add_widget(item)
     
    def set_sleep_timer(self):
        
        Clock.schedule_once(
        self.trigger_sleep,
        600,
        )


    def trigger_sleep(self, dt):
        
        if self.sound:
            
            self.sound.stop()

        self.is_playing = False
     
     
    def share_app(self):
        
        if platform != "android":
            return

        try:
            
            from jnius import autoclass

            Intent = autoclass(
            "android.content.Intent"
            )

            PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            intent = Intent(
            Intent.ACTION_SEND
            )

            intent.setType("text/plain")

            intent.putExtra(
            Intent.EXTRA_TEXT,
            "تطبيق أغاني دارفور"
            )

            chooser = Intent.createChooser(
            intent,
            "مشاركة"
            )

            activity.startActivity(
            chooser
            )

        except Exception:

            traceback.print_exc()
     
    def on_stop(self):
        
        if self.sound:
            
            self.sound.stop()
     
if __name__ == "__main__":
    NaderKhadrApp().run() 