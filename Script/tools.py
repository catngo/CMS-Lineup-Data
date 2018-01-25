import collections

STARTERS = (("PRESIDENT,MILES","SCARLETT,MICHAEL","HALL,RILEY","LYNDS,SCOTT","MORRIS,KENDRICK"),("PRESIDENT,MILES","SCARLETT,MICHAEL","HALL,RILEY","DAVIS,EVAN","MORRIS,KENDRICK"),("PRESIDENT,MILES","SCARLETT,MICHAEL","HALL,RILEY","ELY,JACK","MORRIS,KENDRICK"))

heading = ["player 1","player 2","player 3","player 4","player 5","minutes","plus-minus","points scored","offensive possession","turnovers","offensive rebounds","defensive rebounds given","2-pt made","2-pt missed","3-pt made","3-pt missed","assists","free-throw attempt","points givens","defensive possession","turnovers forced","offensive rebounds given","defensive rebounds","2-pt made given","2-pt missed given","3-pt made given","3-pt missed given","assists given","free-throw attempt given"]

heading1 = ["player","minutes","plus-minus","points scored","offensive possession","turnovers","offensive rebounds","defensive rebounds given","2-pt made","2-pt missed","3-pt made","3-pt missed","assists","free-throw attempt","points givens","defensive possession","turnovers forced","offensive rebounds given","defensive rebounds","2-pt made given","2-pt missed given","3-pt made given","3-pt missed given","assists given","free-throw attempt given"]

heading2 = ["player 1", "player 2","minutes","plus-minus","points scored","offensive possession","turnovers","offensive rebounds","defensive rebounds given","2-pt made","2-pt missed","3-pt made","3-pt missed","assists","free-throw attempt","points givens","defensive possession","turnovers forced","offensive rebounds given","defensive rebounds","2-pt made given","2-pt missed given","3-pt made given","3-pt missed given","assists given","free-throw attempt given"]

heading3 = ["player 1", "player 2", "player 3","minutes","plus-minus","points scored","offensive possession","turnovers","offensive rebounds","defensive rebounds given","2-pt made","2-pt missed","3-pt made","3-pt missed","assists","free-throw attempt","points givens","defensive possession","turnovers forced","offensive rebounds given","defensive rebounds","2-pt made given","2-pt missed given","3-pt made given","3-pt missed given","assists given","free-throw attempt given"]

PLAYERS = ('DAVIS,EVAN',
 'HALL,RILEY',
 'KUSCH,RYAN',
 'MYERS,PATRICK',
 'PRESIDENT,MILES',
 'HORN,JEREMY',
 'SCARLETT,MICHAEL',
 'ELY,JACK',
 'LYNDS,SCOTT',
 'MORRIS,KENDRICK',
 'LEVINE,JD',
 'KIRSCH,MAXWELL',
 'MADDOCK,ANDREW',
 'SUI,MARK',
 'GARVIN,SAM',
 'MKPADO,KELE',
 'WALKER,GEORGE',
 'KEINAN,DANIEL')

# Davis sub out Lynds on 2/4 (index 8) for HOME URLs. 1/28 (index 7) for Away URLs.
# Ely sub out Davis on 2/18 (index 12) for home URLs. 2/20 (index 10) for Away URLs.

Home_URLs = [
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161125_f5x6.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161126_t17s.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161202_h8t7.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161228_ucqz.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161229_cy5v.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170107_9rbl.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170117_sta2.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170126_mjsx.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170204_dyg7.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170207_ewjx.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170209_v0se.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170216_ljsz.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170218_pws3.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170224_bycd.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170225_ra6h.xml?view=plays"
]

Away_URLs = [
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161118_csa8.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161119_9z1r.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161209_wuge.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20161217_pc82.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170105_enmc.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170119_7s63.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170121_l0wi.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170128_dl5k.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170202_pnxp.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170211_8u3b.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170220_es47.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170303_htvf.xml?view=plays",
    "http://www.cmsathletics.org/sports/mbkb/2016-17/boxscores/20170304_y5je.xml?view=plays"
]