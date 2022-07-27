**event_id** *Ex*: 383097, 374427, 364175
(Primary database key field)
(ID assigned by NWS to note a single, small part that goes into a specific storm episode; links
the storm episode between the three files downloaded from SPC’s website)

**cz_name** str *Ex*: AIKEN Co., RICHMOND Co, DEKALB (Z ;ONE) (County/Parish, Z ;one or
Marine Name assigned to the county FIPS number or NWS Forecast Z ;one)

**begin_location** *Ex*: DAVENPORT, PLATO CENTER, BENNETTSVILLE
The name of the begin location of the event

**begin_date** *Ex*: 4/1/2012
The begin time of the event in MM/DD/YYYY format

**begin_time** *Ex*: 1744
The time of day the event began in hhmm format

**event_type** *Ex*: Hail, Thunderstorm Wind, Snow, Ice (spelled out; not abbreviated)
The only events permitted in Storm Data are listed in Table 1. The
chosen event name should be the one that most accurately describes the meteorological event
leading to fatalities, injuries, damage, etc. However, significant events, such as tornadoes,
having no impact or causing no damage, should also be included in Storm Data.

***Table 1***:
Event Name               =  Designator (County or Zone) ;
Astronomical Low Tide    =  Z ;
Avalanche                =  Z ;
Blizzard                 =  Z ;
Coastal Flood            =  Z ;
Cold/Wind Chill          =  Z ;
Debris Flow              =  C ;
Dense Fog                =  Z ;
Dense Smoke              =  Z ;
Drought                  =  Z ;
Dust Devil               =  C ;
Dust Storm               =  Z ;
Excessive Heat           =  Z ;
Extreme Cold/Wind Chill  =  Z ;
Flash Flood              =  C ;
Flood                    =  C ;
Freezing Fog             =  Z ;
Frost/Freeze             =  Z ;
Funnel Cloud             =  C ;
Hail                     =  C ;
Heat                     =  Z ;
Heavy Rain               =  C ;
Heavy Snow               =  Z ;
High Surf                =  Z ;
High Wind                =  Z ;
Hurricane (Typhoon)      =  Z ;
Lake-Effect Snow         =  Z ;
Lakeshore Flood          =  Z ;
Lightning                =  C ;
Marine Hail              =  M ;
Marine High Wind         =  M ;
Marine Strong Wind       =  M ;
Marine Thunderstorm Wind =  M ;
Rip Current              =  Z ;
Seiche                   =  Z ;
Sleet                    =  Z ;
Storm Surge/Tide         =  Z ;
Strong Wind              =  Z ;
Thunderstorm Wind        =  C ;
Tornado                  =  C ;
Tropical Depression      =  Z ;
Tropical Storm           =  Z ;
Tsunami                  =  Z ;
Volcanic Ash             =  Z ;
Waterspout               =  M ;
Wildfire                 =  Z ;
Winter Storm             =  Z ;
Winter Weather           =  Z ;


**magnitude** *Ex*: 0.75, 60, 0.88, 2.75
The magnitude of the event. This is only used for wind speeds and hail siZ ;e (e.g. 0.75” of hail;
60 knot winds)

**tor_f_scale** *Ex*: EF0, EF1, EF2, EF3, EF4, EF5
Enhanced Fujita Scale describes the strength of the tornado based on the amount and type of
damage caused by the tornado. The F-scale of damage will vary in the destruction area;
therefore, the highest value of the F-scale is recorded for each event.  
EF0 – Light Damage (40 – 72 mph)  
EF1 – Moderate Damage (73 – 112 mph)  
EF2 – Significant damage (113 – 157 mph)  
EF3 – Severe Damage (158 – 206 mph)  
EF4 – Devastating Damage (207 – 260 mph)  
EF5 – Incredible Damage (261 – 318 mph)

**deaths_direct** *Ex*: 0, 45, 23
The number of deaths directly related to the weather event.

**injuries_direct** *Ex*: 1, 0, 56
The number of injuries directly related to the weather event

