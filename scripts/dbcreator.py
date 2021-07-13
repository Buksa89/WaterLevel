from os import stat
import pandas as pd
import sqlalchemy
from sshtunnel import SSHTunnelForwarder
from db_data import *

# Create databases:
server = SSHTunnelForwarder(
    (sshhost, sshport),
    ssh_username=sshuser,
    ssh_password=sshpass,
    remote_bind_address=(sshbhost, sshbport)
    )


server.start()
local_port = str(server.local_bind_port)
engine = sqlalchemy.create_engine(f'{dbtype}://{dbuser}:{dbpass}@localhost:{local_port}/{dbname}') #Postgresql

with engine.connect() as connection:
    result = connection.execute(f"""CREATE TABLE IF NOT EXISTS {hdtable}
(
    value double precision,
    datetime timestamp without time zone,
    station_id bigint
)
""")

with engine.connect() as connection:
    result = connection.execute(f"""CREATE TABLE IF NOT EXISTS {wdtable}
(
    value double precision,
    datetime timestamp without time zone,
    station_id bigint
)
""")

with engine.connect() as connection:
    result = connection.execute(f"""CREATE TABLE IF NOT EXISTS {hstable} (
    station_id bigint NOT NULL,
    station_name character(100),
    river character(100) NOT NULL,
    latitude double precision,
    longitude double precision,
    kilometer bigint
)

""")

with engine.connect() as connection:
    result = connection.execute(f"""CREATE TABLE IF NOT EXISTS {wstable} (
    station_id bigint NOT NULL,
    station_name character(100),
    latitude double precision,
    longitude double precision
)

""")

with engine.connect() as connection:
    result = connection.execute(f"""TRUNCATE TABLE  {hstable}
""")

with engine.connect() as connection:
    result = connection.execute(f"""TRUNCATE TABLE  {wstable}
""")




# Fill hydro data
url = "https://danepubliczne.imgw.pl/api/data/hydro/"

stations = pd.read_json(url)
stations = stations[["id_stacji", "stacja", "rzeka"]]
stations.columns = ["station_id", "station_name", "river"]

