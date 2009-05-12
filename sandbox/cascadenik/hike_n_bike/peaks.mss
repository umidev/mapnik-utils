/* -*- css -*- */

/*
update planet_osm_polygon set importance=0 where importance is null;
update planet_osm_line set importance=0 where importance is null;
update planet_osm_point set importance=0 where importance is null;
*/


/* catch-all - FIXME: remove this at some point */
/*
.peak.point[zoom>=13]
{
    point-file: url('map-icons/svg-twotone-png/poi_point_of_interest.p.12.png');
    text-dy: 14;
    text-face-name: "DejaVu Sans Book";
    text-size: 8;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #ff3333;
    text-halo-radius: 1;
}
*/

.peak.point[natural=peak][zoom>=9][importance>=4] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.4.png');
    text-dy: 6;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 7;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}

.peak.point[natural=peak][zoom>=10][importance>=3] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.4.png');
    text-dy: 6;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 7;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}

.peak.point[natural=peak][zoom>=11][importance>=2] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.4.png');
    text-dy: 6;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 7;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}

.peak.point[natural=peak][zoom>=12][importance>=1] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.5.png');
    text-dy: 7;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 8;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}

.peak.point[natural=peak][zoom>=13] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.6.png');
    text-dy: 8;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 8;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}
.peak.point[natural=peak][zoom>=13][importance>=1] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.8.png');
    text-dy: 10;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 9;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=13][importance>=2] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.9.png');
    text-dy: 11;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 9;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=13][importance>=3] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.10.png');
    text-dy: 12;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 9;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=13][importance>=4] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.12.png');
    text-dy: 14;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}

.peak.point[natural=peak][zoom>=14] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.8.png');
    text-dy: 10;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 9;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}
.peak.point[natural=peak][zoom>=14][importance>=1] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.10.png');
    text-dy: 12;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=14][importance>=2] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.11.png');
    text-dy: 13;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=14][importance>=3] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.12.png');
    text-dy: 14;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=14][importance>=4] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.14.png');
    text-dy: 16;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}


.peak.point[natural=peak][zoom>=15] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.8.png');
    text-dy: 10;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}
.peak.point[natural=peak][zoom>=15][importance>=1] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.12.png');
    text-dy: 14;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=15][importance>=2] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.16.png');
    text-dy: 18;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=15][importance>=3] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.17.png');
    text-dy: 19;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=15][importance>=4] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.19.png');
    text-dy: 21;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 12;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}



.peak.point[natural=peak][zoom>=16] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.12.png');
    text-dy: 14;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}
.peak.point[natural=peak][zoom>=16][importance>=1] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.16.png');
    text-dy: 18;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=16][importance>=2] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.17.png');
    text-dy: 19;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=16][importance>=3] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.18.png');
    text-dy: 20;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=16][importance>=4] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.20.png');
    text-dy: 22;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}


.peak.point[natural=peak][zoom>=17] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.16.png');
    text-dy: 18;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-fill: #333333;
    text-size: 10;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}
.peak.point[natural=peak][zoom>=17][importance>=1] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.18.png');
    text-dy: 20;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=17][importance>=2] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.19.png');
    text-dy: 21;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=17][importance>=3] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.20.png');
    text-dy: 22;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 11;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}
.peak.point[natural=peak][zoom>=17][importance>=4] name
{
    point-file: url('map-icons/svg-twotone-png/poi_peak.p.22.png');
    text-dy: 24;
    text-face-name: "DejaVu Sans Condensed Bold";
    text-size: 12;
    text-placement: point;
    text-wrap-width: 500;
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
    point-allow-overlap: true;
}

/* ---------------------------------------------------------------------- */

.peak.point[natural=peak][zoom>=16][importance>0] ele
{
    text-dy: 30;
    text-face-name: "DejaVu Sans Oblique";
    text-fill: #333333;
    text-size: 7;
    text-placement: point;
    text-wrap-width: 500; /* basically never */
    text-halo-fill: #fefefe;
    text-halo-radius: 1;
}

