#!/bin/sh
wget -O N50W002.hgt.zip ftp://e0srp01u.ecs.nasa.gov/srtm/version2/SRTM3/Eurasia/N50W002.hgt.zip
# srtm_generate_hdr.sh from http://mpa.itc.it/rs/srtm/:
./srtm_generate_hdr.sh N50W002.hgt.zip
gdal_translate -of GTiff -co "TILED=YES" -a_srs "+proj=latlong" N50W002.tif N50W002.translated.tif
rm -f N50W002.mercator.tif
gdalwarp -of GTiff -co "TILED=YES" \
                -srcnodata 32767 \
                -dstnodata 32767 \
                -t_srs "+proj=merc +ellps=sphere +R=6378137 +a=6378137 +units=m" \
                -r cubicspline -order 3 \
                -tr 76.437 76.437 \
                -wt Float32 -ot Float32 \
                -wo SAMPLE_STEPS=100 \
                N50W002.translated.tif N50W002.mercator.tif
