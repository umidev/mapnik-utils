.text
{
    /* This is the query field you want to use for the label text, ie "street_name" */
    text-name: (use selector for this);

    /* Font name */
    text-face-name: string;

    /* Font size */
    text-size: number;

    /* ? */
    text-ratio: ?;

    /* length before wrapping long names */
    text-wrap-width: number;

    /* space between repeated labels */
    text-spacing: number;

    /* allow labels to be moved from their point */
    text-label-position-tolerance: ?;

    /* Maximum angle (in degrees) between two consecutive characters in a label allowed (to stop placing labels around sharp corners) */
    text-max-char-angle-delta: number;

    /* Color of the fill ie #FFFFFF */
    text-fill: hex color;

    /* Color of the halo */
    text-halo-fill: hex color;

    /* Radius of the halo in whole pixels, fractional pixels are not accepted */
    text-halo-radius: number;

    /* displace label by fixed amount on either axis. */
    text-dx: number;
    text-dy: number;

    /* Boolean to avoid labeling near intersection edges. */
    text-avoid-edges: ?;

    /* Minimum distance between repeated labels such as street names or shield symbols */
    text-min-distance: number;

    /* Allow labels to overlap other labels */
    text-allow-overlap: ...;

    /* "line" to label along lines instead of by point */
    text-placement: point, line, ?;
}

.line
{
    /* CSS colour (default "black") */
    line-color: hex color;

    /* 0.0 - n (default 1.0) */
    line-width: number;

    /* 0.0 - 1.0 (default 1.0) */
    line-opacity: number;

    /* miter, round, bevel (default miter) */
    line-join: miter, round, bevel;

    /* round, butt, square (default butt) */
    line-cap: round, butt, square;

    /* d0,d1, ... (default none) */
    line-dasharray: number(s);
}

.polygon
{
    /*  */
    polygon-fill: hex color;

    /*  */
    polygon-opacity: number;
}

.shield
{
    /*  */
    shield-name: (use selector for this);

    /*  */
    shield-face-name: string;

    /*  */
    shield-size: ?;

    /*  */
    shield-fill: hex color?;

    /*  */
    shield-file: url;

    /*  */
    shield-type: png, tiff (derived from file);

    /*  */
    shield-width: number;

    /*  */
    shield-height: number;
}

.pattern
{
    /* path to image file (default none) */
    pattern-file: url;

    /* px (default 4) */
    pattern-width: number;

    /* px (default 4) */
    pattern-height: number;

    /* png tiff (default none) */
    pattern-type: png, tiff (derived from file);
}
