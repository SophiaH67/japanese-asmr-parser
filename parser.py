from requests_html import HTMLSession  

class JapaneseAsmr:
  headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8",
    "range": "bytes=1572864-",
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
  
  @property
  def title(self):
    return self.html.find('title', first=True).text.replace(' – Japanese ASMR', '')
  
  @property
  def image(self):
    return self.html.find('img.fotorama__img')[-2].attrs['src']
  
  @property
  def audio(self):
    return self.html.find('audio > source')[0].attrs['src']
  
  def _download_thing(self, thing, path):
    with self.session.get(thing, headers=self.headers, stream=True) as thing_stream:
      with open(path, 'wb') as f:
        for chunk in thing_stream.iter_content(chunk_size=1024):
          f.write(chunk)
  
  def download_audio(self, path):
    self._download_thing(self.audio, path)
  
  def download_image(self, path):
    self._download_thing(self.image, path)

  
    