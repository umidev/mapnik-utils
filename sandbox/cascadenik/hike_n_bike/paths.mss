/* -*- css -*- */

.path
{
    line-cap: butt;
    line-join: round;
}

.path[highway=steps]
{
    line-cap: butt;
    line-join: miter;
}

.path.outline
{ 
    line-width: 3;
    line-dasharray: 3, 3;
}
.path.inline
{
    line-width: 2;
/*     line-dasharray: 3, 3; */
}

.path.outline[highway=path]
{ 
    line-width: 2;
    line-dasharray: 2, 2;
}
.path.inline[highway=path]
{
    line-width: 1;
    line-dasharray: 2, 2;
}

.path.outline[highway=footway],
.path.outline[highway=path][foot=designated]
{ 
    line-width: 2;
    line-dasharray: 6, 2;
}
.path.inline[highway=footway],
.path.inline[highway=path][foot=designated]
{
    line-width: 1;
    line-dasharray: 6, 2;
}

.path.outline[highway=track]
{ 
    line-width: 2;
    line-dasharray: 18, 2;
}
.path.inline[highway=track]
{
    line-width: 1;
    line-dasharray: 18, 2;
}


.path.outline[highway=track][tracktype=grade1]
{ 
    line-width: 2.5;
    line-dasharray: 18, 1;
}
.path.inline[highway=track][tracktype=grade1]
{
    line-width: 2.0;
    line-dasharray: 18, 1;
}


.path.outline[highway=track][tracktype=grade2]
{ 
    line-width: 2.0;
    line-dasharray: 18, 3;
}
.path.inline[highway=track][tracktype=grade2]
{
    line-width: 1.5;
    line-dasharray: 18, 3;
}


.path.outline[highway=track][tracktype=grade3]
{ 
    line-width: 2.0;
    line-dasharray: 15, 3;
}
.path.inline[highway=track][tracktype=grade3]
{
    line-width: 1.5;
    line-dasharray: 15, 3;
}


/* FIXME: change color? */
.path.outline[highway=track][tracktype=grade4]
{ 
    line-width: 1.7;
    line-dasharray: 12, 2;
}
.path.inline[highway=track][tracktype=grade4]
{
    line-width: 1.2;
    line-dasharray: 12, 2;
}


/* FIXME: change color? */
.path.outline[highway=track][tracktype=grade5]
{ 
    line-width: 1.5;
    line-dasharray: 9, 3;
}
.path.inline[highway=track][tracktype=grade5]
{
    line-width: 1.0;
    line-dasharray: 9, 3;
}


.path.outline[zoom>=16][highway=steps] 
{ 
    line-width: 8; 
}
.path.inline[zoom>=16][highway=steps]
{
    line-width: 6;
    line-dasharray: 2, 2;
}

.path.outline[zoom>=14][zoom<=15][highway=steps] 
{ 
    line-width: 6;
}
.path.inline[zoom>=14][zoom<=15][highway=steps]
{
    line-width: 4;
    line-dasharray: 1, 1;
}


.path.outline[zoom>=11][highway=cycleway],
.path.outline[zoom>=11][highway=path][bicycle=designated]
{
    line-width: 3;
    line-dasharray: 18, 2;
}
.path.inline[zoom>=11][highway=cycleway],
.path.inline[zoom>=11][highway=path][bicycle=designated]
{
    line-width: 2;
    line-dasharray: 18, 2;
}


.path.outline[zoom>=11][highway=bridleway],
.path.outline[zoom>=11][highway=path][horse=designated]
{
    line-width: 3;
    line-dasharray: 9, 2;
}
.path.inline[zoom>=11][highway=bridleway],
.path.inline[zoom>=11][highway=path][horse=designated]
{
    line-width: 2;
    line-dasharray: 9, 2;
}



/** Path Colors **/

.path.outline
{
    line-color: #f00; /* catch-all */
    line-opacity: 0.7;
}
.path.inline
{
    line-color: #000;
    line-opacity: 0.5;
}

.path.outline[highway=path]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[highway=path]
{
    line-opacity: 0.75;
}


.path.outline[highway=footway]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[highway=footway]
{
    line-opacity: 0.95;
}


.path.outline[highway=track]
{
    line-color: #fff;
    line-opacity: 0.9;
}
.path.inline[highway=track]
{
    line-opacity: 0.95;
}


.path.outline[highway=steps]
{
    line-color: #fff;
    line-opacity: 0.1;
}
.path.inline[highway=steps]
{
    line-color: #000;
    line-opacity: 0.75;
}


.path.outline[highway=cycleway],
.path.outline[highway=path][bicycle=designated]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[highway=cycleway],
.path.inline[highway=path][bicycle=designated]
{
    line-color: #00f;
    line-opacity: 0.7;
}


.path.outline[highway=bridleway],
.path.outline[highway=path][horse=designated]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[highway=bridleway],
.path.inline[highway=path][horse=designated]
{
    line-color: #0bbf13;
    line-opacity: 0.7;
}


/* fade out at higher zooms */

.path.outline[zoom=13],
.path.inline[zoom=13]
{
    line-opacity: 0.5;
}

.path.outline[zoom=12],
.path.inline[zoom=12]
{
    line-opacity: 0.3;
}

.path.outline[zoom=11],
.path.inline[zoom=11]
{
    line-opacity: 0.1;
}

.path.outline[zoom<=10],
.path.inline[zoom<=10]
{
    line-opacity: 0.01;
}

/** Path Labels **/

.path.label[zoom>=12] name
{
    text-face-name: "DejaVu Sans Book";
    text-size: 8;
    text-fill: #000;
    text-placement: line;
    text-dy: 5;
    text-halo-radius: 1;
    text-halo-fill: #fff;
    text-max-char-angle-delta: 20;
    text-min-distance: 50;
    text-spacing: 400;
}

.path.label[zoom>=15] name
{
    text-face-name: "DejaVu Sans Book";
    text-size: 10;
    text-fill: #000;
    text-placement: line;
    text-dy: 7;
    text-halo-radius: 1;
    text-halo-fill: #fff;
    text-max-char-angle-delta: 20;
    text-min-distance: 50;
    text-spacing: 400;
}
