.text
{
    /* This is the query field you want to use for the label text, ie "street_name" */
    text-name: ...;

    /* Font name */
    text-face-name: ...;

    /* Font size */
    text-size: ...;

    /* ? */
    text-ratio: ...;

    /* length before wrapping long names */
    text-wrap-width: ...;

    /* space between repeated labels */
    text-spacing: ...;

    /* allow labels to be moved from their point */
    text-label-position-tolerance: ...;

    /* Maximum angle (in degrees) between two consecutive characters in a label allowed (to stop placing labels around sharp corners) */
    text-max-char-angle-delta: ...;

    /* Color of the fill ie #FFFFFF */
    text-fill: ...;

    /* Color of the halo */
    text-halo-fill: ...;

    /* Radius of the halo in whole pixels, fractional pixels are not accepted */
    text-halo-radius: ...;

    /* displace label by fixed amount on either axis. */
    text-dx: ...;
    text-dy: ...;

    /* Boolean to avoid labeling near intersection edges. */
    text-avoid-edges: ...;

    /* Minimum distance between repeated labels such as street names or shield symbols */
    text-min-distance: ...;

    /* Allow labels to overlap other labels */
    text-allow-overlap: ...;

    /* "line" to label along lines instead of by point */
    text-placement: ...;
}

.line
{
    /* CSS colour (default "black") */
    line-color: ...;

    /* 0.0 - n (default 1.0) */
    line-width: ...;

    /* 0.0 - 1.0 (default 1.0) */
    line-opacity: ...;

    /* miter, round, bevel (default miter) */
    line-join: ...;

    /* round, butt, square (default butt) */
    line-cap: ...;

    /* d0,d1, ... (default none) */
    line-dasharray: ...;
}

.polygon
{
    /*  */
    polygon-fill: ...;

    /*  */
    polygon-opacity: ...;
}

.shield
{
    /*  */
    shield-name: ...;

    /*  */
    shield-face-name: ...;

    /*  */
    shield-size: ...;

    /*  */
    shield-fill: ...;

    /*  */
    shield-file: ...;

    /*  */
    shield-type: ...;

    /*  */
    shield-width: ...;

    /*  */
    shield-height: ...;
}

.pattern
{
    /* path to image file (default none) */
    pattern-file: ...;

    /* px (default 4) */
    pattern-width: ...;

    /* px (default 4) */
    pattern-height: ...;

    /* png tiff (default none) */
    pattern-type: ...;
}
