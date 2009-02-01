/* -*- css -*- */

.coast.edge.outer
{
    line-width: 13;
    line-color: #a1cbea;/* !!! */
    line-join: round;
}

.coast.edge.inner
{
    line-width: 5;
    line-color: #7eaac1;/* !!! */
    line-join: round;
}

.coast.edge.outer[zoom<=12] { line-width: 9; }
.coast.edge.inner[zoom<=12] { line-width: 3; }

/* water areas with an outline look bad because they show the seams 
   when riverbanks touch along the length of a river, so don't outline any waters */

.water.area
{
    polygon-fill: #cae5fb;
    polygon-opacity: 0.95;
    line-join: round;
}

.water.line
{
    line-color: #cae5fb;
    line-join: round;
}

.water.line[zoom>=13],
.water.line[zoom>=15][waterway=stream]
{
    line-color: #cae5fb;

/*     outline-width: 1; */
/*     outline-color: #7eaac1; */
/*     outline-join: round; */
}

.water.line[zoom>=11][zoom<=12] { line-width: 2; }
.water.line[zoom>=11][zoom<=12][waterway=stream] { line-width: 1; }

.water.line[zoom=13] { line-width: 3; }
.water.line[zoom=13][waterway=stream] { line-width: 1.5; }

.water.line[zoom=14] { line-width: 5; }
.water.line[zoom=14][waterway=stream] { line-width: 2; }

.water.line[zoom=15] { line-width: 6; }
.water.line[zoom=15][waterway=stream] { line-width: 2.5; }

.water.line[zoom=16] { line-width: 7; }
.water.line[zoom=16][waterway=stream] { line-width: 3; }

.water.line[zoom>=17] { line-width: 9; }
.water.line[zoom>=17][waterway=stream] { line-width: 5; }

.water.ferry[zoom>=11]
{
    line-width: 1.0;
    line-color: #000080; /* navy */
    line-dasharray: 3, 3;
}

.water.ferry[zoom>=13]
{
    line-width: 1.5;
    line-color: #000080; /* navy */
    line-dasharray: 5, 5;
}

.coast.fill
{
/*     polygon-fill: #dceee9; */
    /*
    line-width: 1;
    line-color: #dceee9;
    */
}

.citylike.area
{
    polygon-fill: #dddddd;
    polygon-opacity: 0.45;
}

.citylike.area[landuse=residential]
{
/*     polygon-fill: #eeeeee; */
     polygon-fill: #f3dfa4;
    polygon-opacity: 0.45;
}

.citylike.area[landuse=industrial]
{
     polygon-fill: #f3dfa4;
    polygon-opacity: 0.45;
}

/*
.citylike.area[amenity=school],
.citylike.area[amenity=college],
.citylike.area[amenity=university]
{
    polygon-fill: #d2caba;
    polygon-opacity: 0.45;
}
*/

.parklike.area
{
    polygon-fill: #91b156;
    polygon-opacity: 0.45;
}

/* .parklike.area[zoom>=16][leisure!=pitch][leisure!=track][landuse!=cemetery] /\*, */
/* .parklike.area[zoom>=14][zoom<=15][leisure!=pitch][leisure!=track][landuse!=cemetery][size=large] *\/ */
/* { */
/*     polygon-pattern-file: url('img/trees-z.png'); */
/* } */

/* .parklike.area[zoom>=11] */
/* { */
/*     line-width: 1; */
/*     line-color: #6dbe3c; */
/* } */

.parklike.area[landuse=cemetery]
{
    line-color: #799a67;
    polygon-fill: #94b580;
    polygon-opacity: 0.45;
}

.parklike.area[natural=wood],
.parklike.area[landuse=forest]
{
/*     line-color: #799a67; */
    polygon-fill: #e0f0bc;
    polygon-opacity: 0.45;
}

.parklike.area[landuse=allotments]
{
    polygon-fill: #c8b084;
    polygon-opacity: 0.45;
}

.parklike.area[landuse=farm]
{
    polygon-fill: #ead8bd;
    polygon-opacity: 0.45;
}

.parklike.area[landuse=recreation_ground],
.parklike.area[landuse=greenfield],
.parklike.area[landuse=meadow],
.parklike.area[landuse=grass],
.parklike.area[landuse=village_green]
{
    polygon-fill: #ace38b;
    polygon-opacity: 0.45;
}

.parklike.area[landuse=quarry]
{
    polygon-fill: #bbb;
    polygon-opacity: 0.45;
}

