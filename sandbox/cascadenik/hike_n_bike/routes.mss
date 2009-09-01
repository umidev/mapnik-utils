@charset "UTF-8"; /* -*- mode: css; coding: utf-8 -*- */

.route.hiking empty,
.route.hiking_small empty
{
    shield-face-name: "Droid Sans Regular";
    shield-size: 0;
    shield-fill: #777;
}


/* normal-sized icons */
.route.hiking[zoom>=12]
{
    shield-min-distance: 15;
    shield-spacing: 120;
}
.route.hiking[zoom>=14]
{
    shield-min-distance: 30;
    shield-spacing: 210;
}
.route.hiking[zoom>=15]
{
    shield-min-distance: 45;
    shield-spacing: 300;
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[zoom>=12]
{
    shield-min-distance: 5;
    shield-spacing: 40;
}
.route.hiking_small[zoom>=14]
{
    shield-min-distance: 10;
    shield-spacing: 70;
}
.route.hiking_small[zoom>=15]
{
    shield-min-distance: 15;
    shield-spacing: 100;
}




/* normal-sized icons */


.route.hiking[osmc_symbol="red:white:red_bar"][zoom>=12]
{
    shield-file: url('img/red_stripe.8.png');
}

.route.hiking[name="Dresdner Heide, Alte 1"][zoom>=12]
{
    shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Alte1.8.png');
}

.route.hiking[osmc_symbol="red:white:red_bar"][zoom>=14]
{
    shield-file: url('img/red_stripe.10.png');
}
.route.hiking[osmc_symbol="red:white:red_bar"][zoom>=15]
{
    shield-file: url('img/red_stripe.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="red:white:red_bar"][zoom>=12]
{
    shield-file: url('img/red_stripe.5.png');
}
.route.hiking_small[osmc_symbol="red:white:red_bar"][zoom>=14]
{
    shield-file: url('img/red_stripe.6.png');
}
.route.hiking_small[osmc_symbol="red:white:red_bar"][zoom>=15]
{
    shield-file: url('img/red_stripe.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="green:white:green_bar"][zoom>=12]
{
    shield-file: url('img/green_stripe.8.png');
}
.route.hiking[osmc_symbol="green:white:green_bar"][zoom>=14]
{
    shield-file: url('img/green_stripe.10.png');
}
.route.hiking[osmc_symbol="green:white:green_bar"][zoom>=15]
{
    shield-file: url('img/green_stripe.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="green:white:green_bar"][zoom>=12]
{
    shield-file: url('img/green_stripe.5.png');
}
.route.hiking_small[osmc_symbol="green:white:green_bar"][zoom>=14]
{
    shield-file: url('img/green_stripe.6.png');
}
.route.hiking_small[osmc_symbol="green:white:green_bar"][zoom>=15]
{
    shield-file: url('img/green_stripe.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="blue:white:blue_bar"][zoom>=12]
{
    shield-file: url('img/blue_stripe.8.png');
}
.route.hiking[osmc_symbol="blue:white:blue_bar"][zoom>=14]
{
    shield-file: url('img/blue_stripe.10.png');
}
.route.hiking[osmc_symbol="blue:white:blue_bar"][zoom>=15]
{
    shield-file: url('img/blue_stripe.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="blue:white:blue_bar"][zoom>=12]
{
    shield-file: url('img/blue_stripe.5.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_bar"][zoom>=14]
{
    shield-file: url('img/blue_stripe.6.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_bar"][zoom>=15]
{
    shield-file: url('img/blue_stripe.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="yellow:white:yellow_bar"][zoom>=12]
{
    shield-file: url('img/yellow_stripe.8.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_bar"][zoom>=14]
{
    shield-file: url('img/yellow_stripe.10.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_bar"][zoom>=15]
{
    shield-file: url('img/yellow_stripe.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="yellow:white:yellow_bar"][zoom>=12]
{
    shield-file: url('img/yellow_stripe.5.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_bar"][zoom>=14]
{
    shield-file: url('img/yellow_stripe.6.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_bar"][zoom>=15]
{
    shield-file: url('img/yellow_stripe.8.png');
}



/* normal-sized icons */
.route.hiking[osmc_symbol="red:white:red_dot"][zoom>=12]
{
    shield-file: url('img/red_dot.8.png');
}
.route.hiking[osmc_symbol="red:white:red_dot"][zoom>=14]
{
    shield-file: url('img/red_dot.10.png');
}
.route.hiking[osmc_symbol="red:white:red_dot"][zoom>=15]
{
    shield-file: url('img/red_dot.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="red:white:red_dot"][zoom>=12]
{
    shield-file: url('img/red_dot.5.png');
}
.route.hiking_small[osmc_symbol="red:white:red_dot"][zoom>=14]
{
    shield-file: url('img/red_dot.6.png');
}
.route.hiking_small[osmc_symbol="red:white:red_dot"][zoom>=15]
{
    shield-file: url('img/red_dot.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="green:white:green_dot"][zoom>=12]
{
    shield-file: url('img/green_dot.8.png');
}
.route.hiking[osmc_symbol="green:white:green_dot"][zoom>=14]
{
    shield-file: url('img/green_dot.10.png');
}
.route.hiking[osmc_symbol="green:white:green_dot"][zoom>=15]
{
    shield-file: url('img/green_dot.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="green:white:green_dot"][zoom>=12]
{
    shield-file: url('img/green_dot.5.png');
}
.route.hiking_small[osmc_symbol="green:white:green_dot"][zoom>=14]
{
    shield-file: url('img/green_dot.6.png');
}
.route.hiking_small[osmc_symbol="green:white:green_dot"][zoom>=15]
{
    shield-file: url('img/green_dot.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="blue:white:blue_dot"][zoom>=12]
{
    shield-file: url('img/blue_dot.8.png');
}
.route.hiking[osmc_symbol="blue:white:blue_dot"][zoom>=14]
{
    shield-file: url('img/blue_dot.10.png');
}
.route.hiking[osmc_symbol="blue:white:blue_dot"][zoom>=15]
{
    shield-file: url('img/blue_dot.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="blue:white:blue_dot"][zoom>=12]
{
    shield-file: url('img/blue_dot.5.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_dot"][zoom>=14]
{
    shield-file: url('img/blue_dot.6.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_dot"][zoom>=15]
{
    shield-file: url('img/blue_dot.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="yellow:white:yellow_dot"][zoom>=12]
{
    shield-file: url('img/yellow_dot.8.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_dot"][zoom>=14]
{
    shield-file: url('img/yellow_dot.10.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_dot"][zoom>=15]
{
    shield-file: url('img/yellow_dot.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="yellow:white:yellow_dot"][zoom>=12]
{
    shield-file: url('img/yellow_dot.5.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_dot"][zoom>=14]
{
    shield-file: url('img/yellow_dot.6.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_dot"][zoom>=15]
{
    shield-file: url('img/yellow_dot.8.png');
}



/* normal-sized icons */
.route.hiking[osmc_symbol="red:white:red_triangle"][zoom>=12]
{
    shield-file: url('img/red_triangle.8.png');
}
.route.hiking[osmc_symbol="red:white:red_triangle"][zoom>=14]
{
    shield-file: url('img/red_triangle.10.png');
}
.route.hiking[osmc_symbol="red:white:red_triangle"][zoom>=15]
{
    shield-file: url('img/red_triangle.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="red:white:red_triangle"][zoom>=12]
{
    shield-file: url('img/red_triangle.5.png');
}
.route.hiking_small[osmc_symbol="red:white:red_triangle"][zoom>=14]
{
    shield-file: url('img/red_triangle.6.png');
}
.route.hiking_small[osmc_symbol="red:white:red_triangle"][zoom>=15]
{
    shield-file: url('img/red_triangle.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="green:white:green_triangle"][zoom>=12]
{
    shield-file: url('img/green_triangle.8.png');
}
.route.hiking[osmc_symbol="green:white:green_triangle"][zoom>=14]
{
    shield-file: url('img/green_triangle.10.png');
}
.route.hiking[osmc_symbol="green:white:green_triangle"][zoom>=15]
{
    shield-file: url('img/green_triangle.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="green:white:green_triangle"][zoom>=12]
{
    shield-file: url('img/green_triangle.5.png');
}
.route.hiking_small[osmc_symbol="green:white:green_triangle"][zoom>=14]
{
    shield-file: url('img/green_triangle.6.png');
}
.route.hiking_small[osmc_symbol="green:white:green_triangle"][zoom>=15]
{
    shield-file: url('img/green_triangle.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="blue:white:blue_triangle"][zoom>=12]
{
    shield-file: url('img/blue_triangle.8.png');
}
.route.hiking[osmc_symbol="blue:white:blue_triangle"][zoom>=14]
{
    shield-file: url('img/blue_triangle.10.png');
}
.route.hiking[osmc_symbol="blue:white:blue_triangle"][zoom>=15]
{
    shield-file: url('img/blue_triangle.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="blue:white:blue_triangle"][zoom>=12]
{
    shield-file: url('img/blue_triangle.5.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_triangle"][zoom>=14]
{
    shield-file: url('img/blue_triangle.6.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_triangle"][zoom>=15]
{
    shield-file: url('img/blue_triangle.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="yellow:white:yellow_triangle"][zoom>=12]
{
    shield-file: url('img/yellow_triangle.8.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_triangle"][zoom>=14]
{
    shield-file: url('img/yellow_triangle.10.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_triangle"][zoom>=15]
{
    shield-file: url('img/yellow_triangle.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="yellow:white:yellow_triangle"][zoom>=12]
{
    shield-file: url('img/yellow_triangle.5.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_triangle"][zoom>=14]
{
    shield-file: url('img/yellow_triangle.6.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_triangle"][zoom>=15]
{
    shield-file: url('img/yellow_triangle.8.png');
}



/* normal-sized icons */
.route.hiking[osmc_symbol="red:white:red_pipe"][zoom>=12],
.route.hiking[osmc_symbol="red:white:|"][zoom>=12]
{
    shield-file: url('img/red_pipe.8.png');
}
.route.hiking[osmc_symbol="red:white:red_pipe"][zoom>=14],
.route.hiking[osmc_symbol="red:white:|"][zoom>=14]
{
    shield-file: url('img/red_pipe.10.png');
}
.route.hiking[osmc_symbol="red:white:red_pipe"][zoom>=15],
.route.hiking[osmc_symbol="red:white:|"][zoom>=15]
{
    shield-file: url('img/red_pipe.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="red:white:red_pipe"][zoom>=12],
.route.hiking_small[osmc_symbol="red:white:|"][zoom>=12]
{
    shield-file: url('img/red_pipe.5.png');
}
.route.hiking_small[osmc_symbol="red:white:red_pipe"][zoom>=14],
.route.hiking_small[osmc_symbol="red:white:|"][zoom>=14]
{
    shield-file: url('img/red_pipe.6.png');
}
.route.hiking_small[osmc_symbol="red:white:red_pipe"][zoom>=15],
.route.hiking_small[osmc_symbol="red:white:|"][zoom>=15]
{
    shield-file: url('img/red_pipe.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="green:white:green_pipe"][zoom>=12],
.route.hiking[osmc_symbol="green:white:|"][zoom>=12]
{
    shield-file: url('img/green_pipe.8.png');
}
.route.hiking[osmc_symbol="green:white:green_pipe"][zoom>=14],
.route.hiking[osmc_symbol="green:white:|"][zoom>=14]
{
    shield-file: url('img/green_pipe.10.png');
}
.route.hiking[osmc_symbol="green:white:green_pipe"][zoom>=15],
.route.hiking[osmc_symbol="green:white:|"][zoom>=15]
{
    shield-file: url('img/green_pipe.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="green:white:green_pipe"][zoom>=12],
.route.hiking_small[osmc_symbol="green:white:|"][zoom>=12]
{
    shield-file: url('img/green_pipe.5.png');
}
.route.hiking_small[osmc_symbol="green:white:green_pipe"][zoom>=14],
.route.hiking_small[osmc_symbol="green:white:|"][zoom>=14]
{
    shield-file: url('img/green_pipe.6.png');
}
.route.hiking_small[osmc_symbol="green:white:green_pipe"][zoom>=15],
.route.hiking_small[osmc_symbol="green:white:|"][zoom>=15]
{
    shield-file: url('img/green_pipe.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="blue:white:blue_pipe"][zoom>=12],
.route.hiking[osmc_symbol="blue:white:|"][zoom>=12]
{
    shield-file: url('img/blue_pipe.8.png');
}
.route.hiking[osmc_symbol="blue:white:blue_pipe"][zoom>=14],
.route.hiking[osmc_symbol="blue:white:|"][zoom>=14]
{
    shield-file: url('img/blue_pipe.10.png');
}
.route.hiking[osmc_symbol="blue:white:blue_pipe"][zoom>=15],
.route.hiking[osmc_symbol="blue:white:|"][zoom>=15]
{
    shield-file: url('img/blue_pipe.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="blue:white:blue_pipe"][zoom>=12],
.route.hiking_small[osmc_symbol="blue:white:|"][zoom>=12]
{
    shield-file: url('img/blue_pipe.5.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_pipe"][zoom>=14],
.route.hiking_small[osmc_symbol="blue:white:|"][zoom>=14]
{
    shield-file: url('img/blue_pipe.6.png');
}
.route.hiking_small[osmc_symbol="blue:white:blue_pipe"][zoom>=15],
.route.hiking_small[osmc_symbol="blue:white:|"][zoom>=15]
{
    shield-file: url('img/blue_pipe.8.png');
}


/* normal-sized icons */
.route.hiking[osmc_symbol="yellow:white:yellow_pipe"][zoom>=12],
.route.hiking[osmc_symbol="yellow:white:|"][zoom>=12]
{
    shield-file: url('img/yellow_pipe.8.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_pipe"][zoom>=14],
.route.hiking[osmc_symbol="yellow:white:|"][zoom>=14]
{
    shield-file: url('img/yellow_pipe.10.png');
}
.route.hiking[osmc_symbol="yellow:white:yellow_pipe"][zoom>=15],
.route.hiking[osmc_symbol="yellow:white:|"][zoom>=15]
{
    shield-file: url('img/yellow_pipe.12.png');
}

/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="yellow:white:yellow_pipe"][zoom>=12],
.route.hiking_small[osmc_symbol="yellow:white:|"][zoom>=12]
{
    shield-file: url('img/yellow_pipe.5.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_pipe"][zoom>=14],
.route.hiking_small[osmc_symbol="yellow:white:|"][zoom>=14]
{
    shield-file: url('img/yellow_pipe.6.png');
}
.route.hiking_small[osmc_symbol="yellow:white:yellow_pipe"][zoom>=15],
.route.hiking_small[osmc_symbol="yellow:white:|"][zoom>=15]
{
    shield-file: url('img/yellow_pipe.8.png');
}



/* normal-sized icons */
.route.hiking[osmc_symbol="green:white:green_backslash"][zoom>=12],
.route.hiking[osmc_symbol="green:white:#x5c"][zoom>=12]
{
    shield-file: url('img/green_backslash.8.png');
}
.route.hiking[osmc_symbol="green:white:green_backslash"][zoom>=14],
.route.hiking[osmc_symbol="green:white:#x5c"][zoom>=14]
{
    shield-file: url('img/green_backslash.10.png');
}
.route.hiking[osmc_symbol="green:white:green_backslash"][zoom>=15],
.route.hiking[osmc_symbol="green:white:#x5c"][zoom>=15]
{
    shield-file: url('img/green_backslash.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="green:white:green_backslash"][zoom>=12],
.route.hiking_small[osmc_symbol="green:white:#x5c"][zoom>=12]
{
    shield-file: url('img/green_backslash.5.png');
}
.route.hiking_small[osmc_symbol="green:white:green_backslash"][zoom>=14],
.route.hiking_small[osmc_symbol="green:white:#x5c"][zoom>=14]
{
    shield-file: url('img/green_backslash.6.png');
}
.route.hiking_small[osmc_symbol="green:white:green_backslash"][zoom>=15],
.route.hiking_small[osmc_symbol="green:white:#x5c"][zoom>=15]
{
    shield-file: url('img/green_backslash.8.png');
}



/* normal-sized icons */
.route.hiking[osmc_symbol="green:white:green_slash"][zoom>=12],
.route.hiking[osmc_symbol="green:white:/"][zoom>=12]
{
    shield-file: url('img/green_slash.8.png');
}
.route.hiking[osmc_symbol="green:white:green_slash"][zoom>=14],
.route.hiking[osmc_symbol="green:white:/"][zoom>=14]
{
    shield-file: url('img/green_slash.10.png');
}
.route.hiking[osmc_symbol="green:white:green_slash"][zoom>=15],
.route.hiking[osmc_symbol="green:white:/"][zoom>=15]
{
    shield-file: url('img/green_slash.12.png');
}


/* small icons for inbetween the bigger ones */
.route.hiking_small[osmc_symbol="green:white:green_slash"][zoom>=12],
.route.hiking_small[osmc_symbol="green:white:/"][zoom>=12]
{
    shield-file: url('img/green_slash.5.png');
}
.route.hiking_small[osmc_symbol="green:white:green_slash"][zoom>=14],
.route.hiking_small[osmc_symbol="green:white:/"][zoom>=14]
{
    shield-file: url('img/green_slash.6.png');
}
.route.hiking_small[osmc_symbol="green:white:green_slash"][zoom>=15],
.route.hiking_small[osmc_symbol="green:white:/"][zoom>=15]
{
    shield-file: url('img/green_slash.8.png');
}



.path[name="Kletterzustieg"] name
{
    shield-face-name: "Droid Sans Regular";
    shield-size: 0;
    shield-fill: #777;
}

/* .path[name="Kletterzustieg"][zoom>=12], */
/* .path[path=climbing_access][zoom>=12] */
/* { */
/*     shield-file: url('img/black_triangle_right_circle2.8.png'); */
/*     shield-min-distance: 31; */
/*     shield-spacing: 31; */
/* } */
.path[name="Kletterzustieg"][zoom>=14],
.path[path=climbing_access][zoom>=14]
{
    shield-file: url('img/black_triangle_right_circle2.8.png');
    shield-min-distance: 41;
    shield-spacing: 41;
}
.path[name="Kletterzustieg"][zoom>=15],
.path[path=climbing_access][zoom>=15]
{
    shield-file: url('img/black_triangle_right_circle2.10.png');
    shield-min-distance: 61;
    shield-spacing: 61;
}



.path[path=mountain_path] name
{
    shield-face-name: "Droid Sans Regular";
    shield-size: 0;
    shield-fill: #777;
}

/* .path[path=mountain_path][zoom>=12] */
/* { */
/*     shield-file: url('img/green_triangle_right_circle.8.png'); */
/*     shield-min-distance: 31; */
/*     shield-spacing: 31; */
/* } */
.path[path=mountain_path][zoom>=14]
{
    shield-file: url('img/green_triangle_right_circle.8.png');
    shield-min-distance: 41;
    shield-spacing: 41;
}
.path[path=mountain_path][zoom>=15]
{
    shield-file: url('img/green_triangle_right_circle.10.png');
    shield-min-distance: 61;
    shield-spacing: 61;
}

/*
gesperrt: black_X_circle.10.png
*/