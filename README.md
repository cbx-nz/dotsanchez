# .sanchez Video Format

**Interdimensional Cable Video Format** - A custom video format inspired by Rick & Morty

> "Nobody exists on purpose. Nobody belongs anywhere. Everybody's gonna die. Come watch TV." - Morty

## Overview

The `.sanchez` format is a simple, human-readable video/image format where each pixel is stored as RGB hex values. This implementation includes zlib compression to reduce file sizes from ~14.5MB per frame to typically <1MB per frame.

### Format Specification

```
Line 1: Metadata (JSON, one line)
Line 2: Config (WWWWHHHH + 7-digit frame count)
Line 3+: Frame data (compressed or hex pixels)
```

**Example:**
```
{"title":"MyVideo","creator":"cbx","created_at":"2026-01-02T01:30:43Z","seconds":"2.0"}
03200240000048
eJzLzklMT8...base64 compressed data...
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Also need ffmpeg for audio extraction/muxing
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

## Usage

### Command Line

```bash
# Encode video to .sanchez
python -m sanchez encode video.mp4 output.sanchez

# Encode with resize
python -m sanchez encode video.mp4 -r 640x480

# Encode image to .sanchez
python -m sanchez encode image.png output.sanchez

# Decode .sanchez to MP4
python -m sanchez decode input.sanchez output.mp4

# Decode with audio
python -m sanchez decode input.sanchez -a audio.mp3

# Extract single frame
python -m sanchez decode input.sanchez -f 0 -o frame.png

# Extract all frames
python -m sanchez decode input.sanchez --frames

# Play .sanchez file
python -m sanchez play video.sanchez

# Show file info
python -m sanchez info video.sanchez
```

### Python API

```python
from sanchez import SanchezFile, SanchezEncoder, SanchezDecoder, SanchezPlayer

# Encode a video
encoder = SanchezEncoder()
encoder.encode("input.mp4", "output.sanchez", title="My Video", creator="cbx")

# Decode back to MP4
decoder = SanchezDecoder()
decoder.decode("output.sanchez", "decoded.mp4", audio_path="output.mp3")

# Play a .sanchez file
player = SanchezPlayer()
player.play("output.sanchez")

# Create .sanchez from scratch
import numpy as np

sanchez = SanchezFile.create("MyVideo", "cbx", width=320, height=240)
frame = np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)
sanchez.add_frame(frame)
sanchez.save("custom.sanchez")

# Read .sanchez file
sanchez = SanchezFile.load("custom.sanchez")
for frame in sanchez.get_frames():
    # Process frame (numpy array)
    pass
```

## Player Controls

When playing with `python -m sanchez play`:

| Key | Action |
|-----|--------|
| Space | Pause/Resume |
| Left Arrow | Seek backward 5 seconds |
| Right Arrow | Seek forward 5 seconds |
| , | Previous frame (when paused) |
| . | Next frame (when paused) |
| R | Restart |
| I | Toggle info overlay |
| F | Toggle fullscreen |
| Q / Esc | Quit |

## Compression

The format uses zlib compression with base64 encoding to store frame data efficiently:

- **Uncompressed**: ~6.2 MB per 1920x1080 frame (raw RGB bytes)
- **Compressed**: Typically 0.5-2 MB per frame depending on content
- Compression ratio: 3-10x typical

For maximum compatibility with the original spec (hex per pixel), use `--no-compression` flag, but note this creates much larger files.

## File Structure

### Metadata (Line 1)
```json
{"title":"Example","creator":"cbx","created_at":"2026-01-02T01:30:43Z","seconds":"2.0"}
```

### Config (Line 2)
```
WWWWHHHH + FFFFFFF
```
- WWWW: Width (4 digits, zero-padded)
- HHHH: Height (4 digits, zero-padded)  
- FFFFFFF: Frame count (7 digits, zero-padded)

Example: `192010800000048` = 1920x1080, 48 frames

### Frame Data (Lines 3+)
Each line is one frame, either:
- **Compressed**: Base64-encoded zlib-compressed RGB bytes
- **Uncompressed**: `{RRGGBB,RRGGBB,...}` hex format

## Audio

Audio is stored as a separate `.mp3` file with the same name as the `.sanchez` file. When encoding from MP4, audio is automatically extracted. When decoding, audio is automatically detected and muxed if `ffmpeg` is available.

## Example

Run the example script to see the format in action:

```bash
python example.py
```

This creates a test pattern video, saves it as `.sanchez`, reads info, extracts a frame, and decodes it back to MP4.

---

*Get schwifty!* 🛸
