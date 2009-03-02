@charset "UTF-8";
/* -*- mode: css; coding: utf-8 -*- */

.route.hiking name
{
    shield-face-name: "DejaVu Sans Book";
    shield-size: 0;
    shield-fill: #070;
}

/*
.route.hiking[zoom>=12]
{
    shield-min-distance: 55;
    shield-spacing: 55;
}
.route.hiking[zoom>=14]
{
    shield-min-distance: 120;
    shield-spacing: 120;
}
.route.hiking[zoom>=15]
{
    shield-min-distance: 160;
    shield-spacing: 160;
}
*/
.route.hiking[zoom>=12]
{
    shield-min-distance: 2;
    shield-spacing: 22;
}
.route.hiking[zoom>=14]
{
    shield-min-distance: 5;
    shield-spacing: 55;
}
.route.hiking[zoom>=15]
{
    shield-min-distance: 8;
    shield-spacing: 88;
}


.route.hiking[name="Roter Strich"][zoom>=12],
.route.hiking[name="Roter Balken"][zoom>=12],
.route.hiking[symbol="Roter Strich"][zoom>=12],
.route.hiking[osmc_symbol="red:white:red_bar"][zoom>=12]
{
    shield-file: url('img/red_stripe.8.png');
}
.route.hiking[name="Roter Strich"][zoom>=14],
.route.hiking[name="Roter Balken"][zoom>=14],
.route.hiking[symbol="Roter Strich"][zoom>=14],
.route.hiking[osmc_symbol="red:white:red_bar"][zoom>=14]
{
    shield-file: url('img/red_stripe.10.png');
}
.route.hiking[name="Roter Strich"][zoom>=15],
.route.hiking[name="Roter Balken"][zoom>=15],
.route.hiking[symbol="Roter Strich"][zoom>=15],
.route.hiking[osmc_symbol="red:white:red_bar"][zoom>=15]
{
    shield-file: url('img/red_stripe.12.png');
}


.route.hiking[name="Grxxxuener Strich"][zoom>=12],
.route.hiking[name="Grxxxuener Balken"][zoom>=12],
.route.hiking[symbol="Grxxxuener Strich"][zoom>=12],
.route.hiking[osmc_symbol="green:white:green_bar"][zoom>=12]
{
    shield-file: url('img/green_stripe.8.png');
}
.route.hiking[name="Grxxxuener Strich"][zoom>=14],
.route.hiking[name="Grxxxuener Balken"][zoom>=14],
.route.hiking[symbol="Grxxxuener Strich"][zoom>=14],
.route.hiking[osmc_symbol="green:white:green_bar"][zoom>=14]
{
    shield-file: url('img/green_stripe.10.png');
}
.route.hiking[name="Grxxxuener Strich"][zoom>=15],
.route.hiking[name="Grxxxuener Balken"][zoom>=15],
.route.hiking[symbol="Grxxxuener Strich"][zoom>=15],
.route.hiking[osmc_symbol="green:white:green_bar"][zoom>=15]
{
    shield-file: url('img/green_stripe.12.png');
}


.route.hiking[name="Blauer Strich"][zoom>=12],
.route.hiking[name="Blauer Balken"][zoom>=12],
.route.hiking[symbol="Blauer Strich"][zoom>=12],
.route.hiking[osmc_symbol="blue:white:blue_bar"][zoom>=12]
{
    shield-file: url('img/blue_stripe.8.png');
}
.route.hiking[name="Blauer Strich"][zoom>=14],
.route.hiking[name="Blauer Balken"][zoom>=14],
.route.hiking[symbol="Blauer Strich"][zoom>=14],
.route.hiking[osmc_symbol="blue:white:blue_bar"][zoom>=14]
{
    shield-file: url('img/blue_stripe.10.png');
}
.route.hiking[name="Blauer Strich"][zoom>=15],
.route.hiking[name="Blauer Balken"][zoom>=15],
.route.hiking[symbol="Blauer Strich"][zoom>=15],
.route.hiking[osmc_symbol="blue:white:blue_bar"][zoom>=15]
{
    shield-file: url('img/blue_stripe.12.png');
}


.route.hiking[name="Gelber Strich"][zoom>=12],
.route.hiking[name="Gelber Balken"][zoom>=12],
.route.hiking[symbol="Gelber Strich"][zoom>=12],
.route.hiking[osmc_symbol="yellow:white:yellow_bar"][zoom>=12]
{
    shield-file: url('img/yellow_stripe.8.png');
}
.route.hiking[name="Gelber Strich"][zoom>=14],
.route.hiking[name="Gelber Balken"][zoom>=14],
.route.hiking[symbol="Gelber Strich"][zoom>=14],
.route.hiking[osmc_symbol="yellow:white:yellow_bar"][zoom>=14]
{
    shield-file: url('img/yellow_stripe.10.png');
}
.route.hiking[name="Gelber Strich"][zoom>=15],
.route.hiking[name="Gelber Balken"][zoom>=15],
.route.hiking[symbol="Gelber Strich"][zoom>=15],
.route.hiking[osmc_symbol="yellow:white:yellow_bar"][zoom>=15]
{
    shield-file: url('img/yellow_stripe.12.png');
}



