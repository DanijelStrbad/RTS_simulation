Klase koje služe kao memorija:
1 - upr_naredbe
UPR u nji pohranjuje svoje naredbe.

2 - sem_data
Podaci o tome koji je semafor u kojem stanju - crven ili zelen.

3 - ras_data
Podaci o tome gdje se nalaze auti i pješsaci.




Dretve:
UPR
Čita ras_data. Ovisno o tome ili internom brojaču postavlja naredbe u upr_naredbe.

SEM
Čita upr_naredbe. Prema upravljačkim naredbama postavlja stanje na svaki semafor upisivanjem u sem_data.

RAS
Čita ras_data i ovisno o tome puni R[][] - matricu koja predstavlja prikaz raskrižja.
Ispisuje R[][] matricu prikaza raskrižja.

AUTO & PJESAK
Postavi ras_data kada stigneš na svoje mjesto čekanja.
Čitaj i čekaj sem_data za svoj semafor. Kad je zeleno kreni i osvježi ras_data.
Kada prođeš, ponovo osvježi ras_data - da se zna da si prošao.