.parklike.line[natural=cliff],
.parklike.line[man_made=embankment]
{
    line-pattern-file: url('icons-mapnik/cliff2.png');
}

/* .parklike.area[zoom>=16][landuse=cemetery] /\*, */
/* .parklike.area[zoom=15][landuse=cemetery][size=large] *\/ */
/* { */
/*     polygon-pattern-file: url('img/graveyard-z.png'); */
/* } */

.building.area[zoom>=13]
{
    polygon-fill: #dc7c6e;
    polygon-opacity: 0.8;
}

/* .building.area[zoom>=15] */
/* { */
/*     line-width: 1; */
/*     line-color: #808080; */
/* } */


.power.line[zoom>=14]
{
    line-color: #777;
    line-join: round;
    line-width: 1;
}

.power.point[zoom>=14]
{
    point-file: url('icons-mapnik/power_tower.png');
}


/* /\* admin_level=2 --> Staatsgrenze *\/ */
/* .boundary.line[admin_level="2"][scale-denominator>=5000000][scale-denominator<200000000], */
/* .boundary.line[admin_level="3"][scale-denominator>=5000000][scale-denominator<200000000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 0.6; */
/*     line-opacity: 0.2; */
/* } */

/* /\* admin_level=2 --> Staatsgrenze *\/ */
/* .boundary.line[admin_level="2"][scale-denominator>=1000000][scale-denominator<5000000], */
/* .boundary.line[admin_level="3"][scale-denominator>=1000000][scale-denominator<5000000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 2; */
/*     line-opacity: 0.2; */
/* } */

/* /\* admin_level=2 --> Staatsgrenze *\/ */
/* .boundary.line[admin_level="2"][scale-denominator<1000000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 6; */
/*     line-opacity: 0.1; */
/* } */

/* .boundary.line[admin_level="3"][scale-denominator<1000000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 5; */
/*     line-dasharray: 4,2; */
/*     line-opacity: 0.1; */
/* } */


/* /\* admin_level=4 --> Bundesland *\/ */
/* .boundary.line[admin_level="4"][scale-denominator<500000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 3; */
/*     line-dasharray: 4,3; */
/*     line-opacity: 0.2; */
/* } */

/* .boundary.line[admin_level="5"][scale-denominator<500000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 2; */
/*     line-dasharray: 6,3,2,3,2,3; */
/*     line-opacity: 0.3; */
/* } */

/* /\* admin_level=6 -->  Kreisgrenze *\/ */
/* .boundary.line[admin_level="6"][scale-denominator<500000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 2; */
/*     line-dasharray: 6,3,2,3; */
/*     line-opacity: 0.3; */
/* } */

/* .boundary.line[admin_level="7"][scale-denominator<200000], */
/* .boundary.line[admin_level="8"][scale-denominator<200000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 1.5; */
/*     line-dasharray: 5,2; */
/*     line-opacity: 0.3; */
/* } */

/* .boundary.line[admin_level="9"][scale-denominator<100000], */
/* .boundary.line[admin_level="10"][scale-denominator<100000] */
/* { */
/*     line-color: #a020f0; */
/*     line-width: 2; */
/*     line-dasharray: 2,3; */
/*     line-opacity: 0.3; */
/* } */


/* /\* #a020f0 = purple *\/ */
/* .boundary.line[scale-denominator>=200000][scale-denominator<2000000] */
/* { */
/* /\*    line-color: #a020f0; *\/ */
/*     line-color: #00ff00; */
/*     line-width: 1; */
/*     line-opacity: 0.2; */
/* } */


/* zoom=10 --> ScaleDenominator=400000 */
/*.boundary.line[scale-denominator<400000][admin_level<=8] 
{
    line-color: #A020F0;
    line-join: round;
    line-width: 1;
    line-dasharray: 2, 3;
    line-opacity: 0.2;
}
*/


.water.label name,
.parklike.label name,
.citylike.label[amenity!=parking] name,
.building.label name
{
    text-face-name: "DejaVu Sans Book";
    text-fill: #000;
    text-placement: point;
    text-halo-radius: 1;
}

.water.label[zoom>=13][zoom<=15][size=large] name,
.parklike.label[zoom>=13][zoom<=15][size=large] name,
.citylike.label[zoom>=13][zoom<=15][size=large][amenity!=parking] name,
.building.label[zoom>=13][zoom<=15][size=large] name,
.water.label[zoom>=15][zoom<=16][size=medium] name,
.parklike.label[zoom>=15][zoom<=16][size=medium] name,
.citylike.label[zoom>=15][zoom<=16][size=medium][amenity!=parking] name,
.building.label[zoom>=15][zoom<=16][size=medium] name,
.water.label[zoom=16][size=small] name,
.parklike.label[zoom=16][size=small] name,
.citylike.label[zoom=16][size=small][amenity!=parking] name,
.building.label[zoom=16][size=small] name
{
    text-size: 9;
    text-wrap-width: 50;
}

