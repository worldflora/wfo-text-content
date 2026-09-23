# e-flora South Africa Darwin Core Descriptions from IPT

The file contains tab delimited data on descriptions and vernacular names well matched to wfo ids.

Process - the one used:

used splitandref.py works with .txt no need to do db steps.

Looks at Type and Language in description file splits along both of those.
Added bibliographicCition from reference.txt. Parses out url.
Manual fix to change http to https.

Re run pointing to vernacular.txt 

Alt Process
Process:

1. Unzip the file
2. Import each of description, reference, taxon, vernacularname into SQLite database called /working/sa.sqlite. SQLite databases are in .gitignore so won't be checked in. You need to do this locally.
3. Delete the files that came out the DwC zip. No need to check them into github.
4. Run the script ...

# Issues

Vernacular many Languages not all supported.
Will need to work out what ones are available to use.

Afrikaans                       22426
English                         16086
Zulu                             5015
Xhosa                            2093
Unknown                          1301
Venda                             953
Tswana                            882
Southern Sotho (Sotho)            780
Tsonga                            745
Swati                             559
Shona                             555
Southern Sotho                    366
German                            343
Lozi                              343
Pedi; Sepedi; Northern Sotho      328
Northern Sotho (Pedi)             293
Ndebele                           288
Herero                            228
Sotho                             217
Swazi                             194
Wambo; Oshiwambo                  166
Kwangali                          114
Khoekhoe                          101
Kxoe; Khwedam                     100
Mbukushu; Thimbukushu              99
Manyo; Rumanyo                     95
Ju|'hoan                           82
Swahili                            78
Shambala                           70
Masai                              65
Tswati                             65
Shangana                           59
Chagga                             57
Siswati                            57
Ndau                               56
Kalanga                            55
Tonga                              55
IsiZulu                            45
Sukuma                             42
Shangaan                           36
Sesotho                            36
Hehe                               34
Gikuyu                             33
Nguni                              30
Nyamwezi                           29
Kikuyu                             29
Lobedu                             27
Mpondo                             27
Hausa                              27
!Xóõ                               25
Kiswahili                          24
Nama                               23
Manyika                            22
Oromugna                           22
Bondei                             21
Haya                               20
Pedi                               19
Malinke                            18
Ronga                              17
Fula                               17
Zezuru                             17
Meru                               16
Zinza                              16
Karanga                            16
Tanganyika                         15
Kilongo                            15
Pare                               15
Shambaa                            14
Arusha                             14
Amargna                            14
Digo                               13
Iraqw                              13
Hlengwe                            13
Pondo                              12
Thonga                             12
Kamba                              12
Arabic                             12
Sambaa                             12
Kgatla                             11
Kwena                              11
Nyika                              11
Lugishu                            11
Sebei                              11
Zigua                              11
Tawana                             11
Igbo (Ibo)                         10
Luo                                10
Luvale                             10
Gogo                               10
Lunyaneka                          10
Basotho                            10
Wolof                              10
!Kung Bushman                      10
ciYao                              10
Ovambo                             10
Yoruba                             10
Nyanja                             10
Mbukushu                            9
Somali                              9
Rukiga                              9
Luguru                              9
Tigrigna                            9
Baca                                9
Rungwe                              9
Marakwet                            9
Tlhaping                            9
Luganda                             9
Rangi                               9
Fipa                                8
Lovedu                              8
Subiya                              8
Lunda                               8
Ganda                               8
Chopi                               8
Suto                                8
Borana                              8
Bakone Suto                         8
Ngwaketse                           8
Kipsigis                            7
Tebele                              7
Creole                              7
Kimbundu                            7
Kwanyama                            7
Bemba                               7
Zigula                              7
Sangu                               7
Fingo                               6
Tigrinia                            6
Tigre                               6
Mbulu                               6
Rotse                               6
Gbaya                               6
Mbula                               5
Lamba                               5
Gorowa                              5
Bushman                             5
Fon                                 5
Diola                               5
Samburu                             5
Khoi                                5
Natives                             5
Serer                               5
Nyaneka                             5
Nyarwanda                           5
Spanish                             5
Runyankore                          5
Ngoni                               5
Nguu                                5
Usambara                            5
Mfengu                              5
Kanuri                              4
Konde                               4
Mwera                               4
Kinga                               4
Somalgna                            4
Dyula                               4
Nandi                               4
Kakamega                            4
ciCewa                              4
So                                  4
Gwanda                              4
Ila                                 4
Zaramo                              4
Lega                                4
Bambara                             4
Songea                              4
ciNyanja                            4
Dutch                               4
Latin                               4
Ewe                                 4
Rutoro                              4
Teita                               4
Kerewe                              4
Dogon                               4
Niominka                            4
Tululor                             4
Lusoga                              4
Chwabo                              4
Teso                                4
Banda                               4
Kikongo                             4
Fang                                4
Afrikaans, English                  4
Kunama                              3
Mbunga                              3
Saho                                3
Gishu                               3
Matengo                             3
Bilen                               3
Twi                                 3
Amhara                              3
ciTumbuka                           3
Giriama                             3
Uluguru                             3
Senga                               3
Lindi                               3
Nyakyusa                            3
Fiome                               3
Guro                                3
Mbozi                               3
Wolayetgna                          3
Portugese                           3
Dorobo                              3
Kilwa                               3
Gimirigna                           3
Sagara                              3
Lugbare                             3
Shien                               3
Mossi                               3
Pangani                             3
Rukonjo                             3
Edo                                 3
Mbeere                              3
Somalia                             3
Yao                                 3
Ha                                  3
Barotse                             3
Taita                               3
Tukuyu                              3
Efe                                 3
Nyiha                               3
Ngwato                              2
Acholi                              2
Kambo                               2
Luena                               2
Lese                                2
Morogoro                            2
Gula                                2
Masarwa Bushmen                     2
Bila                                2
Rufiji                              2
Lenge                               2
Barabaig                            2
Kirundi                             2
Nkomi                               2
Nyaturu                             2
Nguru                               2
Baule                               2
Safwa                               2
Chinambya                           2
Lunyore                             2
Bisa                                2
Dagari                              2
Bafia (Bekpak)                      2
Makonde                             2
Kondoa                              2
Naron Bushman                       2
Kefgna                              2
Fanti                               2
Ga                                  2
Sidamgna                            2
Bazyia                              2
Tiv                                 2
Kone                                2
Time                                2
Kilolo                              2
Nyindu                              2
Tugen                               2
Kilufi                              2
South Somalia                       2
Eshirma                             2
Rolong                              2
Uluy                                2
Nyankole                            2
Fuagi                               2
Mbengu                              2
Kele                                2
Mtoko                               2
ciTonga                             2
Wemenu                              2
Kuba                                2
Giriam                              2
Temba                               2
Tembu                               2
Guragigna                           2
Hei//om bushmen                     2
Kuangari                            2
!Ko Bushmen                         2
Grussi                              2
Zingwa                              2
Pogoro                              2
Southern Tswana                     2
Zungwa                              2
Somal                               1
Zande                               1
Nyankere                            1
Fant                                1
Ngowe                               1
Lugwe                               1
Tschaudjo                           1
Manja                               1
Kpe                                 1
Gurma                               1
Kxatla                              1
Luo acholi                          1
Karamojong                          1
Sarwa                               1
French                              1
Gando                               1
Orungu                              1
Bukoba                              1
Nyoro                               1
Kuria                               1
Nkoya                               1
Soninke                             1
Laadi                               1
Mambwe                              1
Mohoro                              1
Nyiramba                            1
Borenagna                           1
Totela                              1
Luchaye                             1
Hunde                               1
Mbugwe                              1
Chendao                             1
Ndonga                              1
Kwamba                              1
Ndao                                1
Afrikaans; English; German          1
Vidunda                             1
Toka                                1
Bacwana                             1
Bakusi                              1
Abe                                 1
Janzi                               1
Ngindo                              1
Nupe                                1
Sonjo                               1
Anecho                              1
Kono                                1
Dedza                               1
Adangwe                             1
Jaluo                               1
Griqua                              1
Madi                                1
Galoa                               1
Hindi                               1
English, Latin                      1
Gabbra                              1
Malete                              1
ciSukwa                             1
Lunyuli                             1
Akwapem                             1
Ijebu                               1
Duruma                              1
Luba                                1
Agni                                1
Sumbwa                              1
Musa                                1
Kulango                             1
Kaguru                              1
Vinza                               1
Soga                                1
Wasa                                1
Seguha                              1
Loango                              1
Cherangani                          1
Luo lango                           1
Haderigna                           1
Bende                               1
Kilimandjaro                        1
Tumbuka                             1
Nyanyeka                            1
Runyoro                             1
Pungo                               1
Chewa                               1
Kindodi                             1
Ndzima                              1
Kabras                              1
Kotoko                              1
Mai-Hederbai                        1
Subia                               1
Birom                               1
Mbundu                              1
Karamoja                            1
Pokot                               1
Kololo                              1
Ashanti                             1
Bukushu                             1
Mwangati                            1
Mlanje                              1
Turkana                             1
Multiple                            1
Bagamoya                            1
Mpongwe                             1
Thlokwa                             1
Balante                             1
Lunyul                              1
Ovamba                              1
Italian                             1
Lumba                               1
Sefwim Brosa                        1
San                                 1
Mende                               1
Northern Tswana                     1
Kitwa                               1
Buddu                               1
Boni                                1
Sindebele                           1
Ndengereko                          1
Jindwe                              1
Elgeyo                              1
Djerma                              1
Lenje                               1
Bangala                             1
Kongo                               1
Fula-Fulfulde                       1
Kisi                                1
Hidareb                             1
Kiga                                1
Dagomba                             1
Apindji                             1
Douala                              1
Tsenga                              1
Jaka                                1
Luabo                               1
Luganda, dialect Buddu              1
Susu                                1
Kano                                1
near Chirumbu                       1
Subyia                              1
Mixed                               1
Adja                                1
Miondo                              1
Aka pygmies                         1
Koranna                             1
Bamileke                            1
Kyimbila                            1
Nara                                1
Kwimba                              1
Lugwere                             1
Beembe                              1
Umbundu                             1
Bulu                                1
Tso                                 1
Lumwege                             1
kyaNgonde                           1
Songhai                             1
Tabwa                               1
afrikaans                           1
Padhola                             1