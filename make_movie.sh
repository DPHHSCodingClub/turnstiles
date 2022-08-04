#!/usr/bin/env bash
ffmpeg -y -framerate 15 -pattern_type glob -i "out/*.png" \
    -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -pix_fmt yuvj420p \
    -vcodec libx264 \
    result.mp4
