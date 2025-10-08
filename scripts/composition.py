import ffmpeg
import os

def compose_video(bg_path, presenter_path, audio_path, output_path='final.mp4'):
    # Assume bg is looped to match length; simple overlay
    video = ffmpeg.input(bg_path)
    audio = ffmpeg.input(audio_path)
    presenter = ffmpeg.input(presenter_path)
    out = ffmpeg.output(
        video, presenter.overlay(ffmpeg.input('black.png', w=1920, h=1080).video),  # Corner overlay; add black.png if needed
        audio, output_path, vcodec='libx264', acodec='aac', shortest=None
    )
    ffmpeg.run(out)
    return output_path

def add_fades(input_path, output_path='faded.mp4'):
    ffmpeg.input(input_path).filter('fade', t='in', st=0, d=1).filter('fade', t='out', st=10, d=1).output(output_path).run()