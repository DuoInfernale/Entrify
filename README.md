# Entrify - Entra ID Anwendungsverwaltung

Entrify ist eine auf Flask basierende Webanwendung, die entwickelt wurde, um Entra ID App Registration Secrets und SAML-Zertifikate von Enterprise Applications zu verwalten. Sie bietet eine benutzerfreundliche Oberfläche zur Überwachung und Verwaltung von den genannten Entra ID Ressourcen.

## Inhaltsverzeichnis

1. [Funktionen](#funktionen)
2. [Technologie-Stack](#technologie-stack)
3. [Projektstruktur](#projektstruktur)
4. [Installation](#installation)
5. [Konfiguration](#konfiguration)
6. [Anwendung starten](#anwendung-starten)
7. [Docker-Bereitstellung](#docker-bereitstellung)
8. [Docker Compose](#docker-compose)
9. [API-Dokumentation](#api-dokumentation)
10. [Authentifizierung](#authentifizierung)
11. [Datenbank](#datenbank)
12. [Geplante Aufgaben](#geplante-aufgaben)
13. [Frontend](#frontend)
14. [Demo](#demo)
15. [Mitwirken](#mitwirken)
16. [Support](#support)
17. [Entwickler](#entwickler)
18. [Credits](#credits)

## Funktionen

- Dashboard mit Schlüsselmetriken
- Kundenverwaltung
- Verwaltung von App-Registrierungen
- Verwaltung von Unternehmensanwendungen
- SAML-Zertifikatsüberwachung
- App-Registrierungen Secret Überwachung
- Benutzerauthentifizierung (lokal und Entra ID)
- RESTful API-Endpunkte

## Technologie-Stack

- Backend: Python 3.9, Flask 2.2.5
- Datenbank: SQLAlchemy mit Unterstützung für MySQL
- Frontend: HTML, CSS, JavaScript
- Authentifizierung: Flask-Login, Flask-Dance (für Entra ID-Integration)
- API: Flask-RESTX
- Aufgabenplanung: Schedule
- Bereitstellung: Docker, Gunicorn, Supervisor

Dieses Projekt basiert auf dem Open-Source-Template [Flask Datta Able](https://github.com/app-generator/flask-datta-able), das von AppSeed bereitgestellt wird. Es wurde angepasst und erweitert, um den spezifischen Anforderungen von Entrify gerecht zu werden.

## Projektstruktur

Die Anwendung folgt einer modularen Struktur:

```
entrify/
├── apps/
│   ├── authentication/
│   ├── home/
│   ├── services/
│   ├── static/
│   └── templates/
├── migrations/
├── nginx/
├── .env.sample
├── Dockerfile
├── requirements.txt
├── run.py
└── supervisord.conf
```

- `apps/`: Enthält den Hauptanwendungscode
- `migrations/`: Datenbankmigrationsscripte
- `nginx/`: Nginx-Konfiguration für die Bereitstellung
- `Dockerfile`: Docker-Konfiguration für die Containerisierung
- `run.py`: Einstiegspunkt für die Anwendung

## Installation

1. Klonen Sie das Repository
2. Erstellen Sie eine virtuelle Umgebung:
   ```
   python -m venv venv
   source venv/bin/activate  # Unter Windows verwenden Sie `venv\Scripts\activate`
   ```
3. Installieren Sie die Abhängigkeiten:
   ```
   pip install -r requirements.txt
   ```

## Konfiguration

1. Kopieren Sie `.env.sample` zu `.env`
2. Aktualisieren Sie die `.env`-Datei mit Ihrer spezifischen Konfiguration:
   - Setzen Sie `DEBUG` auf `False` in der Produktion
   - Konfigurieren Sie die Datenbank-Anmeldeinformationen
   - Richten Sie Entra ID-Anmeldeinformationen ein (ENTRA_ID, ENTRA_SECRET, AZURE_TENANT)

Hier sind die wichtigsten Umgebungsvariablen, die Sie konfigurieren sollten:

- `DEBUG`: Setzen Sie dies auf `False` in der Produktion
- `FLASK_APP`: Sollte auf `run.py` gesetzt sein
- `FLASK_DEBUG`: Setzen Sie dies auf `0` in der Produktion
- `ENCRYPTION_KEY`: Ein starker, einzigartiger Schlüssel für die Verschlüsselung
- `DB_ENGINE`: Die zu verwendende Datenbank-Engine (z.B. `mysql+pymysql`)
- `DB_HOST`: Die Adresse des Datenbankservers
- `DB_NAME`: Der Name der Datenbank
- `DB_USERNAME`: Der Benutzername für die Datenbankverbindung
- `DB_PASS`: Das Passwort für die Datenbankverbindung
- `DB_PORT`: Der Port für die Datenbankverbindung
- `ASSETS_ROOT`: Die Basis-URL für statische Assets
- `ENTRA_ID`: Die Anwendungs-ID (Client-ID) für Microsoft Entra ID
- `ENTRA_SECRET`: Das Client-Geheimnis für Microsoft Entra ID
- `AZURE_TENANT`: Die Tenant-ID für Azure
- `OAUTHLIB_INSECURE_TRANSPORT`: Sollte in der Produktion auf `0` gesetzt werden
- `PREFERRED_URL_SCHEME`: Sollte in der Produktion auf `https` gesetzt werden

## Anwendung starten

Um die Anwendung lokal zu starten:

```
flask run
```

Für die Produktion verwenden Sie Gunicorn:

```
gunicorn --config gunicorn-cfg.py run:app
```

## Docker-Bereitstellung

Die Anwendung kann mit Docker bereitgestellt werden:

1. Bauen Sie das Docker-Image:
   ```
   docker build -t entrify .
   ```
2. Führen Sie den Container aus:
   ```
   docker run -p 5000:5000 entrify
   ```

Das `Dockerfile` ist so konfiguriert, dass es Supervisor zur Verwaltung mehrerer Prozesse innerhalb des Containers verwendet.

## Docker Compose

Entrify kann auch mit Docker Compose bereitgestellt werden, was die Verwaltung mehrerer Container erleichtert. Hier ist eine kurze Anleitung:

1. Stellen Sie sicher, dass Docker und Docker Compose auf Ihrem System installiert sind.

2. Navigieren Sie zum Projektverzeichnis, das die `docker-compose.yml` Datei enthält.

3. Erstellen Sie eine `.env` Datei im selben Verzeichnis und füllen Sie sie mit den erforderlichen Umgebungsvariablen aus, einschliesslich der MySQL-Konfiguration.

4. Führen Sie den folgenden Befehl aus, um die Container zu starten:

   ```
   docker-compose up -d
   ```

   Dies startet drei Container:
   - `app`: Die Entrify-Anwendung
   - `nginx`: Ein Nginx-Reverse-Proxy
   - `mysql`: Eine MySQL-Datenbank

5. Die Anwendung ist nun über `http://localhost:5085` erreichbar.

6. Um die Container zu stoppen und zu entfernen, verwenden Sie:

   ```
   docker-compose down
   ```

Beachten Sie, dass die MySQL-Daten in einem benannten Volume `mysql_data` persistiert werden, um Datenverlust zwischen Container-Neustarts zu vermeiden.

Für die Produktion sollten Sie sicherstellen, dass alle sensiblen Informationen in der `.env` Datei sicher gespeichert und verwaltet werden.

## API-Dokumentation

Die API-Dokumentation ist im Swagger-Format verfügbar und unter https://api-docs.entrify.ch/ zu finden. Die `swagger.json`-Datei enthält Details zu verfügbaren Endpunkten und deren Verwendung.

Wichtige API-Endpunkte sind:
- `/api/add-customer`: Einen neuen Kunden hinzufügen
- `/api/customers`: Alle Kunden abrufen
- `/api/applications`: Alle Anwendungen und deren Secret Informationen abrufen
- `/api/enterprise-applications`: Alle Unternehmensanwendungen und deren SAML-Zertifikate abrufen

## Authentifizierung

Die Anwendung unterstützt zwei Authentifizierungsmethoden:
1. Lokale Authentifizierung mit Benutzername und Passwort
2. Entra ID-Authentifizierung mit OAuth 2.0

Die Authentifizierung wird im Modul `apps/authentication/` behandelt.

## Datenbank

Die Anwendung verwendet SQLAlchemy ORM und unterstützt mehrere Datenbank-Engines. Wichtige Modelle sind:
- `Customer`
- `Application`
- `PasswordCredential`
- `EnterpriseApplication`
- `SAMLCertificate`

Die Datenbankkonfiguration finden Sie in `apps/config.py`.

## Geplante Aufgaben

Die Anwendung enthält geplante Aufgaben zur Aktualisierung von Anwendungs- und Zertifikatsinformationen. Diese Aufgaben werden mit der `schedule`-Bibliothek verwaltet und sind im Verzeichnis `apps/services/` konfiguriert.

## Frontend

Das Frontend ist mit HTML-Templates unter Verwendung von Jinja2, CSS und JavaScript aufgebaut. Wichtige Seiten sind:
- Dashboard (`index.html`)
- Kundenliste (`customers.html`)
- App-Registrierungen (`app_registrations.html`)
- Unternehmensanwendungen (`enterprise_applications.html`)

Frontend-Assets befinden sich in `apps/static/` und Templates in `apps/templates/`.

## Demo

Eine Demo Version der Entrify Anwendung ist unter https://dashboard.entrify.ch verfügbar. Diese Demo Instanz ermöglicht es Ihnen, die Funktionen und das Benutzerinterface von Entrify zu erkunden, ohne eine eigene Installation vornehmen zu müssen.

## Mitwirken

Beiträge zu Entrify sind willkommen. Bitte folgen Sie diesen Schritten:
1. Forken Sie das Repository
2. Erstellen Sie einen neuen Branch für Ihr Feature
3. Committen Sie Ihre Änderungen
4. Pushen Sie zu Ihrem Fork
5. Reichen Sie einen Pull-Request ein

## Support

Für Support kontaktieren Sie bitte support@entrify.ch oder öffnen Sie ein Issue im GitHub-Repository des Projekts.

## Entwickler

- [Flavio Meyer](https://github.com/flaviomeyer)
- [Michele Blum](https://github.com/Quattro99)

## Credits

- [Flask Datta Able](https://github.com/app-generator/flask-datta-able)

Mit ❤️ und ☕ wurde die Webanwendung Entrify erstellt.
