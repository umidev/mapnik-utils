/* -*- mode: css -*- */

.road.lighting
{
    line-cap: round;
    line-join: miter;
    outline-cap: butt;
    outline-join: miter;
    line-opacity: 1.0;
}

/* lit ways */
.road.lighting[highway=residential]
{
    line-color: #ddc13d;
}

/* unlit ways */
.road.lighting[highway=tertiary]
{
    line-color: #000000;
}

.road.lighting[prominence=major][zoom=12]{line-width: 5;}
.road.lighting[prominence=minor][zoom=12]{line-width: 3;}

.road.lighting[prominence=major][zoom=13]{line-width: 6;}
.road.lighting[prominence=minor][zoom=13]{line-width: 4;}

.road.lighting[prominence=major][zoom=14]{line-width: 8;}
.road.lighting[prominence=minor][zoom=14]{line-width: 6;}

.road.lighting[prominence=major][zoom=15]{line-width: 9;}
.road.lighting[prominence=minor][zoom=15]{line-width: 7;}

.road.lighting[prominence=major][zoom=16]{line-width: 10;}
.road.lighting[prominence=minor][zoom=16]{line-width: 8;}


/*
.road.lighting[zoom>=12] name
{
    text-face-name: "DejaVu Sans Book";
    text-size: 9;
    text-fill: #000;
    text-placement: line;
    text-halo-radius: 1;
    text-halo-fill: #fdfdfd;
    text-max-char-angle-delta: 20;
    text-min-distance: 50;
    text-spacing: 400;
}

.road.lighting[highway=residential] name
{
    text-halo-radius: 3;
    text-halo-fill: #ddb600;
}

*/