location = {
    #  154180140: ['Gdańsk', '-'], # Gdańsk
    #  150190070: ['Szabelnia', '-'], # Szabelnia
    #  149200360: ['Lipnica Murowana', '-'], # Lipnica Murowana
    #  151170040: ['Łąki', 'Barycz'], # Łąki
    #  151160140: ['Osetno', 'Barycz'], # Osetno
    #  151170070: ['Odolanów', 'Barycz'], # Odolanów
    #  154190110: ['Nowe Sadłuki', 'Bauda'], # Nowe Sadłuki
    #  152170150: ['Trąbczyn', 'Bawół'], # Trąbczyn
    #  154150030: ['Kołobrzeg', 'Bałtyk'], # Kołobrzeg
    #  154180120: ['Gdynia', 'Bałtyk'], # Gdynia
    #  154170100: ['Łeba', 'Bałtyk'], # Łeba
    #  154180100: ['Władysławowo', 'Bałtyk'], # Władysławowo
    #  153180120: ['Hel', 'Bałtyk'], # Hel
    #  154160110: ['Ustka', 'Bałtyk'], # Ustka
    #  149190030: ['Mikuszowice', 'Biała'], # Mikuszowice
    #  149200310: ['Grybów', 'Biała'], # Grybów
    #  149190010: ['Czechowice-Bestwina', 'Biała'], # Czechowice-Bestwina
    #  150170220: ['Dobra', 'Biała'], # Dobra
    #  149200320: ['Koszyce Wielkie', 'Biała'], # Koszyce Wielkie
    #  153230060: ['Zawady', 'Biała'], # Zawady
    #  149200330: ['Ciężkowice', 'Biała'], # Ciężkowice
    #  150170070: ['Głuchołazy', 'Biała Głuchołaska'], # Głuchołazy
    #  150170050: ['Biała Nyska', 'Biała Głuchołaska'], # Biała Nyska
    #  150160200: ['Żelazno', 'Biała Lądecka'], # Żelazno
    #  150160230: ['Lądek Zdrój', 'Biała Lądecka'], # Lądek Zdrój
    #  150200010: ['Mniszek', 'Biała Nida'], # Mniszek
    #  150190100: ['Niwka', 'Biała Przemsza'], # Niwka
    #  149180180: ['Wisła Czarne', 'Biała Wisełka'], # Wisła Czarne
    #  150220110: ['Biłgoraj', 'Biała Łada'], # Biłgoraj
    #  149200110: ['Trybsz 2', 'Białka'], # Trybsz 2
    #  149200100: ['Łysa Polana', 'Białka'], # Łysa Polana
    #  149200020: ['Szaflary', 'Biały Dunajec'], # Szaflary
    #  153220170: ['Osowiec', 'Biebrza'], # Osowiec
    #  153220100: ['Burzyn', 'Biebrza'], # Burzyn
    #  153230070: ['Sztabin', 'Biebrza'], # Sztabin
    #  153220260: ['Dębowo', 'Biebrza'], # Dębowo
    #  154180180: ['Suchy Dąb', 'Bielawa'], # Suchy Dąb
    #  150180080: ['Grabówka', 'Bierawka'], # Grabówka
    #  150200090: ['Slowik', 'Bobrza'], # Slowik
    #  150170200: ['Domaradz', 'Bogacica'], # Domaradz
    #  153170140: ['Smukała', 'Brda'], # Smukała
    #  153170120: ['Tuchola', 'Brda'], # Tuchola
    #  150210070: ['Wampierzów', 'Bren'], # Wampierzów
    #  149180120: ['Górki Wielkie', 'Brennica'], # Górki Wielkie
    #  150190010: ['Brynica', 'Brynica'], # Brynica
    #  150180270: ['Kozłowa Góra', 'Brynica'], # Kozłowa Góra
    #  153230020: ['Karpowicze', 'Brzozówka'], # Karpowicze
    #  150160270: ['Kamieniec Ząbkowicki', 'Budzówka'], # Kamieniec Ząbkowicki
     150240010: [563, 50.84012080171515, 24.025222137070347], # Strzyżów
     152229999: [98, 52.6762464474775, 22.04388761464201], # Małkinia
     152210090: [34, 52.59134392672929, 21.4595265780366], # Wyszków
     150240020: [612, 50.684089158956304, 24.062996343596915], # Kryłów
     152230080: [268, 52.14974667246817, 23.491982284108893], # Krzyczew
     151230040: [385, 51.5496100178516, 23.565161440069403], # Włodawa
     152220050: [163, 52.41454625433878, 22.560452509347744], # Frankopol
     152230200: [209, 52.31463913620738, 23.050603854775684], # Zabuże
     151230060: [476, 51.175152408965786, 23.81225564627763], # Dorohusk
    #  150220020: ['Ruda Jastkowska', 'Bukowa'], # Ruda Jastkowska
    #  149190020: ['Kamesznica', 'Bystra'], # Kamesznica
    #  150160070: ['Lubachów', 'Bystrzyca'], # Lubachów
    #  150160120: ['Krasków', 'Bystrzyca'], # Krasków
    #  151160190: ['Jarnołtów', 'Bystrzyca'], # Jarnołtów
    #  150160150: ['Bystrzyca Kłodzka 2', 'Bystrzyca'], # Bystrzyca Kłodzka 2
    #  150160060: ['Jugowice', 'Bystrzyca'], # Jugowice
    #  150160160: ['Mietków', 'Bystrzyca'], # Mietków
    #  151220100: ['Sobianowice', 'Bystrzyca'], # Sobianowice
    #  150160110: ['Szalejów Dolny', 'Bystrzyca Dusznicka'], # Szalejów Dolny
    #  152200050: ['Żuków', 'Bzura'], # Żuków
    #  152190050: ['Kwiatkówek', 'Bzura'], # Kwiatkówek
    #  150150120: ['Bukówka', 'Bóbr'], # Bukówka
    #  150150080: ['Jelenia Góra', 'Bóbr'], # Jelenia Góra
    #  151150050: ['Dobroszów Wielki', 'Bóbr'], # Dobroszów Wielki
    #  152150020: ['Stary Raduszec', 'Bóbr'], # Stary Raduszec
    #  150150130: ['Błażkowa', 'Bóbr'], # Błażkowa
    #  151150120: ['Szprotawa', 'Bóbr'], # Szprotawa
    #  150150060: ['Pilchowice', 'Bóbr'], # Pilchowice
    #  150150100: ['Wojanów', 'Bóbr'], # Wojanów
    #  150160010: ['Kamienna Góra', 'Bóbr'], # Kamienna Góra
    #  151150040: ['Nowogród Bobrzański', 'Bóbr'], # Nowogród Bobrzański
    #  151150080: ['Żagań', 'Bóbr'], # Żagań
    #  151150140: ['Dąbrowa Bolesławiecka', 'Bóbr'], # Dąbrowa Bolesławiecka
    #  149190380: ['Zakopane Harenda', 'Cicha Woda'], # Zakopane Harenda
    #  150210010: ['Raków', 'Czarna'], # Raków
    #  151190120: ['Dąbrowa', 'Czarna'], # Dąbrowa
    #  150190350: ['Januszewice', 'Czarna'], # Januszewice
    #  150210060: ['Staszów', 'Czarna'], # Staszów
    #  150210100: ['Połaniec', 'Czarna'], # Połaniec
    #  153230080: ['Sochonie', 'Czarna'], # Sochonie
    #  150200120: ['Morawica', 'Czarna Nida'], # Morawica
    #  150200160: ['Daleszyce', 'Czarna Nida'], # Daleszyce
    #  150200040: ['Tokarnia', 'Czarna Nida'], # Tokarnia
    #  150190130: ['Łagisza', 'Czarna Przemsza'], # Łagisza
    #  150190080: ['Radocha', 'Czarna Przemsza'], # Radocha
    #  150190120: ['Przeczyce', 'Czarna Przemsza'], # Przeczyce
    #  149180200: ['Wisła Czarne', 'Czarna Wisełka'], # Wisła Czarne
    #  150160290: ['Gniechowice', 'Czarna Woda'], # Gniechowice
    #  151160040: ['Bukowna', 'Czarna Woda'], # Bukowna
    #  151160080: ['Rzeszotary', 'Czarna Woda'], # Rzeszotary
    #  149220140: ['Polana', 'Czarny'], # Polana
    #  149200030: ['Nowy Targ', 'Czarny Dunajec'], # Nowy Targ
    #  149190280: ['Koniówka', 'Czarny Dunajec'], # Koniówka
    #  150150020: ['Mirsk 2', 'Czarny Potok'], # Mirsk 2
    #  151150030: ['Iłowa', 'Czerna Mała'], # Iłowa
    #  151150070: ['Żagań', 'Czerna Wielka'], # Żagań
    #  150180160: ['Pyskowice Dzierżno', 'Drama'], # Pyskowice Dzierżno
    #  150180170: ['Pyskowice', 'Drama'], # Pyskowice
    #  152150240: ['Drawiny', 'Drawa'], # Drawiny
    #  153190050: ['Brodnica', 'Drwęca'], # Brodnica
    #  153190120: ['Rodzone', 'Drwęca'], # Rodzone
    #  153180140: ['Elgiszewo', 'Drwęca'], # Elgiszewo
    #  153190090: ['Nowe Miasto Lubawskie', 'Drwęca'], # Nowe Miasto Lubawskie
    #  154200020: ['Krosno', 'Drwęca Warmińska'], # Krosno
    #  151200080: ['Odrzywół', 'Drzewiczka'], # Odrzywół
    #  149200050: ['Nowy Targ - Kowaniec', 'Dunajec'], # Nowy Targ - Kowaniec
    #  149200230: ['Czchów', 'Dunajec'], # Czchów
    #  150200170: ['Żabno', 'Dunajec'], # Żabno
    #  149200190: ['Gołkowice', 'Dunajec'], # Gołkowice
    #  149200280: ['Zgłobice', 'Dunajec'], # Zgłobice
    #  149200140: ['Sromowce Wyżne', 'Dunajec'], # Sromowce Wyżne
    #  149200160: ['Krościenko', 'Dunajec'], # Krościenko
    #  149200240: ['Nowy Sącz', 'Dunajec'], # Nowy Sącz
    #  153190040: ['Bągart', 'Dzierzgoń'], # Bągart
    #  153140070: ['Dziwnów', 'Dziwna'], # Dziwnów
    #  153140060: ['Wolin', 'Dziwna'], # Wolin
    #  154190060: ['Elbląg', 'Elbląg'], # Elbląg
    #  153220060: ['Ełk', 'Ełk'], # Ełk
    #  153220080: ['Prostki', 'Ełk'], # Prostki
    #  153220160: ['Osowiec 2', 'Ełk (Kanał Rudzki)'], # Osowiec 2
    #  153220140: ['Przechody', 'Ełk (Kanał.Rudzki)'], # Przechody
    #  152160120: ['Ryczywół', 'Flinta'], # Ryczywół
    #  150190060: ['Bojszowy', 'Gostynia'], # Bojszowy
    #  154220010: ['Banie Mazurskie', 'Gołdapa'], # Banie Mazurskie
    #  154220110: ['Gołdap 2', 'Gołdapa'], # Gołdap 2
    #  151190030: ['Łask', 'Grabia'], # Łask
    #  151180180: ['Grabno', 'Grabia'], # Grabno
    #  150210110: ['Głowaczowa', 'Grabinianka'], # Głowaczowa
    #  154210020: ['Prosna', 'Guber'], # Prosna
    #  153160180: ['Piła', 'Gwda'], # Piła
    #  153160210: ['Ptusza', 'Gwda'], # Ptusza
    #  149220070: ['Hoczew', 'Hoczewka'], # Hoczew
    #  150230070: ['Gozdów', 'Huczwa'], # Gozdów
    #  153140090: ['Goleniów', 'Ina'], # Goleniów
    #  153150010: ['Stargard', 'Ina'], # Stargard
    #  149180250: ['Czechowice Dziedzice', 'Iłownica'], # Czechowice Dziedzice
    #  151210080: ['Kazanów', 'Iłżanka'], # Kazanów
    #  154220050: ['Jurkiszki', 'Jarka'], # Jurkiszki
    #  149210080: ['Jasło', 'Jasiołka'], # Jasło
    #  149210100: ['Zboiska', 'Jasiołka'], # Zboiska
    #  150150110: ['Kowary', 'Jedlica'], # Kowary
    #  153220200: ['Rajgród', 'Jegrznia'], # Rajgród
    #  154190080: ['Żukowo', 'Jez. Drużno'], # Żukowo
    #  153190170: ['Ostróda', 'Jez. Drwęckie'], # Ostróda
    #  153220050: ['Ełk 2', 'Jez. Ełckie'], # Ełk 2
    #  154210060: ['Przystań', 'Jez. Mamry'], # Przystań
    #  154190150: ['Pierzchały', 'Jez. Pierzchalskie; Pasłęka'], # Pierzchały
    #  154190160: ['Pierzchały', 'Jez. Pierzchalskie; Pasłęka'], # Pierzchały
    #  154170190: ['Borucino', 'Jez. Raduńskie Górne'], # Borucino
    #  153210200: ['Maldanin', 'Jez. Roś'], # Maldanin
    #  153200090: ['Szypry', 'Jez. Wadąg'], # Szypry
    #  154170090: ['Izbica', 'Jez. Łebsko'], # Izbica
    #  153220190: ['Rajgród 2', 'Jez.Rajgrodzkie'], # Rajgród 2
    #  152210020: ['Piaseczno', 'Jeziorka'], # Piaseczno
    #  151160100: ['Piątnica', 'Kaczawa'], # Piątnica
    #  151150170: ['Świerzawa', 'Kaczawa'], # Świerzawa
    #  151160020: ['Rzymówka', 'Kaczawa'], # Rzymówka
    #  151160050: ['Dunino', 'Kaczawa'], # Dunino
    #  149200270: ['Łabowa', 'Kamienic'], # Łabowa
    #  150150040: ['Barcinek', 'Kamienica'], # Barcinek
    #  149200250: ['Nowy Sącz', 'Kamienica'], # Nowy Sącz
    #  151200100: ['Bzin', 'Kamienna'], # Bzin
    #  150210090: ['Kunów', 'Kamienna'], # Kunów
    #  151210010: ['Wąchock', 'Kamienna'], # Wąchock
    #  151210020: ['Michałów 2', 'Kamienna'], # Michałów 2
    #  150150030: ['Jakuszyce', 'Kamienna'], # Jakuszyce
    #  150210080: ['Nietulisko Duże', 'Kamienna'], # Nietulisko Duże
    #  151210090: ['Czekarzewice', 'Kamienna'], # Czekarzewice
    #  150150070: ['Jelenia Góra 2', 'Kamienna'], # Jelenia Góra 2
    #  150150050: ['Piechowice', 'Kamienna'], # Piechowice
    #  151210040: ['Brody Iłżeckie', 'Kamienna'], # Brody Iłżeckie
    #  152160090: ['Kościan', 'Kanał Mosiński'], # Kościan
    #  152160130: ['Mosin', 'Kanał Mosiński'], # Mosin
    #  154180260: ['Pruszcz Gdański_kanał', 'Kanał Raduni'], # Pruszcz Gdański_kanał
    #  152180160: ['Konin-Morzysław', 'Kanał Ślesiński'], # Konin-Morzysław
    #  152180110: ['Kościelec', 'Kiełbaska'], # Kościelec
    #  150160040: ['Kudowa Zdrój-Zakrze', 'Klikawa'], # Kudowa Zdrój-Zakrze
    #  150210160: ['Koprzywnica', 'Koprzywianka'], # Koprzywnica
    #  149190150: ['Pewel Mała', 'Koszarawa'], # Pewel Mała
    #  149190350: ['Krzczonów', 'Krzczonówka'], # Krzczonów
     152230070: [0, 52.105396153518384, 23.473423620290873], # Malowa Góra
    #  151170080: ['Odolanów 2', 'Kuroch'], # Odolanów 2
    #  151150090: ['Łozy', 'Kwisa'], # Łozy
    #  151150110: ['Gryfów Śląski', 'Kwisa'], # Gryfów Śląski
    #  151150060: ['Leśna', 'Kwisa'], # Leśna
    #  151150100: ['Nowogrodziec', 'Kwisa'], # Nowogrodziec
    #  150150010: ['Mirsk', 'Kwisa'], # Mirsk
    #  150180070: ['Lenartowice', 'Kłodnica'], # Lenartowice
    #  150180220: ['Gliwice', 'Kłodnica'], # Gliwice
    #  150180180: ['Gliwice-Łabędy', 'Kłodnica'], # Gliwice-Łabędy
    #  150180150: ['Pyskowice Dzierżno', 'Kłodnica'], # Pyskowice Dzierżno
    #  149190360: ['Ludźmierz', 'Lepietnica'], # Ludźmierz
    #  150180210: ['Niwki', 'Liswarta'], # Niwki
    #  151190010: ['Kule', 'Liswarta'], # Kule
    #  153180130: ['Kwidzyn', 'Liwa'], # Kwidzyn
    #  152210120: ['Łochów', 'Liwiec'], # Łochów
    #  152220010: ['Zaliwie-Piegawki', 'Liwiec'], # Zaliwie-Piegawki
    #  150220130: ['Zapałów', 'Lubaczówka'], # Zapałów
    #  149190370: ['Lubień', 'Lubieńka'], # Lubień
    #  151140020: ['Pleśno', 'Lubsza'], # Pleśno
    #  151190080: ['Kłudzice', 'Luciąża'], # Kłudzice
    #  154180160: ['Sobieszewo', 'Martwa Wisła'], # Sobieszewo
    #  150180100: ['Staniszcze Wielkie', 'Mała Panew'], # Staniszcze Wielkie
    #  150180190: ['Krupski Młyn', 'Mała Panew'], # Krupski Młyn
    #  150180020: ['Turawa', 'Mała Panew'], # Turawa
    #  150180050: ['Ozimek', 'Mała Panew'], # Ozimek
    #  150140100: ['Bogatynia', 'Miedzianka'], # Bogatynia
    #  150140030: ['Turoszów', 'Miedzianka'], # Turoszów
    #  150200050: ['Michałów', 'Mierzawa'], # Michałów
    #  150190210: ['Kuźnica Sulikowska', 'Mitręga'], # Kuźnica Sulikowska
    #  150220060: ['Gorliczyna', 'Mleczka Zachodnia'], # Gorliczyna
    #  149210140: ['Iskrzynia', 'Morwawa'], # Iskrzynia
    #  154180170: ['Wiślina', 'Motława'], # Wiślina
    #  152190100: ['Bielawy', 'Mroga'], # Bielawy
    #  149200080: ['Mszana Dolna', 'Mszanka'], # Mszana Dolna
    #  153200020: ['Szreńsk', 'Mławka'], # Szreńsk
    #  150170170: ['Branice 2', 'Młynówka'], # Branice 2
    #  149180070: ['Cieszyn', 'Młynówka'], # Cieszyn
    #  152210060: ['Zambski Kościelne', 'Narew'], # Zambski Kościelne
    #  153220130: ['Strękowa Góra', 'Narew'], # Strękowa Góra
    #  152230090: ['Narew', 'Narew'], # Narew
    #  153220010: ['Piątnica-Łomża', 'Narew'], # Piątnica-Łomża
    #  153220070: ['Wizna', 'Narew'], # Wizna
    #  153210090: ['Ostrołęka', 'Narew'], # Ostrołęka
    #  152230040: ['Ploski', 'Narew'], # Ploski
    #  153220270: ['Babino', 'Narew'], # Babino
    #  152200130: ['Orzechowo', 'Narew'], # Orzechowo
    #  153210210: ['Nowogród', 'Narew'], # Nowogród
    #  152220080: ['Suraż', 'Narew'], # Suraż
    #  152230190: ['Białowieża', 'Narewka'], # Białowieża
    #  152230100: ['Narewka', 'Narewka'], # Narewka
    #  151190040: ['Lutomiersk', 'Ner'], # Lutomiersk
    #  151180160: ['Poddębice', 'Ner'], # Poddębice
    #  152180150: ['Dąbie', 'Ner'], # Dąbie
    #  153220230: ['Kulesze Chobotki', 'Nereśl'], # Kulesze Chobotki
    #  153220280: ['Białobrzegi', 'Netta'], # Białobrzegi
    #  150200030: ['Brzegi', 'Nida'], # Brzegi
    #  150200080: ['Pinczów', 'Nida'], # Pinczów
    #  151180150: ['Widawa', 'Nieciecz'], # Widawa
    #  149200120: ['Niedzica', 'Niedziczanka'], # Niedzica
    #  151180030: ['Kuźnica Skakawska', 'Niesób'], # Kuźnica Skakawska
    #  154190040: ['Dolna Kępa', 'Nogat'], # Dolna Kępa
    #  152150090: ['Santok', 'Noteć'], # Santok
    #  153170100: ['Nakło-Zachód', 'Noteć'], # Nakło-Zachód
    #  152150140: ['Gościmiec', 'Noteć'], # Gościmiec
    #  153160170: ['Ujście', 'Noteć'], # Ujście
    #  152160010: ['Krzyż', 'Noteć'], # Krzyż
    #  153170010: ['Białośliwie', 'Noteć'], # Białośliwie
    #  152150190: ['Nowe Drezdenko', 'Noteć'], # Nowe Drezdenko
    #  152180030: ['Pakość', 'Noteć'], # Pakość
    #  152160070: ['Czarnków', 'Noteć'], # Czarnków
    #  152220070: ['Brańsk', 'Nurzec'], # Brańsk
    #  150170100: ['Kopice', 'Nysa Kłodzka'], # Kopice
    #  150160220: ['Bardo Śląskie', 'Nysa Kłodzka'], # Bardo Śląskie
    #  150160180: ['Kłodzko', 'Nysa Kłodzka'], # Kłodzko
    #  150170060: ['Nysa', 'Nysa Kłodzka'], # Nysa
    #  150160170: ['Bystrzyca Kłodzka', 'Nysa Kłodzka'], # Bystrzyca Kłodzka
    #  150170140: ['Skorogoszcz', 'Nysa Kłodzka'], # Skorogoszcz
    #  150160190: ['Międzylesie', 'Nysa Kłodzka'], # Międzylesie
    #  151160090: ['Jawor', 'Nysa Szalona'], # Jawor
    #  151160070: ['Winnica', 'Nysa Szalona'], # Winnica
    #  150140020: ['Sieniawka', 'Nysa Łużycka'], # Sieniawka
    #  151140010: ['Gubin', 'Nysa Łużycka'], # Gubin
    #  151140040: ['Przewóz', 'Nysa Łużycka'], # Przewóz
    #  151140060: ['Zgorzelec', 'Nysa Łużycka'], # Zgorzelec
    #  152150100: ['Bledzew', 'Obra'], # Bledzew
    #  149200150: ['Tylmanowa', 'Ochotnica'], # Tylmanowa
    #  151160060: ['Głogów', 'Odra'], # Głogów
    #  150170090: ['Brzeg (most)', 'Odra'], # Brzeg (most)
    #  152150050: ['Nietków', 'Odra'], # Nietków
    #  153140030: ['Gryfino', 'Odra'], # Gryfino
    #  153140020: ['Widuchowa', 'Odra'], # Widuchowa
    #  153140050: ['Szczecin', 'Odra'], # Szczecin
    #  151150150: ['Nowa Sól', 'Odra'], # Nowa Sól
    #  150170290: ['Opole - Groszowice', 'Odra'], # Opole - Groszowice
    #  149180300: ['Olza', 'Odra'], # Olza
    #  151160150: ['Malczyce', 'Odra'], # Malczyce
    #  149180020: ['Chałupki', 'Odra'], # Chałupki
    #  151170030: ['Trestno', 'Odra'], # Trestno
    #  150170040: ['Oława', 'Odra'], # Oława
    #  152140060: ['Kostrzyn n. Odrą', 'Odra'], # Kostrzyn n. Odrą
    #  152140050: ['Słubice', 'Odra'], # Słubice
    #  152140010: ['Bielinek', 'Odra'], # Bielinek
    #  150180060: ['Racibórz Miedonia', 'Odra'], # Racibórz Miedonia
    #  150170130: ['Ujście Nysy Kłodzkiej', 'Odra'], # Ujście Nysy Kłodzkiej
    #  152140130: ['Połęcko', 'Odra'], # Połęcko
    #  149180010: ['Krzyżanowice', 'Odra'], # Krzyżanowice
    #  152140020: ['Gozdowice', 'Odra'], # Gozdowice
    #  151160170: ['Brzeg Dolny', 'Odra'], # Brzeg Dolny
    #  152150130: ['Cigacice', 'Odra'], # Cigacice
    #  150180030: ['Koźle', 'Odra'], # Koźle
    #  152140090: ['Biała Góra', 'Odra'], # Biała Góra
    #  151160130: ['Ścinawa', 'Odra'], # Ścinawa
    #  151180090: ['Niechmirów', 'Oleśnica'], # Niechmirów
    #  149180030: ['Łaziska', 'Olza'], # Łaziska
    #  149180130: ['Istebna', 'Olza'], # Istebna
    #  149180060: ['Cieszyn', 'Olza'], # Cieszyn
    #  153210070: ['Białobrzeg Bliższy', 'Omulew'], # Białobrzeg Bliższy
    #  150170160: ['Branice 1', 'Opawa'], # Branice 1
    #  151160200: ['Korzeńsko', 'Orla'], # Korzeńsko
    #  152230030: ['Chraboły', 'Orlanka'], # Chraboły
    #  152210100: ['Czarnowo', 'Orz'], # Czarnowo
    #  152210030: ['Maków Mazowiecki', 'Orzyc'], # Maków Mazowiecki
    #  153180150: ['Rogóźno', 'Osa'], # Rogóźno
    #  150170180: ['Racławice Śląskie', 'Osobłoga'], # Racławice Śląskie
    #  149220020: ['Szczawne', 'Osława'], # Szczawne
    #  149220050: ['Zagórz', 'Osława'], # Zagórz
    #  150170030: ['Oława 2', 'Oława'], # Oława 2
    #  150170010: ['Zborowice', 'Oława'], # Zborowice
    #  151180010: ['Ołobok', 'Ołobok'], # Ołobok
    #  154150040: ['Bardy', 'Parsęta'], # Bardy
    #  154150050: ['Białogard', 'Parsęta'], # Białogard
    #  153160020: ['Tychówko', 'Parsęta'], # Tychówko
    #  154190170: ['Łozy', 'Pasłęka'], # Łozy
    #  154190140: ['Braniewo', 'Pasłęka'], # Braniewo
    #  153200030: ['Kalisty', 'Pasłęka'], # Kalisty
    #  153200040: ['Tomaryny', 'Pasłęka'], # Tomaryny
    #  150160020: ['Świebodzice', 'Pełcznica'], # Świebodzice
    #  149220010: ['Nowosielce', 'Pielnica'], # Nowosielce
    #  151200120: ['Białobrzegi', 'Pilica'], # Białobrzegi
    #  151200090: ['Nowe Miasto/Pilicą', 'Pilica'], # Nowe Miasto/Pilicą
    #  150190280: ['Wąsosz', 'Pilica'], # Wąsosz
    #  151200020: ['Spała', 'Pilica'], # Spała
    #  151190100: ['Sulejów', 'Pilica'], # Sulejów
    #  151190090: ['Przedbórz', 'Pilica'], # Przedbórz
    #  153210170: ['Ptaki', 'Pisa'], # Ptaki
    #  153210220: ['Dobrylas', 'Pisa'], # Dobrylas
    #  153210190: ['Pisz', 'Pisa'], # Pisz
    #  154210090: ['Giżycko', 'Pisa (Kanał Giżycki)'], # Giżycko
    #  150160130: ['Mościsko', 'Piława'], # Mościsko
    #  150160140: ['Dzierżoniów', 'Piława'], # Dzierżoniów
    #  150150190: ['Podgórzyn', 'Podgórna'], # Podgórzyn
    #  150210220: ['Włochy', 'Pokrzywianka'], # Włochy
    #  151170060: ['Bogdaj', 'Polska Woda'], # Bogdaj
    #  151160160: ['Rydzyna', 'Polski Rów'], # Rydzyna
    #  149200290: ['Muszyna', 'Poprad'], # Muszyna
    #  149200220: ['Stary Sącz', 'Poprad'], # Stary Sącz
    #  149200010: ['Poronin', 'Poroniec'], # Poronin
    #  149190300: ['Kościelisko-Kiry', 'Potok Kościeliski'], # Kościelisko-Kiry
    #  152180060: ['Posoka', 'Powa'], # Posoka
    #  151180070: ['Gorzów Śląski', 'Prosna'], # Gorzów Śląski
    #  151170110: ['Bogusław', 'Prosna'], # Bogusław
    #  151180040: ['Mirków', 'Prosna'], # Mirków
    #  151180020: ['Piwonice', 'Prosna'], # Piwonice
    #  150170110: ['Prudnik', 'Prudnik'], # Prudnik
    #  150190180: ['Jeleń', 'Przemsza'], # Jeleń
    #  150190190: ['Piwoń', 'Przemsza'], # Piwoń
    #  150190330: ['Ojców', 'Prądnik'], # Ojców
    #  150180040: ['Bojanów', 'Psina'], # Bojanów
    #  149180090: ['Borki Mizerów', 'Pszczynka'], # Borki Mizerów
    #  149180220: ['Pszczyna', 'Pszczynka'], # Pszczyna
    #  150220120: ['Zakłodzie', 'Pór'], # Zakłodzie
    #  149190310: ['Stróża', 'Raba'], # Stróża
    #  149200060: ['Mszana Dolna', 'Raba'], # Mszana Dolna
    #  149200090: ['Dobczyce', 'Raba'], # Dobczyce
    #  149200040: ['Kasinka Mała', 'Raba'], # Kasinka Mała
    #  149200170: ['Proszówki', 'Raba'], # Proszówki
    #  149190340: ['Rabka 2', 'Raba'], # Rabka 2
    #  154160020: ['Białogórzyno', 'Radew'], # Białogórzyno
    #  151210060: ['Rogożek', 'Radomka'], # Rogożek
    #  154180060: ['Goręczyno', 'Radunia'], # Goręczyno
    #  154180270: ['Pruszcz Gdański', 'Radunia'], # Pruszcz Gdański
    #  152200010: ['Kęszyce', 'Rawka'], # Kęszyce
    #  154180080: ['Wejherowo', 'Reda'], # Wejherowo
    #  154150010: ['Trzebiatów', 'Rega'], # Trzebiatów
    #  153150050: ['Resko', 'Rega'], # Resko
    #  153140190: ['Regalica Szczecin', 'Regalica'], # Regalica Szczecin
    #  152180140: ['Grzegorzew', 'Rgilewka'], # Grzegorzew
    #  149210060: ['Topoliny', 'Ropa'], # Topoliny
    #  149210030: ['Klęczany', 'Ropa'], # Klęczany
    #  149210010: ['Ropa', 'Ropa'], # Ropa
    #  153210120: ['Walery', 'Rozoga'], # Walery
    #  150180130: ['Rybnik Stodoły', 'Ruda'], # Rybnik Stodoły
    #  150180110: ['Ruda Kozielska', 'Ruda'], # Ruda Kozielska
    #  150180280: ['Rybnik Gotartowice', 'Ruda'], # Rybnik Gotartowice
    #  150190310: ['Balice', 'Rudawa'], # Balice
    #  153210180: ['Zaruzie', 'Ruź'], # Zaruzie
    #  149220130: ['Zatwarnica', 'San'], # Zatwarnica
    #  150210210: ['Radomysl', 'San'], # Radomysl
    #  149220030: ['Olchowce', 'San'], # Olchowce
    #  149220150: ['Dwernik', 'San'], # Dwernik
    #  149220190: ['Przemyśl', 'San'], # Przemyśl
    #  149220060: ['Lesko', 'San'], # Lesko
    #  149220040: ['Dynów', 'San'], # Dynów
    #  150220030: ['Nisko', 'San'], # Nisko
    #  150220100: ['Jarosław', 'San'], # Jarosław
    #  150220070: ['Rzuchów', 'San'], # Rzuchów
    #  150220090: ['Leżachów', 'San'], # Leżachów
    #  153230130: ['Harasimowicze', 'Sidra'], # Harasimowicze
    #  149190180: ['Wadowice', 'Skawa'], # Wadowice
    #  149190210: ['Sucha Beskidzka 2', 'Skawa'], # Sucha Beskidzka 2
    #  149190290: ['Jordanów', 'Skawa'], # Jordanów
    #  149190170: ['Zator', 'Skawa'], # Zator
    #  149190260: ['Osielec', 'Skawa'], # Osielec
    #  149190220: ['Skawica Dolna', 'Skawica'], # Skawica Dolna
    #  149190270: ['Radziszów', 'Skawinka'], # Radziszów
    #  151150160: ['Zagrodno', 'Skora'], # Zagrodno
    #  151150180: ['Chojnów', 'Skora'], # Chojnów
    #  151140030: ['Przewoźniki', 'Skroda'], # Przewoźniki
    #  149220080: ['Cisna', 'Solinka'], # Cisna
    #  149220100: ['Terka', 'Solinka'], # Terka
    #  150190160: ['Oświęcim', 'Soła'], # Oświęcim
    #  149190100: ['Żywiec', 'Soła'], # Żywiec
    #  149190050: ['Rajcza', 'Soła'], # Rajcza
    #  149190120: ['Czaniec (Kobiernice)', 'Soła'], # Czaniec (Kobiernice)
    #  149190080: ['Cięcina', 'Soła'], # Cięcina
    #  150150200: ['Sosnówka', 'Sośniak'], # Sosnówka
    #  149210120: ['Godowa', 'Stobnica'], # Godowa
    #  150170150: ['Karłowice (Wapienniki)', 'Stobrawa'], # Karłowice (Wapienniki)
    #  149200480: ['Łapanów', 'Stradomka'], # Łapanów
    #  149200130: ['Stradomka', 'Stradomka'], # Stradomka
    #  150180010: ['Kamionka', 'Stradunia'], # Kamionka
    #  149190200: ['Sucha Beskidzka', 'Stryszawka'], # Sucha Beskidzka
    #  151160180: ['Bogdaszowice', 'Strzegomka'], # Bogdaszowice
    #  150160030: ['Chwaliszów', 'Strzegomka'], # Chwaliszów
    #  150160090: ['Łażany', 'Strzegomka'], # Łażany
    #  153230170: ['Nowosiółki', 'Supraśl'], # Nowosiółki
    #  153230110: ['Supraśl', 'Supraśl'], # Supraśl
    #  153230010: ['Fasty', 'Supraśl'], # Fasty
    #  151180050: ['Dębe', 'Swędrnia'], # Dębe
    #  154190020: ['Tujsk', 'Szkarpawa'], # Tujsk
    #  153210140: ['Szkwa', 'Szkwa'], # Szkwa
    #  150220140: ['Charytany', 'Szkło'], # Charytany
    #  151150130: ['Szprotawa 2', 'Szprotawa'], # Szprotawa 2
    #  150200070: ['Biskupice', 'Szreniawa'], # Biskupice
    #  151160220: ['Kanclerzowice', 'Sąsiecznica'], # Kanclerzowice
    #  154170010: ['Słupsk', 'Słupia'], # Słupsk
    #  154170120: ['Soszyca', 'Słupia'], # Soszyca
    #  150220050: ['Harasiuki', 'Tanew'], # Harasiuki
    #  150220160: ['Osuchy', 'Tanew'], # Osuchy
    #  150220040: ['Sarzyna', 'Trzebośnica'], # Sarzyna
    #  151220080: ['Tchórzew', 'Tyśmienica'], # Tchórzew
    #  149200510: ['Brzesko-Miasto', 'Uszwica'], # Brzesko-Miasto
    #  150200140: ['Borzęcin', 'Uszwica'], # Borzęcin
    #  149200370: ['Brzesko-Okocim', 'Uszwica'], # Brzesko-Okocim
    #  152200090: ['Krubice', 'Utrata'], # Krubice
    #  149180230: ['Podkępie', 'Wapienica'], # Podkępie
    #  152150080: ['Santok 2', 'Warta'], # Santok 2
    #  151190060: ['Bobry', 'Warta'], # Bobry
    #  152170060: ['Nowa Wieś Podgórna', 'Warta'], # Nowa Wieś Podgórna
    #  151180100: ['Osjaków', 'Warta'], # Osjaków
    #  152180050: ['Sławsk', 'Warta'], # Sławsk
    #  152150010: ['Świerkocin', 'Warta'], # Świerkocin
    #  152180120: ['Koło', 'Warta'], # Koło
    #  152150110: ['Skwierzyna', 'Warta'], # Skwierzyna
    #  151180080: ['Sieradz', 'Warta'], # Sieradz
    #  152140070: ['Kostrzyn n. Odrą', 'Warta'], # Kostrzyn n. Odrą
    #  152170080: ['Pyzdry', 'Warta'], # Pyzdry
    #  150190240: ['Kręciwilk', 'Warta'], # Kręciwilk
    #  152150200: ['Międzychód', 'Warta'], # Międzychód
    #  151180130: ['Działoszyn', 'Warta'], # Działoszyn
    #  150190150: ['Poraj', 'Warta'], # Poraj
    #  152160050: ['Wronki', 'Warta'], # Wronki
    #  150190200: ['Lgota Nadwarcie', 'Warta'], # Lgota Nadwarcie
    #  152160140: ['Poznań Most Rocha', 'Warta'], # Poznań Most Rocha
    #  151180120: ['Burzenin', 'Warta'], # Burzenin
    #  152170010: ['Śrem', 'Warta'], # Śrem
    #  152160100: ['Oborniki', 'Warta'], # Oborniki
    #  152150040: ['Gorzów Wielkopolski', 'Warta'], # Gorzów Wielkopolski
    #  151180110: ['Uniejów', 'Warta'], # Uniejów
    #  152170130: ['Ląd', 'Warta'], # Ląd
    #  154200010: ['Bornity', 'Wałsza'], # Bornity
    #  153180010: ['Czarna Woda', 'Wda'], # Czarna Woda
    #  153180060: ['Krąplewice', 'Wda'], # Krąplewice
    #  153190150: ['Lidzbark', 'Wel'], # Lidzbark
    #  153190130: ['Kuligi (Nowe Miasto)', 'Wel'], # Kuligi (Nowe Miasto)
    #  149220110: ['Kalnica', 'Wetlina'], # Kalnica
    #  152160110: ['Kowanówko', 'Wełna'], # Kowanówko
    #  149220200: ['Krówniki', 'Wiar'], # Krówniki
    #  151210050: ['Gusin', 'Wiała'], # Gusin
    #  151170050: ['Zbytowa', 'Widawa'], # Zbytowa
    #  151170010: ['Krzyżanowice', 'Widawa'], # Krzyżanowice
    #  151170090: ['Namysłów', 'Widawa'], # Namysłów
    #  151180140: ['Podgórze', 'Widawka'], # Podgórze
    #  151190020: ['Szczerców', 'Widawka'], # Szczerców
    #  151180170: ['Rogóźno', 'Widawka'], # Rogóźno
    #  149190390: ['Ludźmierz', 'Wielki Rogoźnik'], # Ludźmierz
    #  150210140: ['Brzeźnica', 'Wielopolka'], # Brzeźnica
    #  150230040: ['Krasnystaw', 'Wieprz'], # Krasnystaw
    #  150230010: ['Nielisz', 'Wieprz'], # Nielisz
    #  151220090: ['Lubartów', 'Wieprz'], # Lubartów
    #  151220010: ['Kośmin', 'Wieprz'], # Kośmin
    #  150230080: ['Michałów', 'Wieprz'], # Michałów
    #  151230010: ['Trawniki', 'Wieprz'], # Trawniki
    #  154160070: ['Stary Kraków', 'Wieprza'], # Stary Kraków
    #  154160120: ['Korzybie', 'Wieprza'], # Korzybie
    #  154160150: ['Darłowo', 'Wieprza'], # Darłowo
    #  149190160: ['Rudze', 'Wieprzówka'], # Rudze
    #  150200020: ['Bocheniec', 'Wierna Rzeka'], # Bocheniec
    #  153180030: ['Bożepole', 'Wierzyca'], # Bożepole
    #  153180110: ['Brody Pomorskie', 'Wierzyca'], # Brody Pomorskie
    #  150160210: ['Wilkanów', 'Wilczka'], # Wilkanów
    #  153220090: ['Czachy', 'Wissa'], # Czachy
    #  149220210: ['Nienowice', 'Wisznia'], # Nienowice
     153180080: [134, 53.3687562918215, 18.426891396275536], # Chełmno
    #  154180220: ['Gdańska Głowa', 'Wisła'], # Gdańska Głowa
     154180210: [0, 54.35963408932706, 18.949361344675392], # Ujście Wisły
    #  149180160: ['Wisła Czarne', 'Wisła'], # Wisła Czarne
     154180190: [5, 54.308482596025065, 18.932495157472076], # Przegalina
     154180200: [3, 54.33439619271618, 18.940067918738112], # Świbno
     152200110: [390, 52.42763727463254, 20.69036438411345], # Modlin
     153180100: [107, 53.483490342674834, 18.739834957997413], # Grudziądz
    #  150190170: ['Pustynia', 'Wisła'], # Pustynia
     152200030: [352, 52.38215826778921, 20.18587330017835], # Wyszogród
     152200150: [370, 52.39497960804686, 20.42621028370233], # Wychódźc
     150210180: [643, 50.88523693158125, 21.832825421385216], # Annopol
    #  149190060: ['Jawiszowice', 'Wisła'], # Jawiszowice
     150210190: [654, 50.80604295846389, 21.86484570551917], # Zawichost
     154180150: [33, 54.092983076194955, 18.806583829987705], # Tczew
    #  149180110: ['Ustroń Obłaziec', 'Wisła'], # Ustroń Obłaziec
    #  152210170: ['Warszawa-Bulwary', 'Wisła'], # Warszawa-Bulwary
    #  149180240: ['Goczałkowice', 'Wisła'], # Goczałkowice
     150200060: [812, 50.13700541497056, 20.46989258447206], # Sierosławice
     150190360: [904, 50.05662419240478, 19.293913548211666], # Gromiec
    #  149180100: ['Skoczów', 'Wisła'], # Skoczów
     150190340: [875, 50.03109929339496, 19.8198813586877], # Kraków - Bielany
    #  150210150: ['Koło', 'Wisła'], # Koło
     151210190: [570, 51.43726845382657, 21.94291005434442], # Puławy
    #  150200100: ['Popędzynka', 'Wisła'], # Popędzynka
    #  150200150: ['Karsy', 'Wisła'], # Karsy
    #  151210120: ['Dęblin', 'Wisła'], # Dęblin
    #  150190260: ['Smolice', 'Wisła'], # Smolice
    #  149180210: ['Zabrzeg', 'Wisła'], # Zabrzeg
     153180090: [208, 53.01538806847525, 18.655435414118934], # Toruń
     152190030: [262, 52.66481106343718, 19.071600866597095], # Włocławek
     149190230: [0, 49.98127082844883, 19.66296748623251], # Czernichów - Prom
     149180140: [0, 49.6356377383622, 18.886210936584643], # Wisła
     150210170: [672, 50.67387943016068, 21.757843936209085], # Sandomierz
     152190120: [333, 52.431346063055585, 19.955670014937475], # Kępa Polska
    #  152210010: ['Warszawa', 'Wisła'], # Warszawa
     153180020: [167, 53.14427475316668, 18.171618359712223], # Fordon
     152210040: [432, 52.176777790297876, 21.128404319736752], # Warszawa - Nadwilanówka
     150190140: [0, 50.06390860244547, 19.19250842566753], # Bieruń Nowy
     149180080: [0, 49.869170799701145, 18.749649108588148], # Drogomyśl
     150210020: [747, 50.31966298146264, 21.068028055089734], # Szczucin
     150220080: [0, 50.16230793852418, 22.54723956755295], # Tryńcza
     149210150: [0, 50.1071142246683, 22.069270424378406], # Puławy
     150220010: [0, 50.0300596854135, 22.005425056621405], # Rzeszów
     149210160: [0, 50.18919488946855, 22.545972389228886], # Sieniawa
     149210130: [0, 49.87351636832064, 21.817713016415002], # Żarnowa
     149210110: [0, 49.69639926263033, 21.761783572848817], # Krosno
     149210050: [0, 49.77454897253637, 21.411194091666736], # Krajowice
     149210090: [0, 49.51954198314392, 21.471721132195068], # Krempna-Kotań
     150210120: [0, 50.28077745950781, 21.42646425093088], # Mielec 2
#      149210040: ['Łabuzie', 'Wisłoka'], # Łabuzie
     149210070: [0, 49.72944289455662, 21.45976771209955], # Żółków
     150210130: [0, 50.13407263621631, 21.48207456710603], # Pustków
     151140050: [0, 51.04529495299441, 14.971892752988936], # Ręczyn
     151150020: [0, 51.02012151524581, 15.03304060375718], # Ostróżno
     152200120: [0, 52.56192523259792, 20.666045572730173], # Borkowo
     152200020: [0, 52.93062179487059, 20.1718500192979], # Trzciniec
#      149190040: ['Ujsoły', 'Woda Ujsolska'], # Ujsoły
     149220180: [0,49.18562073490515, 22.68362732706532], # Stuposiany
     152170120: [0, 52.20351787341474, 17.763141077092637], # Samarzewo
     154190100: [0, 54.070598441867816, 19.660632798509955], # Pasłęk
     154210080: [0, 54.24410522777647, 21.72006781853944], # Prynowo
     154210100: [0, 54.323352819243766, 21.9819597513659], # Mieduniszki
     154210070: [0, 54.2099686896293, 21.74276176403892], # Węgorzewo
#      153140040: ['Trzebież', 'Zalew Szczeciński'], # Trzebież
#      154190030: ['Osłonka', 'Zalew Wiślany'], # Osłonka
#      154190130: ['Nowa Pasłęka', 'Zalew Wiślany'], # Nowa Pasłęka
#      154190090: ['Tolkmicko', 'Zalew Wiślany'], # Tolkmicko
#      154190050: ['Nowe Batorowo', 'Zalew Wiślany'], # Nowe Batorowo
#      153140010: ['Świnoujście', 'Zatoka Pomorska (ujście Świny)'], # Świnoujście
#      154180090: ['Puck', 'Zatoka Pucka'], # Puck
#      152230120: ['Bondary - Siemianówka', 'Zb Siemianówka'], # Bondary - Siemianówka
#      152230110: ['Bondary - Siemianówka', 'Zb Siemianówka'], # Bondary - Siemianówka
#      152210150: ['Popowo', 'Zb. Dębe'], # Popowo
#      152180170: ['Popowo', 'Zb. Gopło'], # Popowo
     150170080: [0, 50.284130063859834, 17.426714327872794], # Jarnołtówek
#      152150270: ['Zbąszyń', 'jez. Błędno'], # Zbąszyń
#      153160040: ['Czaplinek', 'jez. Drawsko'], # Czaplinek
#      153160300: ['Wielimie', 'jez. Wielimskie'], # Wielimie
#      153140200: ['Morzyczyn', 'jez.Miedwie'], # Morzyczyn
#      150210030: ['Mocha', 'Łagowica'], # Mocha
     154170160: [0, 54.54263336211772, 17.74403593099487], # Lębork
     154180020: [0, 54.43974613252891, 18.029801003122994], # Miłoszewo
     153170040: [0, 53.154773172305674, 17.26569388706088], # Wyrzysk
     150150090: [0, 50.863904952093044, 15.794954596543345], # Łomnica
#      149200200: ['Jakubkowice', 'Łososina'], # Jakubkowice
     149200260: [0, 49.62397982173495, 20.72698384303998], # Nowy Sącz 1
     154170080: [0, 54.41895376805381, 17.415844143937356], # Łupawa
     154170060: [0, 54.662057992334304, 17.21225756525158], # Smołdzino
     151180060: [0, 51.51874618313202, 18.224538768831565], # Kraszewice
     154200030: [0, 54.02563897602873, 20.397215239754377], # Smolajny
     154210010: [0, 54.272626513719715, 21.009827466439237], # Sępopol
     153200070: [0, 53.75568081443124, 20.471582203657118], # Olsztyn
     150210200: [0, 50.57571607910604, 21.91185276203964], # Grębów
     149190140: [0, 49.71156423501853, 19.268216562116237], # Łękawica
     150170120: [0, 50.64062635586403, 17.624635559645096], # Niemodlin
     150160080: [0, 50.55317645485947, 16.432338284861352], # Tłumaczów
     150160100: [0, 50.48583209602621, 16.571330374945788], # Gorzuchów
     153220180: [0, 53.15625499691204, 22.67281280958423], # Zawady
     150160280: [0, 50.88912977472603, 16.990148528957704], # Borów
     150160250: [0, 50.80193951891598, 16.892764834624533], # Białobrzezie
     151160230: [0, 51.04343179729945, 16.98609419405631], # Ślęza
     152210070: [0, 52.1395268086873, 21.33117492880225], # Wólka Mlądzka
#      154190010: ['Nowy Dwór Gdański', 'Święta'], # Nowy Dwór Gdański
     150210040: [0, 50.97314651633364, 21.091840774138454], # Rzepin
     149190090: [0, 49.58008425561489, 19.155709023662272], # Żabnica
     149190070: [0, 49.728679544537584, 19.141557433377855] # Łodygowice
}

