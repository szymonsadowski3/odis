# Projekt "Monitoring ruchu internetowego"

## Architektura projektu 

![alt text](https://github.com/szymonsadowski3/odis/doc/img/diagram.png "Architecture diagram")

## Zależności systemowe

- python3
- rabbitMQ
- pmacct (wraz z pluginem do RabbitMQ - instrukcja instalacji zawarta jest w dokumencie https://github.com/pmacct/pmacct/blob/master/QUICKSTART w sekcji nr 8.)
- PostgreSQL

## Zależności dla pythona

- flask
- Flask-CORS
- flassger
- psycopg2
- dnspython
- waitress

Aby zainstalować zależności należy uruchomić komendę `pip3 install -r requirements.txt`

## Schemat DDL

Schemat DDL dla potrzebnych tabel w gotowym do uruchomienia skrypcie SQL znajduje się w lokalizacji `src/ddl/ddl.sql`

## Instrukcja uruchomienia

Po zainstalowaniu wspomnianych wcześniej zależności można przystąpić do uruchomienia programu.

1. Należy uruchomić program pmacctd z pluginem dla RabbitMQ i odpowiednią konfiguracją (plik amqp_plugin_config.cfg znajduje się w `src/amqp`):

`sudo pmacctd -P amqp -f amqp_plugin_config.cfg` 

więcej informacji na temat możliwości konfiguracyjnych znaleźć można pod adresem https://github.com/pmacct/pmacct/blob/master/CONFIG-KEYS

2. Należy uruchomić klienta konsumującego dane z kolejki RabbitMQ:

`python3 src/amqp/consume.py`

3. Należy uruchomić serwis REST API serwujący dane:

```
export PYTHONPATH=.
python3 src/rest_api/waitress_serve.py
```

4. Wówczas serwis będzie dostępny na porcie 5000.

## Dokumentacja/kontrakt serwisu Rest API

Po uruchomieniu serwisu pod endpointem /apidocs można uruchomić dokumentację "Swagger" serwisu.
Np. po uruchomieniu na localhoscie: http://localhost:5000/apidocs/

## Panel administratora RabbitMQ

Panel administratora RabbitMQ domyślnie uruchomiony jest pod portem 15672 np.:
http://localhost:15672

## Uruchomienie testów jednostkowych

python3 -m unittest test/*_test.py
