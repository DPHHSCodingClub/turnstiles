README
======

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aarontran/turnstiles/HEAD?labpath=mta_turnstile_map.ipynb)

2022 July 06 -- a quick project to visualize turnstile data in 2D form,
to show off tools like . . .

* more complex scatter plots
* imshow
* working with coordinate transformations.

Stick to numpy, don't use anything more complex than
base Python + dict, list transformations.

Data sources:
* http://web.mta.info/developers/turnstile.html
* https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm
* https://data.ny.gov/Transportation/NYC-Transit-Subway-Entrance-And-Exit-Data/i9wp-a4ja


Create movie:

    ffmpeg -y -framerate 15 -pattern_type glob -i "*.png" \
        -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -pix_fmt yuvj420p \
        -vcodec libx264 \
        result.mp4