location = pd.DataFrame(location).T
location.columns = ["kilometer","latitude","longitude"]
stations = stations.merge(location, left_on="station_id", right_index=True, how="left")

for index, row in stations.iterrows():
    with engine.connect() as connection:

        
        row = row.to_frame().T
        row.to_sql(hstable, engine, if_exists='append', index=False)
        #print(row)


url = "https://danepubliczne.imgw.pl/api/data/synop/"
stations = pd.read_json(url)
stations = stations[["id_stacji", "stacja"]]
stations.columns = ["station_id", "station_name"]

location = {
    12295: [53.13269289045303, 23.158805938259118], # Białystok
    12600: [49.810628212127575, 19.042410897677918], # Bielsko Biała
    12235: [53.69978486646282, 17.56766267769026], # Chojnice
    12550: [50.81580763827262, 19.107320454070674], # Częstochowa
    12160: [54.165224998394116, 19.403796452386572], # Elbląg
    12155: [54.362363303522095, 18.602111922492217], # Gdańsk
    12300: [52.73813569027436, 15.222370660098962], # Gorzów
    12135: [54.63101862486838, 18.789103112082355], # Hel
    12500: [50.895793650319845, 15.734047051265717], # Jelenia Góra
    12435: [51.75408459397205, 18.08958543200005], # Kalisz
    12650: [49.23267652946702, 19.981539152940517], # Kasprowy Wierch
    12560: [50.23161627816384, 19.01688588541984], # Katowice
    12185: [54.08075404348663, 21.377720880406926], # Kętrzyn
    12570: [50.86268780114404, 20.610147014142314], # Kielce
    12520: [50.44128249489103, 16.649181304133887], # Kłodzko
    12345: [52.19768981229449, 18.632711501592155], # Koło
    12100: [54.17868858498237, 15.586087188356132], # Kołobrzeg
    12105: [54.208605429428715, 16.21597123004451], # Koszalin
    12488: [51.588335447500306, 21.535525000826606], # Kozienice
    12566: [50.060634552792976, 19.941863214352235], # Kraków
    12670: [49.69253679952997, 21.760346366452556], # Krosno
    12415: [51.20510065667285, 16.16822580777957], # Legnica
    12690: [49.47487011580228, 22.32990885853269], # Lesko
    12418: [51.84840081781375, 16.573709433939538], # Leszno
    12125: [54.537479200739384, 17.750647706982026], # Lębork
    12495: [51.2458202717939, 22.560335807978035], # Lublin
    12120: [54.761849571323765, 17.558522964597046], # Łeba
    12465: [51.77006040236823, 19.45998864233709], # Łódź
    12280: [53.800196375630485, 21.58105899820593], # Mikołajki
    12270: [53.125899548661806, 20.383679235674922], # Mława
    12660: [49.608732614602545, 20.707490091011078], # Nowy Sącz
    12272: [53.780250650886785, 20.473250789016195], # Olsztyn
    12530: [50.683955109281506, 17.90941523309258], # Opole
    12285: [53.08137942773691, 21.578297649301778], # Ostrołęka
    12230: [53.15097382355849, 16.759637733812898], # Piła
#     12001: [], # Platforma
    12360: [52.54248524481034, 19.707148489864142], # Płock
    12330: [52.41049941320378, 16.88792845148401], # Poznań
    12695: [49.78419691777446, 22.7754725879192], # Przemyśl
    12540: [50.0892395935134, 18.226571675981493], # Racibórz
    12210: [53.77071926801013, 15.408595795905205], # Resko
    12580: [50.03827578806589, 22.000126733421386], # Rzeszów
    12585: [50.68267829840306, 21.752134484951092], # Sandomierz
    12385: [52.167537357279635, 22.271915542355824], # Siedlce
    12310: [52.360978508162916, 14.585134600189683], # Słubice
    12469: [51.35527180036615, 19.886226079255206], # Sulejów
    12195: [54.10351361676021, 22.931530779755466], # Suwałki
    12205: [53.42794459182344, 14.564954927484074], # Szczecin
    12215: [53.70867312162282, 16.69426051466759], # Szczecinek
    12510: [50.74242796984402, 15.738003649448991], # Śnieżka
    12200: [53.87776701433164, 14.29365036764134], # Świnoujście
    12575: [50.02391698879909, 20.963858647306072], # Tarnów
    12399: [52.075023210575246, 23.616381457854132], # Terespol
    12250: [53.01868031091065, 18.620083641865506], # Toruń
    12115: [54.57950786831226, 16.860334579962604], # Ustka
    12375: [52.22907004214596, 21.031663841297622], # Warszawa
    12455: [51.22432786509302, 18.572331610393057], # Wieluń
    12497: [51.54218818839693, 23.53312707332828], # Włodawa
    12424: [51.133457828705865, 16.99666581871236], # Wrocław
    12625: [49.27609412494612, 19.977994368788597], # Zakopane
    12595: [50.721377255845674, 23.25864032382748], # Zamość
    12400: [51.94259569159023, 15.509028918315687], # Zielona Góra
}

location = pd.DataFrame(location).T
location.columns = ["latitude","longitude"]
stations = stations.merge(location, left_on="station_id", right_index=True, how="left")

for index, row in stations.iterrows():
    with engine.connect() as connection:

        
        row = row.to_frame().T
        row.to_sql(wstable, engine, if_exists='append', index=False)


server.stop()
