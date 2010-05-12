/* -*- mode: css -*- */

/* -------------------------------------------------- */
/* normal rail */
.rail.bridge[zoom>=17][railway!=tram][railway!=narrow_gauge][railway!=monorail][bridge=yes],
.rail.bridge[zoom>=17][railway!=tram][railway!=narrow_gauge][railway!=monorail][bridge=true],
.rail.bridge[zoom>=17][railway!=tram][railway!=narrow_gauge][railway!=monorail][bridge=1]
{
/* the dark casing when it's a bridge */
    line-color: #121212;
    line-width: 10;
}
.rail.outline[zoom>=17]
{
/* the two tracks */
    line-color: #808080;
    line-width: 8;
}
.rail.centerline[zoom>=17]
{
/* the white centerline dividing the tracks */
    line-color: #ddd;
    line-width: 6;
}
.rail.line[zoom>=17]
{
/* the wooden... things */
    line-color: #808080;
    line-width: 9;
    line-dasharray: 1, 7;
}

.rail.bridge[zoom=16][railway!=tram][railway!=narrow_gauge][railway!=monorail][bridge=yes],
.rail.bridge[zoom=16][railway!=tram][railway!=narrow_gauge][railway!=monorail][bridge=true],
.rail.bridge[zoom=16][railway!=tram][railway!=narrow_gauge][railway!=monorail][bridge=1]
{
/* the dark casing when it's a bridge */
    line-color: #121212;
    line-width: 9;
}
.rail.outline[zoom=16]
{
/* the two tracks */
    line-color: #808080;
    line-width: 6;
}
.rail.centerline[zoom=16]
{
/* the white centerline dividing the tracks */
    line-color: #ddd;
    line-width: 4;
}
.rail.line[zoom=16]
{
/* the wooden... things */
    line-color: #808080;
    line-width: 8;
    line-dasharray: 1, 5;
}


.rail.centerline[zoom>=14][zoom<=15][railway!=tram][railway!=narrow_gauge][railway!=monorail]
{
    line-color: #808080;
    line-width: 1;
}
.rail.line[zoom>=14][zoom<=15][railway!=tram][railway!=narrow_gauge][railway!=monorail]
{
    line-color: #808080;
    line-width: 6;
    line-dasharray: 1, 6;
}

.rail.centerline[zoom>=12][zoom<=13][railway!=tram][railway!=narrow_gauge][railway!=monorail]
{
    line-color: #808080;
    line-width: 1;
}
.rail.line[zoom>=12][zoom<=13][railway!=tram][railway!=narrow_gauge][railway!=monorail]
{
    line-color: #808080;
    line-width: 4;
    line-dasharray: 1, 4;
}

.rail.centerline[zoom=11][railway!=tram][railway!=narrow_gauge][railway!=monorail]
{
    line-color: #808080;
    line-width: 1;
}
.rail.line[zoom=11][railway!=tram][railway!=narrow_gauge][railway!=monorail]
{
    line-color: #808080;
    line-width: 3;
    line-dasharray: 1, 4;
}


/* ------------------------- */
/* tunnels */
.rail.outline[zoom>=17][tunnel=yes]
{
/* the two tracks are dashed now */
    line-dasharray: 2, 2;
}
.rail.centerline[zoom>=17]
{
/* the white centerline dividing the tracks is brighter */
    line-color: #eee;
}

.rail.outline[zoom=16][tunnel=yes]
{
/* the two tracks are dashed now */
    line-dasharray: 2, 2;
}
.rail.centerline[zoom=16]
{
/* the white centerline dividing the tracks is brighter */
    line-color: #eee;
}

/* -------------------------------------------------- */
/* trams */
.rail.centerline[zoom=15][railway=tram]
{
    line-color: #808080;
    line-width: 1;
}

.rail.line[zoom=15][railway=tram]
{
    line-color: #808080;
    line-width: 3;
    line-dasharray: 1, 4;
}

.rail.outline[zoom=16][railway=tram]
{
/* the two tracks */
    line-color: #808080;
    line-width: 4;
}
.rail.centerline[zoom=16][railway=tram]
{
/* the white centerline dividing the tracks */
    line-color: #ddd;
    line-width: 2;
}
.rail.line[zoom=16][railway=tram]
{
/* the wooden... things */
    line-color: #808080;
    line-width: 6;
    line-dasharray: 1, 5;
}

