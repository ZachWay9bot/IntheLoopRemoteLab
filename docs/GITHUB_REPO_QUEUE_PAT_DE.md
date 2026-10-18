# GitHub: Projekt-Repo, Job-Queue und Fine-grained PAT

GitHub macht aus einer simplen Berechtigung gern eine kleine Verwaltungswissenschaft. Deshalb hier die klare Trennung.

## A. Projekt-Repository

`ZachWay9bot/RemoteLab` enthaelt:

- Source
- Dokumentation
- Tests
- Releases

Dieses Repository ist **nicht** die XBOT-Job-Queue.

Zum normalen Entwickeln ueber GitHub/ChatGPT ist kein lokaler Runtime-PAT fuer RemoteLab notwendig, solange der GitHub-Connector verwendet wird.

## B. Bestehende XBOT-Queue

Die bestehende XBOT-Queue bleibt unveraendert.

- keine Umbenennung
- kein Wechsel des Issue-Protokolls
- kein neuer Token nur wegen RemoteLab v0.4
- kein Umschalten des produktiven Agenten

## C. Neue Queue fuer ein spaeteres Projekt

Erst wenn ein neues Hardwareprojekt eine eigene Remote-Queue braucht:

1. separates **privates** Repository erstellen, z. B. `MyDevice-RemoteQueue`
2. ein offenes Issue als Queue anlegen
3. Fine-grained PAT erstellen
4. bei **Repository access** nur dieses Queue-Repo auswaehlen
5. Repository Permissions:
   - **Contents: Read-only**, falls Artefakte aus dem Repo geladen werden
   - **Issues: Read and write**, fuer Jobs und Ergebnisse
   - **Metadata: Read** wird von GitHub automatisch benoetigt
6. keine Administration-, Workflow- oder Actions-Rechte geben

Der Runtime-Agent soll so wenig Rechte wie moeglich besitzen.

## D. Warum Projekt-Repo und Queue getrennt bleiben

Ein kompromittierter Runtime-Agent soll nicht automatisch Schreibrechte auf den Sourcecode haben. Die Queue ist Transport, das Projekt-Repo ist Entwicklungsstand.

Das ist auch der Grund, warum das bestehende XBOT-System nicht in das neue RemoteLab-Repo verschoben wird.
