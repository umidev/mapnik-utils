<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:output method="html" encoding="utf-8" omit-xml-declaration="no" indent="yes"/>

    <xsl:variable name="PolygonSymbolizer" select="'&#x2003;'"/>
    <xsl:variable name="PolygonPatternSymbolizer" select="'&#x25a8;'"/>
    <xsl:variable name="LineSymbolizer" select="'&#x2621;'"/>
    <xsl:variable name="LinePatternSymbolizer" select="'&#x2197;'"/>
    <xsl:variable name="PointSymbolizer" select="'&#x2691;'"/>
    <xsl:variable name="ShieldSymbolizer" select="'&#x25a2;'"/>
    <xsl:variable name="TextSymbolizer" select="'T'"/>

    <xsl:template match="/">
        <html>
            <head>
                <title>Mapnik Map File Overview</title>
                <meta http-equiv="content-type" content="text/html; charset=utf-8" />
                <style type="text/css">
body {
    font-family: Helvetica, Arial, sans-serif;
}

table.overview {
    width: 100%;
    border-collapse: collapse;
}

table.overview th {
    text-align: right;
    background-color: #e0e0e0;
    padding: 2px;
}

table.overview td {
    background-color: #f0f0f0;
    padding: 2px;
}

table.layer {
    width: 100%;
    border-collapse: collapse;
    border-left: 10px solid #e0e0e0;
}

table.layer td {
    vertical-align: top;
    padding: 2px;
}

table.layer tr.layer td {
    border-top: 20px solid #ffffff;
    background-color: #e0e0e0;
}

table.layer tr.layer td.name {
    font-weight: bold;
    white-space: nowrap;
}

table.layer tr.datasource td {
    background-color: #f0f0f0;
}

table.layer tr.style td {
    background-color: #f8f8f8;
}

div.style {
    margin-left: 30px;
}

div.rules {
    margin-left: 60px;
}

table.rules {
    width: 100%;
    border-collapse: collapse;
}

table.rules td {
    vertical-align: top;
    padding: 2px;
}

table.rules td.num {
    vertical-align: top;
    text-align: right;
}

table.rules td.max {
    width: 8em;
}

table.rules td.min {
    width: 6em;
}

table.rules td.sym {
    width: 1em;
    text-align: center;
}

div.popup table.popup {
   display: none;
}

div.popup:hover span.anchor {
    color: #e00000;
}

div.popup:hover table.popup {
    display: block;
    position: absolute;
    margin-left: 10px;
    z-index: 100;
    color: #000000;
    background-color: #f0f000;
    border: 1px solid #ffffff;
    text-align: left;
    border-collapse: collapse;
}

div.popup table.popup th {
    text-align: right;
    background-color: #e8e800;
    color: #000000;
    font-weight: normal;
    padding: 2px;
    width: 20%;
    white-space: nowrap;
    vertical-align: top;
}

div.popup table.popup th.title {
    text-align: left;
    font-weight: bold;
}

