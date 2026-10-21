# PROJECT_CONTRACT.md — IntheLoopRemoteLab Development Contract
Version: 1.1
Effective: 2026-10-21
Scope: IntheLoopRemoteLab and the explicitly linked DeltaESC, EBiCS and SmartESC development tracks.
Status: Baseline approved on 2026-10-20; DeltaESC clarification explicitly approved on 2026-10-21.

> **If it works, it works. No need to change a running system.**

## Verbindliche DeltaESC-Klarstellung vom 21.10.2026

Der Projektbesitzer hat die zuvor zu weit ausgelegte Zustimmungspflicht
korrigiert: Fuer den aktuellen DeltaESC-Auftrag gilt sie fuer den
**Rueckflashpfad**, der ohne ST-Link frei und erreichbar bleiben muss.
**Motorfreigabe ist erteilt.** Die fuer Fahrbetrieb notwendigen Motorstart-,
Regelungs-, Ausroll-/Wiederanlauf- und Schutzlogik-Aenderungen duerfen im
Auftrag eigenstaendig umgesetzt werden; keine erneuten Einzelgenehmigungen
an regulaeren Softwareteilschritten verlangen.

**Am aktuellen Zielcontroller gibt es keine ST-Link-Moeglichkeit.** Fruehere
ST-Link-Nachweise sind historisch und kein verfuegbarer Rueckweg. Keine
neuen CRC-, Flashgroessen-, Versions-, Kalibrierungs- oder Motorfehler-Gates
duerfen IAP/Rueckflash blockieren. Vor einer Flash-Empfehlung muss der
tatsaechliche Rueckweg am exakten Ziel bekannt und belegt sein. Ein
Handler innerhalb der austauschbaren App allein ist kein Nachweis fuer
Recovery bei einer gar nicht startenden App; keine solche Garantie erfinden.

Diese aktuelle, ausdrueckliche Freigabe uebersteuert fuer DeltaESC die
widersprechenden Motor-Freigabeannahmen in v1.0 und alten Uebergaben.
Elektrische Schutzfunktionen bleiben Entwicklungsgegenstand und werden
nicht pauschal entfernt. Keine nicht nachweisbar reversible Hardwareaktion,
kein neuer Bootloader und kein Versuch mit geratenem Flashlayout folgt
allein aus dieser Source-Freigabe. Andere Projektauftraege bleiben getrennt.

## 1. Ziel und Arbeitsmodus
Wir entwickeln für die jeweils **konkret bekannte, festgelegte Hardware**, nicht für hypothetische Drittgeräte. Ein Hinweis "tested only on the specified hardware revision; other hardware is not qualified" genügt für öffentliche Releases. Fehlende allgemeine Kompatibilität ist kein Grund für eine invasive Änderung.

Der Entwicklungsassistent soll in einem freigegebenen Arbeitspaket so viele sinnvolle Schritte wie möglich eigenständig erledigen: untersuchen -> Code schreiben -> bauen -> simulieren/testen -> Ergebnisse analysieren -> verbessern -> dokumentieren. Nach regulären Teilerfolgen (z. B. ADC-Offset-Test) braucht er kein weiteres "weiter". RemoteLab kann bereits vorbereitete, freigegebene Jobs abarbeiten; ein nicht aktiver Chat kann nicht eigenständig ständig neue Codeänderungen vornehmen.

## 2. Entscheidungsklassen
- **GEWÜNSCHT:** ausdrücklich beauftragt; innerhalb des beschriebenen Umfangs selbstständig implementieren, prüfen und dokumentieren.
- **SINNVOLL, ABER NICHT BEAUFTRAGT:** vor Umsetzung Vorschlag mit konkretem Nutzen, Nachteilen, Risiken, betroffenen Komponenten und Alternative "unverändert lassen"; Freigabe abwarten.
- **NICE TO HAVE / NOT NECESSARY:** nur als Vorschlag oder Backlog, niemals ungefragt einbauen.

Eine Freigabe für eine Aufgabe ist **keine** pauschale Zustimmung zu Architektur-, Bootloader-, Flash- oder Recovery-Änderungen.

## 3. Nicht verhandelbare Invarianten
1. **Funktionierende Systeme nicht ohne Anlass verändern.** Bekannte funktionierende Schnittstellen, Protokolle und Verhalten bleiben Referenz.
2. **Flash-, IAP-, Bootloader-, Start- und Recovery-Pfade bleiben unverändert**, sofern eine Änderung nicht explizit beauftragt und nach Abwägung freigegeben wurde. Insbesondere keine zusätzlichen Bootloader-CRC-, Flashgrößen-, Hardwareidentitäts- oder Versions-Gates auf Verdacht.
3. Bekannte Hardwareeigenschaften werden dokumentiert, **nicht** als Anlass zur Erfindung neuer Sperren benutzt.
4. Keine stillschweigende Änderung von Startbedingungen, GPIO-Belegung, Leistungsgrenzen, Motorfreigabe oder Safety-Mechanismen. Elektrische Schutzfunktionen (z. B. Überstrom, Deadtime, Abschaltung) nicht entfernen.
5. Ein neu erkannter realer Gefahren- oder Widerspruchsfall: **betroffene aktive Arbeit anhalten, Befund dokumentieren, Nutzer informieren** statt eigenmächtig neue Architektur einzubauen.
6. Keine Schreib-/Motoraktionen auf Hardware ohne vorher gemeinsam festgelegtes Testpaket und reale, verfügbare Schnittstelle. Ohne Controller: ausschließlich Source-Audit, Build, Host-Tests, Simulation und Dokumentation.
7. Kein Versuch, Zugang durch unbestätigte Flash-Geometrie, neue gesperrte Recovery-Pfade oder unbestätigte Mechanismen zu erzwingen. **Kein** generischer Kompatibilitäts-Overhead ohne Nutzen für die tatsächlich vorhandene Hardware.
8. Bestehende Release-Holds und bereits konfigurierte CI-Sperren werden bei der Bestandsaufnahme **nicht stillschweigend geändert, gelöscht oder umgangen**. Wenn sie fachlich unpassend erscheinen, als Entscheidungsbedarf mit Vor-/Nachteilen markieren.

