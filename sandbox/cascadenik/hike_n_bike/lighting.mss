/* -*- mode: css -*- */

/* Roads */

.road.lighting[zoom>=8]
{
    line-cap: round;
    line-join: miter;
    line-opacity: 1.0;
    outline-cap: butt;
    outline-join: miter;
}

/* lit and unlit */
.road.lighting[lit=yes]{ line-color: #ddc13d; }
.road.lighting[lit=no] { line-color: #000000; }

/* line widths depending on zoom and prominence */
.road.lighting[prominence=major][zoom<=8]{ line-width: 1; }
.road.lighting[prominence=minor][zoom<=8]{ line-width: 1; }

.road.lighting[prominence=major][zoom=9] { line-width: 2; }
.road.lighting[prominence=minor][zoom=9] { line-width: 1; }

.road.lighting[prominence=major][zoom=10]{ line-width: 3; }
.road.lighting[prominence=minor][zoom=10]{ line-width: 1; }

.road.lighting[prominence=major][zoom=11]{ line-width: 4; }
.road.lighting[prominence=minor][zoom=11]{ line-width: 2; }

.road.lighting[prominence=major][zoom=12]{ line-width: 5; }
.road.lighting[prominence=minor][zoom=12]{ line-width: 3; }

.road.lighting[prominence=major][zoom=13]{ line-width: 6; }
.road.lighting[prominence=minor][zoom=13]{ line-width: 4; }

.road.lighting[prominence=major][zoom=14]{ line-width: 8; }
.road.lighting[prominence=minor][zoom=14]{ line-width: 6; }

.road.lighting[prominence=major][zoom=15]{ line-width: 9; }
.road.lighting[prominence=minor][zoom=15]{ line-width: 7; }

.road.lighting[prominence=major][zoom>=16]{ line-width: 10; }
.road.lighting[prominence=minor][zoom>=16]{ line-width:  8; }



/* Ways */

.way.lighting[zoom>=14]
{
    line-cap: round;
    line-join: miter;
    line-opacity: 1.0;
    outline-cap: butt;
    outline-join: miter;
}

/* lit and unlit */
.way.lighting[lit=yes]{ line-color: #ddc13d; }
.way.lighting[lit=no] { line-color: #000000; }

/* line widths depending on zoom */
.way.lighting[zoom=13] { line-width: 2; }
.way.lighting[zoom=14] { line-width: 2; }
.way.lighting[zoom=15] { line-width: 3; }
.way.lighting[zoom=16] { line-width: 4; }
.way.lighting[zoom>16] { line-width: 5; }



/* Buildings */

.building.lighting[zoom>=14]
{
    line-cap: round;
    line-join: miter;
    line-opacity: 1.0;
    line-width: 1;
    polygon-opacity: 0.7;
    outline-cap: butt;
    outline-join: miter;
}

/* lit and unlit */
.building.lighting[lit=yes]{ line-color: #ddc13d; }
.building.lighting[lit=no] { line-color: #000000; }



/* Areas */

.area.lighting[building!=yes][zoom>=8]
{
    line-cap: round;
    line-join: miter;
    line-opacity: 1.0;
    line-width: 1;
    polygon-opacity: 0.7;
    outline-cap: butt;
    outline-join: miter;
}

/* lit and unlit */
.area.lighting[lit=yes]{ polygon-fill: #ddc96a; }
.area.lighting[lit=no] { polygon-fill: #000000; }


/* TODO: highway = street_lamp, see http://www.openstreetmap.org/browse/node/378995336 */