.rail.outline[zoom>16][railway=tram]
{
/* the two tracks */
    line-color: #808080;
    line-width: 4;
}
.rail.centerline[zoom>16][railway=tram]
{
/* the white centerline dividing the tracks */
    line-color: #ddd;
    line-width: 2;
}
.rail.line[zoom>16][railway=tram]
{
/* the wooden... things */
    line-color: #808080;
    line-width: 6;
    line-dasharray: 1, 5;
}

/* -------------------------------------------------- */
/* disused/abandoned */
.rail.line[disused=yes],
.rail.line[disused=true],
.rail.line[railway=disused],
.rail.outline[disused=yes],
.rail.outline[disused=true],
.rail.outline[railway=disused],
.rail.centerline[disused=yes],
.rail.centerline[disused=true],
.rail.centerline[railway=disused]
{
    line-opacity: 0.5;
}

/*.rail.line[abandoned=yes],
.rail.line[abandoned=true],
*/
.rail.line[railway=abandoned],
.rail.outline[railway=abandoned],
.rail.centerline[railway=abandoned]
{
    line-opacity: 0.25;
}

/* -------------------------------------------------- */
/* transit */
.transit.point[zoom>=13] name
{
    text-face-name: "Droid Sans Regular";
    text-fill: #082685;
    text-placement: point;
    text-size: 8;
}

.transit.point[zoom>=14] name
{
    text-face-name: "Droid Sans Regular";
    text-fill: #082685;
    text-placement: point;
    text-size: 9;
}

.transit.point[zoom>=15] name
{
    text-face-name: "Droid Sans Regular";
    text-fill: #082685;
    text-placement: point;
    text-size: 10;
    point-allow-overlap: true;
}

.transit.point[zoom>=16] name
{
    text-face-name: "Droid Sans Regular";
    text-fill: #082685;
    text-placement: point;
    text-size: 11;
    point-allow-overlap: true;
}

.transit.point[railway=station][zoom>=17],
.transit.point[railway=subway_entrance][zoom>=17]
{
    point-file: url('img/misc/railway_station.24.png');
    point-allow-overlap: true;
    text-dy: 14;
}

.transit.point[aeroway=airport][zoom>=17],
.transit.point[aeroway=aerodrome][zoom>=17]
{
    point-file: url('img/misc/airport.24.png');
    text-dy: 24;
}

.transit.point[railway=station][zoom>=15][zoom<=16],
.transit.point[railway=subway_entrance][zoom>=15][zoom<=16]
{
    point-file: url('img/misc/railway_station.16.png');
    point-allow-overlap: true;
    text-dy: 12;
}
.transit.point[railway=halt][zoom>=15],
.transit.point[railway=tram_stop][zoom>=15]
{
    point-file: url('img/mapnik-symbols/halt.png');
    point-allow-overlap: true;
    text-dy: 5;
}


.transit.point[aeroway=airport][zoom>=14][zoom<=16],
.transit.point[aeroway=aerodrome][zoom>=14][zoom<=16]
{
    point-file: url('img/misc/airport.24.png');
    text-dy: 24;
}

.transit.point[zoom>=17] name
{
    text-size: 12;
    text-halo-radius: 2;
    text-wrap-width: 65;
}

.transit.point[zoom>=15][zoom<=16] name,
.transit.point[aeroway=airport][zoom>=10][zoom<=14] name,
.transit.point[aeroway=aerodrome][zoom>=10][zoom<=14] name
{
    text-size: 9;
    text-halo-radius: 1;
    text-wrap-width: 50;
}

.transit.point[railway=station][zoom>=12][zoom<=14],
.transit.point[railway=subway_entrance][zoom>=12][zoom<=14]
{
    point-file: url('img/misc/railway_station.12.png');
    /* point-allow-overlap: true; */
    text-dy: 10;
}

.transit.point[aeroway=airport][zoom>=12][zoom<=13],
.transit.point[aeroway=aerodrome][zoom>=12][zoom<=13]
{
    point-file: url('img/misc/airport.16.png');
    text-dy: 20;
}

.transit.point[aeroway=airport][zoom>=9][zoom<=11],
.transit.point[aeroway=aerodrome][zoom>=9][zoom<=11]
{
    point-file: url('img/misc/airport.12.png');
    text-dy: 18;
}