## 4. Beweise statt Behauptungen
Jede Aussage kennzeichnen:
- **REAL GETESTET:** konkreter Hardwaretyp, Datum, Softwarestand, Messergebnis/Log und Testbedingungen.
- **SOFTWARE GETESTET:** Testsuite, Build-ID/Commit, Ergebnis; **kein** Nachweis eines Motorlaufs.
- **ENTWURF/UNVERIFIZIERT:** ausdrücklich als offen bezeichnen.

Donor-Hardware-Ergebnisse dürfen nicht als Tests des Zielcontrollers ausgegeben werden. Kein "ready", "flashbar", "recovered" oder Prozentwert ohne überprüfbare Grundlage. Ergebnisse müssen zum **exakten** Quellstand gehören.

## 5. GitHub und Projektgrenzen
- Gemeinsamer generischer Core: `ZachWay9bot/IntheLoopRemoteLab`.
- XBOT-/G30-identical-Laufzeitqueue: **eigenes PRIVATES** `ZachWay9bot/xbot-remote-lab` (NICHT als Queue des generischen Projekts wiederverwenden oder verändern).
- DeltaESC: `ZachWay9bot/DeltaESC-G30D`.
- SmartESC: `ZachWay9bot/SmartESC_STM32_v21b`.
- EBiCS: maßgeblichen Source-ZIP/Referenzstand je Übergabe dokumentieren; kein fremdes Repository oder andere Firmware als kanonisch behaupten.
- Keine ungefragten Moves, Umbenennungen, Rewrites, Force-Pushes oder Releases. Für neuen Code bevorzugt isolierte zusätzliche Tests/Adapter/Branches, ohne funktionierende Produktionspfade anzufassen.

## 6. Verbindliche Übergabe bei jedem Chatwechsel / Neustart
Zuerst diese Datei **aus GitHub neu lesen**; zusätzlich die aktuelle `PROJECT_HANDOFF.md` bzw. projektspezifische Standdatei. Eine alte Chat-Zusammenfassung allein ist keine maßgebliche Wahrheit.

Die Übergabe muss enthalten:
1. Auftrag, Scope und ausdrücklich freigegebene **sowie nicht freigegebene** Aktionen;
2. Link zum Entwicklungsvertrag und seine Version;
3. Zielhardware und tatsächliche physische Recovery-Möglichkeiten;
4. Name/Version jedes Projekts, Branch, **Commit-SHA**, Source-Archiv mit SHA-256 (sofern verfügbar);
5. verifizierte Referenzfunktionen; benannte unveränderliche Schnittstellen;
6. real bestätigte vs. reine Software-Ergebnisse mitsamt Belegen;
7. bekannte Fehler, abgelehnte Ideen und entscheidende technische Abwägungen **mit Begründung**;
8. zuletzt erledigter Schritt, nächsten 3-5 konkrete Schritte und Stop-Kriterien;
9. aktuellen RemoteLab-Agent-/Queue-Stand und Abhängigkeiten, ohne Geheimnisse/Tokens.

Vor Änderungen bei Unstimmigkeiten: **anhalten und Quellen abgleichen**. Kein Raten, kein stillschweigender Rückgriff auf ältere Firmware, keine neuen Architekturentscheidungen aufgrund einer unvollständigen Übergabe. Nach jedem abgeschlossenen Arbeitspaket die Übergabe aktualisieren.

## 7. Autonomie mit klaren Grenzen
Innerhalb des freigegebenen Pakets: selbstständig weiterarbeiten, bis Umfang fertig oder Stop-Kriterium erreicht. Nicht nach jedem bestandenen Test um Erlaubnis bitten. Schritte sauber loggen und nachvollziehbar versionieren.

Sofort anhalten bei: unbekannter Hardware-/Firmwarezuordnung, implizitem Flash-/Recovery-Umbau, akuter elektrischer Gefahr, widersprüchlicher Identität/Messung, überschrittenem Auftragsumfang, verlangter physischer Handlung durch den Nutzer.

## 8. Änderungen am Vertrag
Nur auf ausdrücklichen Wunsch des Projektbesitzers und mit dokumentierter Begründung. Änderungen werden versioniert. Eine Chat-Übergabe oder ein autonomer Agent darf Regeln **nicht** stillschweigend überschreiben.

**Kernregel: Maximale Selbstständigkeit innerhalb des Auftrags. Grundlegende Entscheidungen gemeinsam.**