div.popup table.popup td {
    padding: 2px;
    background-color: #f0f000;
}

                </style>
            </head>
            <body>
                <xsl:apply-templates select="Map"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="Map">
        <h1>Mapnik Map File</h1>
        <table class="overview">
            <tr>
                <th>SRS:</th><td><xsl:value-of select="@srs"/></td>
            </tr>
            <tr>
                <th>Background:</th><td><span style="background-color: {@bgcolor}"><xsl:value-of select="@bgcolor"/></span></td>
            </tr>
        </table>
        <h2>Layer:</h2>
        <p>Only styles referenced in layers will be shown.</p>
        <table class="layer">
            <xsl:apply-templates select="Layer"/>
        </table>
    </xsl:template>

    <xsl:template match="Layer">
        <tr class="layer">
            <td class="name"><xsl:value-of select="@name"/></td>
            <td>SRS <xsl:value-of select="@srs"/></td>
        </tr>
        <tr class="datasource">
            <td></td>
            <td>
                <xsl:apply-templates select="Datasource"/>
            </td>
        </tr>
        <xsl:apply-templates select="StyleName"/>
    </xsl:template>

    <xsl:template match="Datasource">
        <xsl:choose>
            <xsl:when test="Parameter[@name='type'][text()='shape']">
                <xsl:text>SHAPE </xsl:text><xsl:value-of select="Parameter[@name='file']/text()"/>
            </xsl:when>
            <xsl:when test="Parameter[@name='type'][text()='postgis']">
                <xsl:text>POSTGIS </xsl:text><xsl:value-of select="Parameter[@name='table']/text()"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="Parameter[@name='type']"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="StyleName">
        <tr class="style">
            <td colspan="2">
                <div class="style"><xsl:value-of select="text()"/></div>
                <xsl:variable name="style" select="text()"/>
                <xsl:apply-templates select="/Map/Style[@name=$style]"/>
            </td>
        </tr>
    </xsl:template>

    <xsl:template match="Style">
        <div class="rules">
            <table class="rules">
                <xsl:apply-templates select="Rule"/>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="Rule">
        <tr>
            <td class="num max"><xsl:value-of select="translate(format-number(MaxScaleDenominator/text(), '###,###,###,###'), ',', '&#x00a0;')"/></td>
            <td class="num min"><xsl:value-of select="translate(format-number(concat('0', MinScaleDenominator/text()), '###,###,###,###'), ',', '&#x00a0;')"/></td>
            <td class="sym"><xsl:apply-templates select="PolygonSymbolizer"/><xsl:apply-templates select="PolygonPatternSymbolizer"/></td>
            <td class="sym"><xsl:apply-templates select="LineSymbolizer"/><xsl:apply-templates select="LinePatternSymbolizer"/></td>
            <td class="sym"><xsl:apply-templates select="PointSymbolizer"/></td>
            <td class="sym"><xsl:apply-templates select="ShieldSymbolizer"/></td>
            <td class="sym"><xsl:apply-templates select="TextSymbolizer"/></td>

            <td>
                <xsl:choose>
                    <xsl:when test="ElseFilter">
                        <i>else</i>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="Filter/text()"/>
                    </xsl:otherwise>
                </xsl:choose>
            </td>
        </tr>
    </xsl:template>

    <xsl:template match="PolygonSymbolizer">
        <div class="popup">
            <span class="anchor" style="background-color: {CssParameter[@name='fill']/text()}"><xsl:value-of select="$PolygonSymbolizer"/></span>
            <table class="popup">
                <tr><th colspan="2" class="title"><xsl:value-of select="$PolygonSymbolizer"/> PolygonSymbolizer</th></tr>
                <tr><th>fill:</th><td><xsl:value-of select="CssParameter[@name='fill']/text()"/></td></tr>
                <tr><th>fill-opacity:</th><td><xsl:value-of select="CssParameter[@name='fill-opacity']/text()"/></td></tr>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="PolygonPatternSymbolizer">
        <div class="popup">
            <span class="anchor"><xsl:value-of select="$PolygonPatternSymbolizer"/></span>
            <table class="popup">
                <tr><th colspan="2" class="title"><xsl:value-of select="$PolygonPatternSymbolizer"/> PolygonPatternSymbolizer</th></tr>
                <tr><th></th><td><img src="{@file}"/></td></tr>
                <tr><th>file:</th><td><xsl:value-of select="@file"/></td></tr>
                <tr><th>height:</th><td><xsl:value-of select="@height"/></td></tr>
                <tr><th>type:</th><td><xsl:value-of select="@type"/></td></tr>
                <tr><th>width:</th><td><xsl:value-of select="@width"/></td></tr>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="LineSymbolizer">
        <div class="popup">
            <span class="anchor" style="color: {CssParameter[@name='stroke']/text()};"><xsl:value-of select="$LineSymbolizer"/></span>
            <table class="popup">
                <tr><th colspan="2" class="title"><xsl:value-of select="$LineSymbolizer"/> LineSymbolizer</th></tr>
                <tr><th>stroke:</th><td><xsl:value-of select="CssParameter[@name='stroke']/text()"/></td></tr>
                <tr><th>stroke-dasharray:</th><td><xsl:value-of select="CssParameter[@name='stroke-dasharray']/text()"/></td></tr>
                <tr><th>stroke-linecap:</th><td><xsl:value-of select="CssParameter[@name='stroke-linecap']/text()"/></td></tr>
                <tr><th>stroke-linejoin:</th><td><xsl:value-of select="CssParameter[@name='stroke-linejoin']/text()"/></td></tr>
                <tr><th>stroke-width:</th><td><xsl:value-of select="CssParameter[@name='stroke-width']/text()"/></td></tr>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="LinePatternSymbolizer">
        <div class="popup">
            <span class="anchor"><xsl:value-of select="$LinePatternSymbolizer"/></span>
            <table class="popup">
                <tr><th colspan="2" class="title"><xsl:value-of select="$LinePatternSymbolizer"/> LinePatternSymbolizer</th></tr>
                <tr><th></th><td><img src="{@file}"/></td></tr>
                <tr><th>file:</th><td><xsl:value-of select="@file"/></td></tr>
                <tr><th>height:</th><td><xsl:value-of select="@height"/></td></tr>
                <tr><th>type:</th><td><xsl:value-of select="@type"/></td></tr>
                <tr><th>width:</th><td><xsl:value-of select="@width"/></td></tr>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="PointSymbolizer">
        <div class="popup">
            <span class="anchor"><xsl:value-of select="$PointSymbolizer"/></span>
            <table class="popup">
                <tr><th colspan="2" class="title"><xsl:value-of select="$PointSymbolizer"/> PointSymbolizer</th></tr>
                <tr><th></th><td><img src="{@file}"/></td></tr>
                <tr><th>allow_overlap:</th><td><xsl:value-of select="@allow_overlap"/></td></tr>
                <tr><th>file:</th><td><xsl:value-of select="@file"/></td></tr>
                <tr><th>height:</th><td><xsl:value-of select="@height"/></td></tr>
                <tr><th>type:</th><td><xsl:value-of select="@type"/></td></tr>
                <tr><th>width:</th><td><xsl:value-of select="@width"/></td></tr>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="ShieldSymbolizer">
        <div class="popup">
            <span class="anchor"><xsl:value-of select="$ShieldSymbolizer"/></span>
            <table class="popup">
                <tr><th colspan="2" class="title"><xsl:value-of select="$ShieldSymbolizer"/> ShieldSymbolizer</th></tr>
                <tr><th></th><td><img src="{@file}"/></td></tr>
                <tr><th>face_name:</th><td><xsl:value-of select="@face_name"/></td></tr>
                <tr><th>file:</th><td><xsl:value-of select="@file"/></td></tr>
                <tr><th>fill:</th><td><xsl:value-of select="@fill"/></td></tr>
                <tr><th>height:</th><td><xsl:value-of select="@height"/></td></tr>
                <tr><th>min_distance:</th><td><xsl:value-of select="@min_distance"/></td></tr>
                <tr><th>name:</th><td><xsl:value-of select="@name"/></td></tr>
                <tr><th>placement:</th><td><xsl:value-of select="@placement"/></td></tr>
                <tr><th>size:</th><td><xsl:value-of select="@size"/></td></tr>
                <tr><th>type:</th><td><xsl:value-of select="@type"/></td></tr>
                <tr><th>width:</th><td><xsl:value-of select="@width"/></td></tr>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="TextSymbolizer">
        <div class="popup">
            <span class="anchor"><xsl:value-of select="$TextSymbolizer"/></span>
            <table class="popup">
                <tr><th colspan="2" class="title"><xsl:value-of select="$TextSymbolizer"/> TextSymbolizer</th></tr>
                <tr><th>allow_overlap:</th><td><xsl:value-of select="@allow_overlap"/></td></tr>
                <tr><th>avoid_edges:</th><td><xsl:value-of select="@avoid_edges"/></td></tr>
                <tr><th>dx:</th><td><xsl:value-of select="@dx"/></td></tr>
                <tr><th>dy:</th><td><xsl:value-of select="@dy"/></td></tr>
                <tr><th>face_name:</th><td><xsl:value-of select="@face_name"/></td></tr>
                <tr><th>fill:</th><td><xsl:value-of select="@fill"/></td></tr>
                <tr><th>halo_fill:</th><td><xsl:value-of select="@halo_fill"/></td></tr>
                <tr><th>halo_radius:</th><td><xsl:value-of select="@halo_radius"/></td></tr>
                <tr><th>label_position_tolerance:</th><td><xsl:value-of select="@label_position_tolerance"/></td></tr>
                <tr><th>max_char_angle_delta:</th><td><xsl:value-of select="@max_char_angle_delta"/></td></tr>
                <tr><th>min_distance:</th><td><xsl:value-of select="@min_distance"/></td></tr>
                <tr><th>name:</th><td><xsl:value-of select="@name"/></td></tr>
                <tr><th>placement:</th><td><xsl:value-of select="@placement"/></td></tr>
                <tr><th>size:</th><td><xsl:value-of select="@size"/></td></tr>
                <tr><th>spacing:</th><td><xsl:value-of select="@spacing"/></td></tr>
                <tr><th>text_ratio:</th><td><xsl:value-of select="@text_ratio"/></td></tr>
                <tr><th>wrap_width:</th><td><xsl:value-of select="@wrap_width"/></td></tr>
            </table>
        </div>
    </xsl:template>

</xsl:stylesheet>