.building.label[zoom>=17][amenity=school],
.citylike.label[zoom>=17][amenity=school]
{
    point-file: url('img/icons/24x24/symbol/landmark/amenity=school.png');
    text-dy: 20;
}

.building.label[zoom>=15][zoom<=16][amenity=school],
.citylike.label[zoom>=15][zoom<=16][amenity=school]
{
    point-file: url('img/icons/16x16/symbol/landmark/amenity=school.png');
    text-dy: 18;
}

.building.label[zoom=14][amenity=school],
.citylike.label[zoom=14][amenity=school]
{
    point-file: url('img/icons/12x12/symbol/landmark/amenity=school.png');
}

.building.label[zoom>=17][amenity=police],
.citylike.label[zoom>=17][amenity=police]
{
    point-file: url('img/icons/24x24/symbol/emergency/amenity=police.png');
    text-dy: 20;
}

.building.label[zoom>=15][zoom<=16][amenity=police],
.citylike.label[zoom>=15][zoom<=16][amenity=police]
{
    point-file: url('img/icons/16x16/symbol/emergency/amenity=police.png');
    text-dy: 18;
}

.building.label[zoom=14][amenity=police],
.citylike.label[zoom=14][amenity=police]
{
    point-file: url('img/icons/12x12/symbol/emergency/amenity=police.png');
}

.building.label[zoom>=17][amenity=fire_station],
.citylike.label[zoom>=17][amenity=fire_station]
{
    point-file: url('img/icons/24x24/symbol/emergency/amenity=fire_station.png');
    text-dy: 20;
}

.building.label[zoom>=15][zoom<=16][amenity=fire_station],
.citylike.label[zoom>=15][zoom<=16][amenity=fire_station]
{
    point-file: url('img/icons/16x16/symbol/emergency/amenity=fire_station.png');
    text-dy: 18;
}

.building.label[zoom=14][amenity=fire_station],
.citylike.label[zoom=14][amenity=fire_station]
{
    point-file: url('img/icons/12x12/symbol/emergency/amenity=fire_station.png');
}

.building.label[zoom>=17][amenity=hospital],
.citylike.label[zoom>=17][amenity=hospital]
{
    point-file: url('img/icons/24x24/symbol/emergency/amenity=hospital.png');
    text-dy: 20;
}

.building.label[zoom>=15][zoom<=16][amenity=hospital],
.citylike.label[zoom>=15][zoom<=16][amenity=hospital]
{
    point-file: url('img/icons/16x16/symbol/emergency/amenity=hospital.png');
    text-dy: 18;
}

.building.label[zoom=14][amenity=hospital],
.citylike.label[zoom=14][amenity=hospital]
{
    point-file: url('img/icons/12x12/symbol/emergency/amenity=hospital.png');
}

.building.label[zoom>=17][amenity=parking],
.citylike.label[zoom>=17][amenity=parking]
{
    point-file: url('img/icons/16x16/panel/transport/amenity=parking.png');
}

.water.label[zoom>=16][size=large] name,
.parklike.label[zoom>=16][size=large] name,
.citylike.label[zoom>=16][size=large][amenity!=parking] name,
.building.label[zoom>=16][size=large] name,
.water.label[zoom>=17] name,
.parklike.label[zoom>=17] name,
.citylike.label[zoom>=17][amenity!=parking] name,
.building.label[zoom>=17] name
{
    text-wrap-width: 100;
    text-size: 12;
}

.water.label name
{
    text-fill: #7396bb;
    text-halo-fill: #e7f6fd;
}

.ferry.label[zoom>=13] name
{
    text-face-name: "DejaVu Sans Book";
    text-size: 9;
    text-placement: line;
    text-dy: 5;
    text-fill: #000080; /* navy */
    text-halo-fill: #fff;
}

.parklike.label name
{
/*     text-halo-fill: #d1ffb6; */
    text-halo-fill: #eeeeee;
}

.citylike.label[amenity!=parking] name
{
    text-halo-fill: #eeeeee;
}

.building.label name
{
    text-halo-fill: #eeeeee;
}
