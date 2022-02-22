#!/usr/bin/env python
import click
from japanese_asmr.parser import JapaneseAsmr

@click.command()
@click.argument('url')
@click.argument('output', default="")
def main(url, output):
  japanese_asmr = JapaneseAsmr(url)
  print(f"Downloading {japanese_asmr.title}")
  japanese_asmr.render_video(output)

if __name__ == '__main__':
  main()