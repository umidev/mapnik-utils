/* -*- mode: css -*- */

/*

http://wiki.openstreetmap.org/index.php/Dresdner_Heide
http://commons.wikimedia.org/wiki/Category:Footpath_signs_in_Dresdner_Heide

*/


.route.hiking_heide_a_h empty,
.route.hiking_heide_k_n empty,
.route.hiking_heide_o_s empty,
.route.hiking_heide_t_z empty
{
    shield-face-name: "Droid Sans Regular";
    shield-size: 0;
    shield-fill: #777;
}

.route.hiking_heide_a_h[zoom>=12],
.route.hiking_heide_k_n[zoom>=12],
.route.hiking_heide_o_s[zoom>=12],
.route.hiking_heide_t_z[zoom>=12]
{
    shield-min-distance: 2;
    shield-spacing: 22;
}
.route.hiking_heide_a_h[zoom>=14],
.route.hiking_heide_k_n[zoom>=14],
.route.hiking_heide_o_s[zoom>=14],
.route.hiking_heide_t_z[zoom>=14]
{
    shield-min-distance: 5;
    shield-spacing: 55;
}
.route.hiking_heide_a_h[zoom>=15],
.route.hiking_heide_k_n[zoom>=15],
.route.hiking_heide_o_s[zoom>=15],
.route.hiking_heide_t_z[zoom>=15]
{
    shield-min-distance: 8;
    shield-spacing: 88;
}

/*

missing:

Alter Kannenhenkel
Bluempenweg
Fensterchen
Kreuz 4

*/


