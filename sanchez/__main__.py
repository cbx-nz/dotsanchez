#!/usr/bin/env python3
"""
Sanchez CLI - Command-line interface for .sanchez video format

Interdimensional Cable Video Format for Rick & Morty

Usage:
    python -m sanchez encode <input.mp4> [output.sanchez] [options]
    python -m sanchez decode <input.sanchez> [output.mp4] [options]
    python -m sanchez play <input.sanchez> [options]
    python -m sanchez info <input.sanchez>
    python -m sanchez image <input.png> [output.sanchez]
"""

import argparse
import sys
from pathlib import Path


def cmd_encode(args):
    """Encode a video/image to .sanchez format"""
    from .encoder import SanchezEncoder
    
    encoder = SanchezEncoder()
    
    input_path = Path(args.input)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = str(input_path.with_suffix('.sanchez'))
    
    # Parse resize option
    resize = None
    if args.resize:
        parts = args.resize.lower().split('x')
        resize = (int(parts[0]), int(parts[1]))
    
    # Check if input is image or video
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}
    
    if input_path.suffix.lower() in image_extensions:
        encoder.encode_image(
            str(input_path),
            output_path,
            title=args.title,
            creator=args.creator,
            resize=resize
        )
    else:
        encoder.encode(
            str(input_path),
            output_path,
            title=args.title,
            creator=args.creator,
            resize=resize,
            max_frames=args.max_frames,
            use_compression=not args.no_compression
        )


def cmd_decode(args):
    """Decode a .sanchez file to video/image"""
    from .decoder import SanchezDecoder
    
    decoder = SanchezDecoder()
    
    input_path = Path(args.input)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = str(input_path.with_suffix('.mp4'))
    
    # Parse resize option
    resize = None
    if args.resize:
        parts = args.resize.lower().split('x')
        resize = (int(parts[0]), int(parts[1]))
    
    # Check if extracting to image or video
    if args.frame is not None:
        # Extract single frame as image
        if not args.output:
            output_path = str(input_path.with_suffix('.png'))
        decoder.decode_to_image(
            str(input_path),
            output_path,
            frame_index=args.frame,
            resize=resize
        )
    elif args.frames:
        # Extract all frames
        output_dir = args.output if args.output else str(input_path.with_suffix('')) + '_frames'
        decoder.extract_all_frames(
            str(input_path),
            output_dir,
            format=args.format or 'png',
            resize=resize
        )
    else:
        # Decode to video
        decoder.decode(
            str(input_path),
            output_path,
            audio_path=args.audio,
            resize=resize
        )


def cmd_play(args):
    """Play a .sanchez file"""
    from .player import SanchezPlayer, SimplePlayer
    
    if args.simple:
        player = SimplePlayer()
        player.view(args.input, frame_index=args.start_frame or 0)
    else:
        try:
            player = SanchezPlayer(scale=args.scale)
            player.play(
                args.input,
                audio_path=args.audio,
                start_frame=args.start_frame or 0,
                fullscreen=args.fullscreen
            )
        except ImportError:
            print("pygame not available, using simple viewer...")
            player = SimplePlayer()
            player.view(args.input, frame_index=args.start_frame or 0)


def cmd_info(args):
    """Show info about a .sanchez file"""
    from .decoder import SanchezDecoder
    
    decoder = SanchezDecoder()
    info = decoder.get_info(args.input)
    
    print(f"\n{'='*50}")
    print(f"  .sanchez File Info")
    print(f"{'='*50}")
    print(f"  Title:       {info['title']}")
    print(f"  Creator:     {info['creator']}")
    print(f"  Created:     {info['created_at']}")
    print(f"  Type:        {'Image' if info['is_image'] else 'Video'}")
    print(f"  Resolution:  {info['width']}x{info['height']}")
    print(f"  Frames:      {info['frame_count']}")
    print(f"  FPS:         {info['fps']}")
    print(f"  Duration:    {info['duration_seconds']:.2f} seconds")
    print(f"  File Size:   {info['file_size_mb']:.2f} MB")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Sanchez - Interdimensional Cable Video Format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encode video:     python -m sanchez encode video.mp4 output.sanchez
  Encode image:     python -m sanchez encode image.png output.sanchez
  Decode to video:  python -m sanchez decode input.sanchez output.mp4
  Extract frame:    python -m sanchez decode input.sanchez -f 0 -o frame.png
  Play video:       python -m sanchez play video.sanchez
  Get info:         python -m sanchez info video.sanchez

  Resize on encode: python -m sanchez encode video.mp4 -r 640x480
  With audio:       python -m sanchez decode video.sanchez -a video.mp3
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode video/image to .sanchez')
    encode_parser.add_argument('input', help='Input video or image file')
    encode_parser.add_argument('output', nargs='?', help='Output .sanchez file')
    encode_parser.add_argument('-t', '--title', help='Video title')
    encode_parser.add_argument('-c', '--creator', default='cbx', help='Creator name')
    encode_parser.add_argument('-r', '--resize', help='Resize to WxH (e.g., 1280x720)')
    encode_parser.add_argument('-m', '--max-frames', type=int, help='Maximum frames to encode')
    encode_parser.add_argument('--no-compression', action='store_true', help='Disable compression')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode .sanchez to video/image')
    decode_parser.add_argument('input', help='Input .sanchez file')
    decode_parser.add_argument('output', nargs='?', help='Output video/image file')
    decode_parser.add_argument('-a', '--audio', help='Audio file to mux')
    decode_parser.add_argument('-r', '--resize', help='Resize to WxH (e.g., 1280x720)')
    decode_parser.add_argument('-f', '--frame', type=int, help='Extract single frame (0-indexed)')
    decode_parser.add_argument('--frames', action='store_true', help='Extract all frames')
    decode_parser.add_argument('--format', choices=['png', 'jpg', 'bmp'], help='Frame format')
    
    # Play command
    play_parser = subparsers.add_parser('play', help='Play .sanchez file')
    play_parser.add_argument('input', help='Input .sanchez file')
    play_parser.add_argument('-a', '--audio', help='Audio file to play')
    play_parser.add_argument('-s', '--scale', type=float, default=1.0, help='Display scale')
    play_parser.add_argument('--start-frame', type=int, help='Start from frame')
    play_parser.add_argument('--fullscreen', action='store_true', help='Start in fullscreen')
    play_parser.add_argument('--simple', action='store_true', help='Use simple viewer (no pygame)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show .sanchez file info')
    info_parser.add_argument('input', help='Input .sanchez file')
    
    args = parser.parse_args()
    
    if args.command == 'encode':
        cmd_encode(args)
    elif args.command == 'decode':
        cmd_decode(args)
    elif args.command == 'play':
        cmd_play(args)
    elif args.command == 'info':
        cmd_info(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
