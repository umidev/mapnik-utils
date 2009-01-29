/* -*- css -*- */

.srtm.ten
{
    line-color: #efe7e0;
    line-width: 1.0;
    line-opacity: 0.4;
}

.srtm.fifty
{
    line-color: #efdfd1;
    line-width: 1.1;
    line-opacity: 0.7;
}


.srtm.fifty[zoom>=15] height
{
    text-face-name: "DejaVu Sans Book";
    text-size: 7;
    text-placement: line;
    text-fill: #e4ae80;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    text-max-char-angle-delta: 20;
    text-min-distance: 50;
    text-spacing: 400;
    text-avoid-edges: true;
}

.srtm.hundred height
{
    line-color: #e4ae80;
    line-width: 1.3;
    line-opacity: 0.5;

    text-face-name: "DejaVu Sans Book";
    text-size: 8;
    text-placement: line;
    text-fill: #e4ae80;
/*     text-halo-fill: #11111180; */
/*     text-halo-fill: #111111,; */
    text-halo-fill: #fefefe; /* 20% alpha is a good value */
    text-halo-radius: 2;
    text-max-char-angle-delta: 20;
    text-min-distance: 50;
    text-spacing: 400;
    text-avoid-edges: true;
}