.route.hiking_heide_a_h[name="Dresdner Heide, Anker"][zoom>=14]                     { shield-file: url('img/symbols/dresdner_heide/anker1.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Bischofsweg"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/bischofsweg.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Brille"][zoom>=14]                    { shield-file: url('img/symbols/dresdner_heide/brille.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Diebsteig"][zoom>=14]                 { shield-file: url('img/symbols/dresdner_heide/diebsteig.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Doppel-E"][zoom>=14]                  { shield-file: url('img/symbols/dresdner_heide/doppel-e.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Flügelweg"][zoom>=14]                 { shield-file: url('img/symbols/dresdner_heide/fluegelweg.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Gabel"][zoom>=14]                     { shield-file: url('img/symbols/dresdner_heide/gabel.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Gänsefuß"][zoom>=14]                  { shield-file: url('img/symbols/dresdner_heide/gaensefuss.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, HG-Weg"][zoom>=14]                    { shield-file: url('img/symbols/dresdner_heide/hg-weg.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Hakenweg"][zoom>=14]                  { shield-file: url('img/symbols/dresdner_heide/hakenweg.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Hirschstängel"][zoom>=14]             { shield-file: url('img/symbols/dresdner_heide/hirschstaengel.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Hämmerchen"][zoom>=14]                { shield-file: url('img/symbols/dresdner_heide/haemmerchen.16.png'); }
.route.hiking_heide_a_h[name="Dresdner Heide, Hütchen"][zoom>=14]                   { shield-file: url('img/symbols/dresdner_heide/huetchen.16.png'); }

.route.hiking_heide_k_n[name="Dresdner Heide, Kannenhenkel"][zoom>=14]              { shield-file: url('img/symbols/dresdner_heide/kannenhenkel.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Kreuz 5"][zoom>=14]                   { shield-file: url('img/symbols/dresdner_heide/kreuz_5.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Kreuz 6"][zoom>=14]                   { shield-file: url('img/symbols/dresdner_heide/kreuz_6.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Kreuz 7"][zoom>=14]                   { shield-file: url('img/symbols/dresdner_heide/kreuz_7.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Krumme Neun"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/krumme_9.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Krumme 9"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/krumme_9.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Mehlflußweg"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/mehlflussweg.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Mittelweg"][zoom>=14]                 { shield-file: url('img/symbols/dresdner_heide/mittelweg.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Mühlweg"][zoom>=14]                   { shield-file: url('img/symbols/dresdner_heide/muehlweg.16.png'); }

.route.hiking_heide_k_n[name="Dresdner Heide, Nachtflügel"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/nachtfluegel.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Neuer Flügel"][zoom>=14]              { shield-file: url('img/symbols/dresdner_heide/neuer_fluegel.16.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Neuer Weg"][zoom>=14]                 { shield-file: url('img/symbols/dresdner_heide/neuer_weg.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Ochsensteig"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/ochsensteig.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Pillnitz-Moritzburger-Weg"][zoom>=14] { shield-file: url('img/symbols/dresdner_heide/pillnitz-moritzburger_weg.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Reichsapfel"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/reichsapfel.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Rennsteig"][zoom>=14]                 { shield-file: url('img/symbols/dresdner_heide/rennsteig.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Runde 4"][zoom>=14]                   { shield-file: url('img/symbols/dresdner_heide/runde_4.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Sandbrückenweg"][zoom>=14]            { shield-file: url('img/symbols/dresdner_heide/sandbrueckenweg.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Saugartenweg"][zoom>=14]              { shield-file: url('img/symbols/dresdner_heide/saugartenweg.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Schere"][zoom>=14]                    { shield-file: url('img/symbols/dresdner_heide/schere.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Schwerterweg"][zoom>=14]              { shield-file: url('img/symbols/dresdner_heide/schwerterweg.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Schwesternsteig"][zoom>=14]           { shield-file: url('img/symbols/dresdner_heide/schwesternsteig.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Semmelweg"][zoom>=14]                 { shield-file: url('img/symbols/dresdner_heide/semmelweg.16.png'); }
.route.hiking_heide_o_s[name="Dresdner Heide, Stuhlweg"][zoom>=14]                  { shield-file: url('img/symbols/dresdner_heide/stuhlweg.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Todweg"][zoom>=14]                    { shield-file: url('img/symbols/dresdner_heide/todweg.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Topfweg"][zoom>=14]                   { shield-file: url('img/symbols/dresdner_heide/topfweg.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Verkehrte Gabel"][zoom>=14]           { shield-file: url('img/symbols/dresdner_heide/verkehrte_gabel.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Verkehrter Anker"][zoom>=14]          { shield-file: url('img/symbols/dresdner_heide/verkehrter_anker.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Vogelzipfel"][zoom>=14]               { shield-file: url('img/symbols/dresdner_heide/vogelzipfel.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Weißiger Gänsefuß"][zoom>=14]         { shield-file: url('img/symbols/dresdner_heide/weissiger_gaensefuss.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Weißiger Weg"][zoom>=14]              { shield-file: url('img/symbols/dresdner_heide/weissiger_weg.16.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Wiesenweg"][zoom>=14]                 { shield-file: url('img/symbols/dresdner_heide/wiesenweg.16.png'); }



.route.hiking_heide_k_n[name="Dresdner Heide, Kreuz R"][zoom>=12]    { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Kreuz-R.8.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Kuhschwanz"][zoom>=12] { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Kuhschwanz.8.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Zirkel"][zoom>=12]     { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Zirkel.8.png'); }

.route.hiking_heide_k_n[name="Dresdner Heide, Kreuz R"][zoom>=14]    { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Kreuz-R.10.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Kuhschwanz"][zoom>=14] { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Kuhschwanz.10.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Zirkel"][zoom>=14]     { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Zirkel.10.png'); }

.route.hiking_heide_k_n[name="Dresdner Heide, Kreuz R"][zoom>=15]    { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Kreuz-R.12.png'); }
.route.hiking_heide_k_n[name="Dresdner Heide, Kuhschwanz"][zoom>=15] { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Kuhschwanz.12.png'); }
.route.hiking_heide_t_z[name="Dresdner Heide, Zirkel"][zoom>=15]     { shield-file: url('img/symbols/dresdner_heide/Wegzeichen_Zirkel.12.png'); }
