from kivy.core.audio import SoundLoader


class AudioPlayer:
    def __init__(self):
        self.sound = None
        self.current_file = None

    def load(self, filename):
        self.stop()

        self.current_file = filename
        self.sound = SoundLoader.load(filename)

        if self.sound:
            self.sound.volume = 1.0

        return self.sound

    def play(self):
        if self.sound:
            self.sound.play()

    def pause(self):
        if self.sound:
            try:
                self.sound.stop()
            except Exception:
                pass

    def stop(self):
        if self.sound:
            try:
                self.sound.stop()
            except Exception:
                pass
            self.sound = None

    def is_loaded(self):
        return self.sound is not None

    def get_length(self):
        if self.sound:
            try:
                return self.sound.length or 0
            except Exception:
                return 0
        return 0

    def get_position(self):
        if self.sound:
            try:
                return self.sound.get_pos()
            except Exception:
                return 0
        return 0

    def seek(self, position):
        if self.sound:
            try:
                self.sound.seek(position)
            except Exception:
                pass