import os
import argparse
from datetime import timedelta
from moviepy.editor import VideoFileClip
import whisper

def extract_audio(video, temp_file):
    if video.audio is not None:
        video.audio.write_audiofile(temp_file, codec="mp3")
    else:
        raise ValueError("Video has no audio.")

def generate_subtitles(srt_name, transcribe_segments, temp_file):
    print('[i] Generating SRT...')
    with open(srt_name, "w", encoding="utf-8") as f:
        for segment_id, seg in enumerate(transcribe_segments, start=1):
            start = format_time(seg["start"])
            end = format_time(seg["end"])
            text = seg["text"].lstrip()
            f.write(f"{segment_id}\n{start} --> {end}\n{text}\n\n")
    try:
        os.remove(temp_file)
    except FileNotFoundError:
        print(f"Warning: Temporary MP3 file '{temp_file}' could not be found for deletion.")

def format_time(seconds):
    return str(timedelta(seconds=int(seconds))) + ",000"

def main():
    parser = argparse.ArgumentParser(description="auto caption generator v1.0")
    parser.add_argument("-f", "--video-path", type=str, required=True, help="Filepath of the video")
    parser.add_argument("--model", choices=["tiny", "base", "small", "medium", "large"], default="tiny", help="Choose the whisper model size (default: tiny)")
    args = parser.parse_args()
    path = args.video_path

    try:
        validate_path(path)
        video_manager = VideoFileClip(path)
        file_name, file_extension = os.path.splitext(os.path.basename(path))
        temp_file = f"{file_name}_temp_for_srt.mp3"
        srt_name = f"{file_name}.srt"
        with video_manager:
            extract_audio(video_manager, temp_file)
            model = whisper.load_model(args.model)
            transcribe = model.transcribe(audio=temp_file, fp16=False)
            print('[i] Transcription finished.')
            generate_subtitles(srt_name, transcribe["segments"], temp_file)
    except FileNotFoundError:
        print(f"Error: Temporary file '{temp_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def validate_path(path):
    if not os.path.exists(path):
        raise ValueError("Invalid file path, quitting")

if __name__ == "__main__":
    main()