**damage_property_num** *Ex*: 10.00K, 0.00K, 10.00M
The estimated amount of damage to property incurred by the weather event. (e.g. 10.00K =
$10,000; 10.00M = $10,000,000)

**damage_crops_num** *Ex*: 0.00K, 500.00K, 15.00M
The estimated amount of damage to crops incurred by the weather event (e.g. 10.00K =
$10,000; 10.00M = $10,000,000)

**state_abbr** *Ex*: GA, WY, CO
The state postal abbreviation of the event

**cz_timezone** *Ex*: EST-5, MST-7, CST-6
(Time Z ;one for the County/Parish, Z ;one or Marine Name)
Eastern Standard Time (EST), Central Standard Time (CST), Mountain Standard Time (MST),
etc.

**magnitude_type** *Ex*: EG, MS, MG, ES
EG = Wind Estimated Gust; ES = Estimated Sustained Wind; MS = Measured Sustained Wind;
MG = Measured Wind Gust (no magnitude is included for instances of hail)

**episode_id** *Ex*: 60904
ID assigned by NWS to denote the storm episode; links the storm episode with the information
within the event details file. An Episode may contain several different events.

**cz_type** *Ex*: C, Z ; , M
Indicates whether the event happened in a (C) county/parish, (Z ;) Z ;one or (M) marine

**cz_fips** *Ex*: 245, 003, 155
The county FIPS number is a unique number assigned to the county by the National Institute
for Standards and Technology (NIST) or NWS Forecast Z ;one Number (See addendum)

**wfo** *Ex*: CAE, BYZ ;, GJT (National Weather Service Forecast Office’s area of responsibility
(County Warning Area) in which the event occurred)

**injuries_indirect** *Ex*: 0, 15, 87
The number of injuries indirectly related to the weather event

**deaths_indirect** *Ex*: 0, 4, 6
The number of deaths indirectly related to the weather event

**source** *Ex*: Public, Newspaper, Law Enforcement, Broadcast Media, ASOS, Park and Forest
Service, Trained Spotter, CoCoRaHS, etc. (can be any entry; isn’t restricted in what’s
allowed)
Source reporting the weather event

**flood_cause** *Ex*: Ice Jam, Heavy Rain, Heavy Rain/Snow Melt
Reported or estimated cause of the flood

**tor_length** *Ex*: 0.66, 1.05, 0.48
Length of the tornado or tornado segment while on the ground (minimal of tenths of miles)

**tor_width** *Ex*: 25, 50, 2640, 10
Width of the tornado or tornado segment while on the ground (in feet)

**begin_range** *Ex*: 0.59, 0.69, 4.84, 1.17 (in miles)
The distance to the nearest tenth of a mile, to the location referenced below.

**begin_azimuth** *Ex*: ENE, NW, WSW, S
16-point compass direction from the location referenced below.

**end_range** see begin_range

**end_azimuth** see begin_aZ ;imuth

**end_location** see begin_location

**begin_lat** *Ex*: 29.7898
The latitude in decimal degrees of the begin point of the event or damage path.

**begin_lon** *Ex*: -98.6406
The longitude in decimal degrees of the begin point of the event or damage path.

**end_lat** *Ex*: 29.7158
The latitude in decimal degrees of the end point of the event or damage path. Signed negative (-)
if in the southern hemisphere.

**end_lon** *Ex*: -98.7744
The longitude in decimal degrees of the end point of the event or damage path. Signed negative
(-) if in the eastern hemisphere.

**episode_narrative** *Ex*: On the morning of Sunday March 3rd, 2019, an upper-level
disturbance moved eastward from the Southern Plains into the southern Gulf Coast States.
The episode narrative depicting the general nature and overall activity of the episode. The
National Weather Service creates the narrative.

**event_narrative** *Ex*: National Weather Service meteorologists surveyed damage in far
southern Lee County and determined that it was consistent with an EF4 tornado, with
maximum sustained winds near 170 mphThe event narrative provides descriptive details of the
individual event. The National Weather Service creates the narrative.

**absolute_row_number** the sequential number of events exported in this data file.
