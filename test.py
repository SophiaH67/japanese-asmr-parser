from parser import JapaneseAsmr

japanese_asmr = JapaneseAsmr("https://japaneseasmr.com/60063/")

print(f"Title: {japanese_asmr.title} audio: {japanese_asmr.audio} image: {japanese_asmr.image}")
japanese_asmr.download_audio("test.mp3")