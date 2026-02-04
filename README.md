# MesseCall – Planner für Messdiener

## Zielbild
MesseCall ist ein Planungs- und Community-Tool für Messdiener*innen und Verwaltung in Pfarreien. Kirchen registrieren sich, pflegen ihre Gottesdienst-Events, stellen diese optional öffentlich bereit (Webseite/Feed), und koordinieren intern Einsatzpläne. Messdiener*innen geben Präferenzen an, können sich freiwillig melden, Tauschanfragen stellen und Ersatzdienste übernehmen. Ein Matching-Algorithmus erstellt Vorschläge, die Verwaltung final freigibt. Danach werden Benachrichtigungen verschickt und das Dashboard aktualisiert.

## Kernrollen
- **Kirchenverwaltung (Admin/Leitung):** Stammdaten, Events, Regeln, Freigaben, Kommunikation.
- **Messdiener*innen:** Präferenzen, Verfügbarkeiten, Zusagen, Tausch/Ersatz.
- **Gemeinde/Öffentlichkeit:** Sichtbare Terminlisten (optional, lesend).

## Hauptmodule

### 1) Kirchen-Registrierung & Mandantenfähigkeit
- Mehrere Kirchen/Pfarreien als getrennte Mandanten.
- Kirchenprofil mit Gottesdienstorten, Kontakt, Standard-Regeln.
- Rollenverwaltung: Admin, Koordinator*in, Messdiener*in.

### 2) Event-Management & Öffentliches Kalender-Listing
- Eventtypen (z. B. Sonntagsmesse, Feiertag, Hochzeit, Probe).
- Felder: Datum/Zeit, Ort, Bedarf (Anzahl Messdiener*innen), Anforderungen (z. B. „erfahren“).
- Öffentliches Event-Listing (Webseite/Embed) und Export:
  - iCal/ICS Feed
  - JSON Feed für Website-Integration
  - Optional: API-Token pro Kirche

### 3) Präferenzen & Verfügbarkeiten
- Messdiener*innen legen bevorzugte Uhrzeiten, Wochentage, Orte fest.
- Verfügbarkeitsfenster (mit Sperrzeiten wie Ferien, Prüfungen).
- Wunschpartner*innen: „Bitte mit Person X/Y zusammen dienen“.
- „Lieblingsmessen“ als freiwillige Priorisierung.

### 4) Matching-Algorithmus & Freigabe-Workflow
- Algorithmus erstellt Vorschläge auf Basis:
  - Verfügbarkeit
  - Präferenzen
  - Fairness (gleichmäßige Verteilung)
  - Kompetenzlevel (Anfänger/Erfahren)
  - Wunschpartner*innen
  - Freiwillige Zusagen
- Ergebnis = Vorschlagsplan, der von der Verwaltung freigegeben wird.
- Freigabe erzeugt verbindliche Einsätze.

### 5) Benachrichtigungen & Dashboards
- E-Mail, Push (optional), In-App Benachrichtigungen.
- Messdiener*innen-Dashboard: persönliche Termine, Zusagen, offene Anfragen.
- Verwaltung-Dashboard: Planstatus, Konflikte, Abwesenheiten, Ersatzbedarf.

### 6) Ersatz- & Tauschsysteem (kreativ & flexibel)
- **Direkter Tausch:** Messdiener*in bietet Tausch an, andere bestätigt.
- **Ersatzbörse:** Offene Schicht kann von Pool übernommen werden.
- **Ersatzpool:** Freiwillige melden „Ersatzbereit“ für bestimmte Zeitfenster.
- **Auto-Match für Ersatz:** System schlägt Ersatz basierend auf Präferenzen vor.
- **Notfallmodus:** Wenn kurz vor Start unbesetzt, geht Broadcast an Ersatzpool.

### 7) Gamification & Community
- **Punkte & Level:** Für Zuverlässigkeit, Einsätze, Ersatzübernahmen.
- **Badges:** „Frühaufsteher“, „Feiertagsheld“, „Teamplayer“.
- **Community-Challenges:** „Als Gruppe 20 Einsätze in der Adventszeit“.
- **Mentor-Feature:** Erfahrene begleiten Neueinsteiger.
- **Team-Spotlight:** Wöchentliche Highlights im Dashboard.

## Datenmodell (Vorschlag)
- **Church**: id, name, adresse, zeitzone, settings
- **User**: id, name, email, role, church_id
- **Event**: id, church_id, type, start_time, end_time, location, required_slots
- **Assignment**: id, event_id, user_id, status (proposed/approved/swapped)
- **Preference**: user_id, weekdays, time_ranges, locations, partner_user_ids
- **Availability**: user_id, date_range, status (available/unavailable)
- **SwapRequest**: assignment_id, status, requested_user_ids
- **BackupPool**: user_id, time_ranges, active
- **Gamification**: user_id, points, badges

## Typische Workflows

### A) Neue Messe planen
1. Verwaltung legt Event an.
2. Algorithmus erstellt Vorschlagsplan.
3. Verwaltung prüft/editiert und gibt frei.
4. Benachrichtigungen werden versendet.

### B) Messdiener*in möchte tauschen
1. Messdiener*in initiiert Tausch.
2. System informiert potenzielle Ersatzpersonen.
3. Ersatz bestätigt; Verwaltung kann optional freigeben.

### C) Ersatzpool greift ein
1. Offene Schicht wird erkannt.
2. System schlägt Ersatz vor.
3. Bei Annahme: Assignment wird aktualisiert.

## Erweiterungen & Schnittstellen
- API für Kirchenwebseiten: Events abrufen (öffentlich oder mit Token).
- Export nach Google Calendar (per iCal).
- Statistik & Reporting: Fairness, Abwesenheiten, Belastung.
- Datenschutz: Rollenbasierter Zugriff, öffentliche Events ohne personenbezogene Daten.

## Erfolgskriterien
- 80–90 % automatisch zugewiesene Messen.
- Hohe Zufriedenheit durch Präferenzen & Fairness.
- Schnelle Ersatzfindung unter 24 Stunden.
- Messdiener*innen aktivieren sich durch Gamification & Community.

## Lokale Entwicklung (API)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Beispiel-Flow
1. Kirche anlegen: `POST /churches`
2. Nutzer*innen anlegen: `POST /users`
3. Events anlegen: `POST /events`
4. Verfügbarkeiten & Präferenzen: `POST /availability`, `POST /preferences`
5. Freiwillige Zusagen: `POST /volunteer-interests`
6. Vorschlag generieren: `POST /events/{event_id}/suggestions`
7. Vorschlag übernehmen: `POST /events/{event_id}/proposals`
8. Freigabe: `POST /assignments/{assignment_id}/approve`
9. Ersatzsystem: `POST /swap-requests` + `POST /swap-requests/{id}/accept`

### Öffentliche Termine
- JSON: `GET /public/churches/{church_id}/events`
- ICS: `GET /public/churches/{church_id}/events.ics`
