/* -*- mode: css -*- */

.path.closed[zoom>=13]
{
    line-color: #f00;
    line-opacity: 0.7;
    line-cap: butt;
    line-join: miter;
}
.path.closed[zoom=13]
{
    line-width: 3;
    line-dasharray: 1, 1, 1, 8;
}
.path.closed[zoom=14]
{
    line-width: 5;
    line-dasharray: 1, 1, 1, 10;
}
.path.closed[zoom=15],
.path.closed[zoom=16]
{
    line-width: 7;
    line-dasharray: 1, 2, 1, 14;
}
.path.closed[zoom>=17]
{
    line-width: 9;
    line-dasharray: 1, 2, 1, 24;
}



.path[zoom>=10]
{
    line-cap: butt;
    line-join: round;
}

.path[zoom>=10][highway=steps]
{
    line-cap: butt;
    line-join: miter;
}

.path.outline[zoom>=10]
{ 
    line-width: 3;
    line-dasharray: 3, 3;
}
.path.inline[zoom>=10]
{
    line-width: 2;
/*     line-dasharray: 3, 3; */
}

.path.outline[zoom>=10][highway=path]
{ 
    line-width: 2;
    line-dasharray: 2, 2;
}
.path.inline[zoom>=10][highway=path]
{
    line-width: 1;
    line-dasharray: 2, 2;
}

.path.outline[zoom>=10][highway=footway],
.path.outline[zoom>=10][highway=path][foot=designated]
{ 
    line-width: 2;
    line-dasharray: 6, 2;
}
.path.inline[zoom>=10][highway=footway],
.path.inline[zoom>=10][highway=path][foot=designated]
{
    line-width: 1;
    line-dasharray: 6, 2;
}

.path.outline[zoom>=10][highway=track]
{ 
    line-width: 2;
    line-dasharray: 18, 2;
}
.path.inline[zoom>=10][highway=track]
{
    line-width: 1;
    line-dasharray: 18, 2;
}


.path.outline[zoom>=10][highway=track][tracktype=grade1]
{ 
    line-width: 2.5;
    line-dasharray: 18, 1;
}
.path.inline[zoom>=10][highway=track][tracktype=grade1]
{
    line-width: 2.0;
    line-dasharray: 18, 1;
}


.path.outline[zoom>=10][highway=track][tracktype=grade2]
{ 
    line-width: 2.0;
    line-dasharray: 18, 3;
}
.path.inline[zoom>=10][highway=track][tracktype=grade2]
{
    line-width: 1.5;
    line-dasharray: 18, 3;
}


.path.outline[zoom>=10][highway=track][tracktype=grade3]
{ 
    line-width: 2.0;
    line-dasharray: 15, 3;
}
.path.inline[zoom>=10][highway=track][tracktype=grade3]
{
    line-width: 1.5;
    line-dasharray: 15, 3;
}


/* FIXME: change color? */
.path.outline[zoom>=10][highway=track][tracktype=grade4]
{ 
    line-width: 1.7;
    line-dasharray: 12, 2;
}
.path.inline[zoom>=10][highway=track][tracktype=grade4]
{
    line-width: 1.2;
    line-dasharray: 12, 2;
}


/* FIXME: change color? */
.path.outline[zoom>=10][highway=track][tracktype=grade5]
{ 
    line-width: 1.5;
    line-dasharray: 9, 3;
}
.path.inline[zoom>=10][highway=track][tracktype=grade5]
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

.path.outline[zoom>=10]
{
    line-color: #f00;
    line-opacity: 0.7;
}
.path.inline[zoom>=10]
{
    line-color: #000;
    line-opacity: 0.5;
}

.path.outline[zoom>=10][highway=path]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[zoom>=10][highway=path]
{
    line-opacity: 0.75;
}


.path.outline[zoom>=10][highway=footway]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[zoom>=10][highway=footway]
{
    line-opacity: 0.95;
}


.path.outline[zoom>=10][highway=track]
{
    line-color: #fff;
    line-opacity: 0.9;
}
.path.inline[zoom>=10][highway=track]
{
    line-opacity: 0.95;
}


.path.outline[zoom>=10][highway=steps]
{
    line-color: #fff;
    line-opacity: 0.1;
}
.path.inline[zoom>=10][highway=steps]
{
    line-color: #000;
    line-opacity: 0.75;
}


.path.outline[zoom>=10][highway=cycleway],
.path.outline[zoom>=10][highway=path][bicycle=designated]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[zoom>=10][highway=cycleway],
.path.inline[zoom>=10][highway=path][bicycle=designated]
{
    line-color: #00f;
    line-opacity: 0.7;
}


.path.outline[zoom>=10][highway=bridleway],
.path.outline[zoom>=10][highway=path][horse=designated]
{
    line-color: #fff;
    line-opacity: 0.77;
}
.path.inline[zoom>=10][highway=bridleway],
.path.inline[zoom>=10][highway=path][horse=designated]
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

.path.outline[zoom=10],
.path.inline[zoom=10]
{
    line-opacity: 0.01;
}

/** Path Labels **/

.path.label[zoom>=12] name
{
    text-face-name: "Droid Sans Regular";
    text-size: 8;
    text-fill: #000;
    text-placement: line;
    text-dy: 5;
    text-halo-radius: 1;
    text-halo-fill: #fcfcfc;
    text-max-char-angle-delta: 20;
    text-min-distance: 50;
    text-spacing: 400;
}

.path.label[zoom>=15] name
{
    text-face-name: "Droid Sans Regular";
    text-size: 10;
    text-fill: #000;
    text-placement: line;
    text-dy: 7;
    text-halo-radius: 1;
    text-halo-fill: #fcfcfc;
    text-max-char-angle-delta: 20;
    text-min-distance: 50;
    text-spacing: 400;
}
