//DECOMPRESS FILES
tz0:.z.p
system "gzip -kd gzipped/*"
tz1:.z.p
tgz:tz1-tz0

//INGEST DETAILS
t0:.z.p
detfiles:asc hsym each `$' ":/home/conner/testgz/gzipped/",/:  system "ls gzipped | grep -v gz | grep details"
details: (,/) {(51#"*";enlist ",") 0: x} each detfiles
t1:.z.p

//CREATE DETAILS SUBSET TABLE AND CAST COLUMN TYPES
det:select BEGIN_YEARMONTH,BEGIN_DAY,END_YEARMONTH,END_DAY,"I"$EPISODE_ID,"I"$EVENT_ID,EVENT_TYPE,
    `$STATE,"I"$INJURIES_DIRECT,"I"$INJURIES_INDIRECT,"I"$DEATHS_DIRECT,"I"$DEATHS_INDIRECT,"F"$BEGIN_LAT,"F"$BEGIN_LON from details
update BEGIN_DATE:(BEGIN_YEARMONTH,'BEGIN_DAY) from `det where not 1=count each BEGIN_DAY;
update BEGIN_DATE:(BEGIN_YEARMONTH,'("0",'BEGIN_DAY)) from `det where 1=count each BEGIN_DAY;
update END_DATE:(END_YEARMONTH,'END_DAY) from `det where not 1=count each END_DAY;
update END_DATE:(END_YEARMONTH,'("0",'END_DAY)) from `det where 1=count each END_DAY;

//CALC DETAILS ELAPSED TIMES
t2:.z.p;td1:t1-t0;td2:t2-t1;td3:t2-t0;t4:.z.p

//INGEST FATALITES
fatfiles:asc hsym each `$' ":/home/conner/testgz/gzipped/",/:  system "ls gzipped | grep -v gz | grep fatalities"
fatalities: (,/) {(11#"*";enlist ",") 0:x} each fatfiles
t5:.z.p

//CREATE FATALITES SUBSET TABLE AND CAST COLUMN TYPES
fat: select FATALITY_DATE,FATALITY_ID,EVENT_ID,FATALITY_TYPE,FATALITY_AGE,FATALITY_SEX,FATALITY_LOCATION from fatalities
update "I"$FATALITY_ID,"I"$EVENT_ID,`$FATALITY_TYPE,"I"$FATALITY_AGE,`$FATALITY_SEX from `fat;
update "D"$10#'FATALITY_DATE from `fat;

//CALC FATALITIES ELAPSED TIMES
t6:.z.p;td4:t5-t4;td5:t6-t5;td6:t6-t4;td7:t6-tz0;show ""

//PRINT SCRIPT TOTAL ELAPSED TIME
show (enlist `$"UNZIPPING TIME: ")!enlist `$((-6_8_string tgz)," secs")
show ""
//PRINT DETAILS SUMMARY DICT
show (`$"TABLE: ";`$"ROWS:";`$"COLS:";`$"COPY:";`$"CAST:";`$"TOTAL:")!
    `details,(`$string count details),(`$string count cols details),`$'(-6_'8_'string value each `td1`td2`td3), \: " secs"
show ""

//PRINT FATALITIES SUMMARY DICT
show (`$"TABLE: ";`$"ROWS:";`$"COLS:";`$"COPY:";`$"CAST:";`$"TOTAL:")!
    `fatalities,(`$string count fatalities),(`$string count cols fatalities),`$'(-6_'8_'string value each `td4`td5`td6), \: " secs"
show ""

//PRINT SCRIPT TOTAL ELAPSED TIME
show (enlist `$"FULL SCRIPT RUN ELAPSED TIME: ")!enlist `$((-6_8_string td7)," secs")
show ""
\\
