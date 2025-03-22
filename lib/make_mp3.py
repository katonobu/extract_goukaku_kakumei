import os
import tempfile
try:
    import pyttsx3
except ModuleNotFoundError as e:
    pyttsx3 = None

from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK

class MakeMp3():
    def __init__(self):
        pass

    def init(self, base_dir, dry_run = False):
        self.track_count = 1
        self.dry_run = pyttsx3 is None or dry_run
        if self.dry_run == False:
            self.engine = pyttsx3.init()
        else:
            self.engine = None
            print("MakeMp3() is initialized with dry_ryn mode.")
        self.dir_path = base_dir
        os.makedirs(self.dir_path, exist_ok=True)

    def mp3_tts(self, file_name, texts1, mute_msec, texts2, title, artist_name, album_name, rate=200):
        mp3_file_path = os.path.join(self.dir_path, file_name)
        if self.dry_run == False:
            with tempfile.TemporaryDirectory() as td:
                print(f'  Generating {title}')

                wav_file1 = os.path.join(td, "tmp1.wav")
                self.engine.setProperty('rate', rate)
                self.engine.save_to_file("\n".join(texts1), wav_file1)
                self.engine.runAndWait()
                text_audio_1 = AudioSegment.from_mp3(wav_file1)
                combined = text_audio_1

                if 0 < mute_msec:
                    mute_data = AudioSegment.silent(duration=mute_msec)
                    combined += mute_data

                if texts2 is not None:
                    wav_file2 = os.path.join(td, "tmp2.wav")
                    self.engine.setProperty('rate', rate)
                    self.engine.save_to_file("\n".join(texts2), wav_file2)
                    self.engine.runAndWait()
                    text_audio_2 = AudioSegment.from_mp3(wav_file2)
                    combined += text_audio_2

                combined.export(mp3_file_path, format='mp3')

                # タグを設定
                audio = MP3(mp3_file_path, ID3=ID3)
                if rate != 200:
                    baisoku = rate/200
                    audio.tags.add(TIT2(encoding=3, text=f"{title} {baisoku:1.1f}倍速"))  # 曲名
                else:
                    audio.tags.add(TIT2(encoding=3, text=title))  # 曲名

                audio.tags.add(TPE1(encoding=3, text=artist_name))  # アーティスト
                audio.tags.add(TALB(encoding=3, text=album_name))  # アルバム
                audio.tags.add(TRCK(encoding=3, text=f"{self.track_count}"))            # トラック番号
                audio.save()                
                self.track_count += 1
        else:
            total_texts = texts1
            if texts2 is not None:
                total_texts += texts2
            with open(mp3_file_path.replace(".mp3",".txt"), "w", encoding='utf-8') as f:
                f.write('\n'.join(total_texts))
            print(f'  Generating {title}(dry_run), {len(total_texts)} lines')
    
    def finish(self):
        print("Finish MakeMp3().")
        if self.dry_run == False:
            self.engine.stop()
            self.engine = None


if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__),"mp3")
    mk_mp3 = MakeMp3(base_dir)