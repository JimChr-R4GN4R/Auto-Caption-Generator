# Auto Caption Generator

This Python script leverages the `openai-whisper` model to automatically generate captions for a given video file. The generated captions are saved in SubRip (SRT) format, allowing easy integration with video players.

## Prerequisites

Before running the script, make sure you have the following installed:

- [MoviePy](https://zulko.github.io/moviepy/)
- [OpenAI-Whisper]([https://whisper.ai/](https://pypi.org/project/openai-whisper/))
- [FFmpeg](https://www.ffmpeg.org/)

## How to use it

```bash
python auto_caption_generator.py -f /path/to/your/video.mp4 --model <model_size>
```

-  `-f` or `--video-path`: Filepath of the video.
-  `--model`: Choose the Whisper model size (tiny, base, small, medium, large). Default is tiny.

## Output
The script will generate an SRT file with the same name as the input video file. The SRT file will be saved in the same directory as the script.

## Notes
- The script requires the input video to have an audio track.
- Temporary MP3 files are created during the process and are deleted upon completion.