.route.hiking[name="Roter Punkt"][zoom>=12],
.route.hiking[symbol="Roter Punkt"][zoom>=12],
.route.hiking[osmc_symbol="red:white:red_dot"][zoom>=12]
{
    shield-file: url('img/red_dot.8.png');
}
.route.hiking[name="Roter Punkt"][zoom>=14],
.route.hiking[symbol="Roter Punkt"][zoom>=14],
.route.hiking[osmc_symbol="red:white:red_dot"][zoom>=14]
{
    shield-file: url('img/red_dot.10.png');
}
.route.hiking[name="Roter Punkt"][zoom>=15],
.route.hiking[symbol="Roter Punkt"][zoom>=15],
.route.hiking[osmc_symbol="red:white:red_dot"][zoom>=15]
{
    shield-file: url('img/red_dot.12.png');
}


.route.hiking[name="Grxxxuener Punkt"][zoom>=12],
.route.hiking[symbol="Grxxxuener Punkt"][zoom>=12],
.route.hiking[osmc_symbol="green:white:green_dot"][zoom>=12]
{
    shield-file: url('img/green_dot.8.png');
}
.route.hiking[name="Grxxxuener Punkt"][zoom>=14],
.route.hiking[symbol="Grxxxuener Punkt"][zoom>=14],
.route.hiking[osmc_symbol="green:white:green_dot"][zoom>=14]
{
    shield-file: url('img/green_dot.10.png');
}
.route.hiking[name="Grxxxuener Punkt"][zoom>=15],
.route.hiking[symbol="Grxxxuener Punkt"][zoom>=15],
.route.hiking[osmc_symbol="green:white:green_dot"][zoom>=15]
{
    shield-file: url('img/green_dot.12.png');
}


.route.hiking[name="Blauer Punkt"][zoom>=12],
.route.hiking[symbol="Blauer Punkt"][zoom>=12],
.route.hiking[osmc_symbol="blue:white:blue_dot"][zoom>=12]
{
    shield-file: url('img/blue_dot.8.png');
}
.route.hiking[name="Blauer Punkt"][zoom>=14],
.route.hiking[symbol="Blauer Punkt"][zoom>=14],
.route.hiking[osmc_symbol="blue:white:blue_dot"][zoom>=14]
{
    shield-file: url('img/blue_dot.10.png');
}
.route.hiking[name="Blauer Punkt"][zoom>=15],
.route.hiking[symbol="Blauer Punkt"][zoom>=15],
.route.hiking[osmc_symbol="blue:white:blue_dot"][zoom>=15]
{
    shield-file: url('img/blue_dot.12.png');
}


.route.hiking[name="Gelber Punkt"][zoom>=12],
.route.hiking[symbol="Gelber Punkt"][zoom>=12],
.route.hiking[osmc_symbol="yellow:white:yellow_dot"][zoom>=12]
{
    shield-file: url('img/yellow_dot.8.png');
}
.route.hiking[name="Gelber Punkt"][zoom>=14],
.route.hiking[symbol="Gelber Punkt"][zoom>=14],
.route.hiking[osmc_symbol="yellow:white:yellow_dot"][zoom>=14]
{
    shield-file: url('img/yellow_dot.10.png');
}
.route.hiking[name="Gelber Punkt"][zoom>=15],
.route.hiking[symbol="Gelber Punkt"][zoom>=15],
.route.hiking[osmc_symbol="yellow:white:yellow_dot"][zoom>=15]
{
    shield-file: url('img/yellow_dot.12.png');
}







.path[name="Kletterzustieg"]
{
    shield-face-name: "DejaVu Sans Book";
    shield-size: 0;
    shield-fill: #070;
}

.path[name="Kletterzustieg"][zoom>=12] name
{
    shield-file: url('img/green_triangle_right.8.png');
    shield-min-distance: 31;
    shield-spacing: 31;
}
.path[name="Kletterzustieg"][zoom>=14] name
{
    shield-file: url('img/green_triangle_right.8.png');
    shield-min-distance: 41;
    shield-spacing: 41;
}
.path[name="Kletterzustieg"][zoom>=15] name
{
    shield-file: url('img/green_triangle_right.10.png');
    shield-min-distance: 61;
    shield-spacing: 61;
}
