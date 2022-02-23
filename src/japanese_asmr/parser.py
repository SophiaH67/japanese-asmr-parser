from requests_html import HTMLSession  
from subprocess import run
from pathlib import Path
from random import randint
import threading

class JapaneseAsmr:
  headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "audio",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "Referer": "https://japaneseasmr.com/39993/",
    "Referrer-Policy": "no-referrer-when-downgrade"
  }

  def __init__(self, url):
    self.url = url
    
    self.session = HTMLSession()
    self.response = self.session.get(self.url)
    self.response.html.render()
    self.html = self.response.html
    self.headers["Referer"] = self.url

  @property
  def title(self):
    return self.html.find('title', first=True).text.replace(' – Japanese ASMR', '')

  @property
  def image(self):
    images = self.html.find('img.fotorama__img')
    if len(images) > 1:
      return images[-2].attrs['src']
    elif len(images) > 0:
      return images[0].attrs['src']
    else:
      return self.html.find('img.lazy', first=True).attrs['src']

  @property
  def audio(self):
    return [element.attrs['src'] for element in self.html.find('audio > source')]

  def _download_thing(self, thing, path):
    with self.session.get(thing, headers=self.headers, stream=True) as thing_stream:
      with open(path, 'wb') as f:
        for chunk in thing_stream.iter_content(chunk_size=1024):
          f.write(chunk)

  def download_audio(self, path):
    paths = []
    threads = []
    for i, audio in enumerate(self.audio):
      paths.append(f"{path[:-4]}.{i}.mp3")
      # self._download_thing(audio, paths[i])
      t = threading.Thread(target=self._download_thing, args=(audio, paths[i]))
      threads.append(t)
      t.daemon = True
      t.start()
    for t in threads:
      t.join()
    return paths

  def download_image(self, path):
    self._download_thing(self.image, path)

  def render_video(self, output=""):
    if output == "":
      output = self.title.replace('/', '_').replace('\\', '_')
    if output.endswith('/'):
      output += self.title.replace('/', '_').replace('\\', '_')
    if not output.endswith('.mp4'):
      output += '.mp4'

    audio_path = f"audio.{randint(1, 999999)}.tmp.mp3"
    image_path = f"image.{randint(1, 999999)}.tmp.jpg"

    audio_files = self.download_audio(audio_path)
    self.download_image(image_path)

    for i, audio_file in enumerate(audio_files):
      ffmpeg_command = f"ffmpeg -i {audio_file} -framerate 1 -loop 1 -i {image_path} -map 0:a -map 1:v -c:v libx264 -preset ultrafast -crf 30 -c:a copy -pix_fmt yuv420p -y -shortest \"{output[:-4]}.{i+1}.mp4\""
      run(ffmpeg_command, shell=True, check=True)
      Path(audio_file).unlink()

    Path(image_path).unlink()
