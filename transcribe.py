#!/usr/bin/env python3
"""
Transcribe a video ad and pull frames for on-screen text.

usage: python3 transcribe.py <video.mp4> [--frames 0.5,3,10]
Writes next to the video:  <name>.txt (transcript), <name>-frame-<t>.jpg (frames)

Transcription backends, tried in order:
  1. local `whisper` CLI (pip3 install openai-whisper)
  2. OpenAI API (OPENAI_API_KEY in env or ~/.claude/ad-profiles/.env)
Requires ffmpeg on PATH (brew install ffmpeg).
"""
import argparse, json, os, shutil, subprocess, sys, urllib.request
from pathlib import Path

def load_env():
    p = Path.home() / ".claude" / "ad-profiles" / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"'))

def ffmpeg():
    for c in ("ffmpeg", "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if shutil.which(c) or Path(c).exists(): return c
    sys.exit("ffmpeg not found. Install: brew install ffmpeg (Mac) or sudo apt install ffmpeg (Linux)")

def whisper_cli():
    for c in ("whisper", str(Path.home() / "Library/Python/3.9/bin/whisper"), str(Path.home() / ".local/bin/whisper")):
        if shutil.which(c) or Path(c).exists(): return c
    return None

def transcribe_local(cli, wav, outdir):
    subprocess.run([cli, str(wav), "--model", "base", "--output_format", "txt", "--output_dir", str(outdir), "--fp16", "False"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return (outdir / (wav.stem + ".txt")).read_text().strip()

def transcribe_api(wav):
    key = os.environ.get("OPENAI_API_KEY")
    if not key: return None
    boundary = "----adspy"
    data = wav.read_bytes()
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nwhisper-1\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{wav.name}\"\r\nContent-Type: audio/wav\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request("https://api.openai.com/v1/audio/transcriptions", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())["text"].strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--frames", default="0.5,3,10")
    a = ap.parse_args(); load_env()
    v = Path(a.video); outdir = v.parent; ff = ffmpeg()
    wav = outdir / (v.stem + ".wav")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(v), "-vn", "-ar", "16000", "-ac", "1", str(wav)], check=True)
    for t in a.frames.split(","):
        subprocess.run([ff, "-y", "-loglevel", "error", "-ss", t, "-i", str(v), "-frames:v", "1", "-vf", "scale=480:-1",
                        str(outdir / f"{v.stem}-frame-{t}.jpg")], check=True)
    text = None
    cli = whisper_cli()
    if cli:
        try: text = transcribe_local(cli, wav, outdir)
        except Exception: text = None
    if text is None: text = transcribe_api(wav)
    if text is None:
        sys.exit("No transcription backend. Install local whisper (pip3 install openai-whisper) or add OPENAI_API_KEY to ~/.claude/ad-profiles/.env")
    (outdir / (v.stem + ".txt")).write_text(text + "\n")
    wav.unlink(missing_ok=True)
    print(outdir / (v.stem + ".txt"))

if __name__ == "__main__":
    main()
