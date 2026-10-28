# TDS 210/220 RemoteLab Adapter (28.10.2026)

- **Beauftragt:** Tektronix TDS 210 + TDS 220 als getrennt konfigurierbare RS-232-Adapter fuer IntheLoopRemoteLab integrieren.
- **Branch:** `feature/tektronix-tds210-tds220-adapter`, Basis main `3c203b6b37f3660fd624cf8d2026c895d8fbdcda`.
- **Hardware-Fakten:** TDS220 identifizierte sich vor diesem Paket ueber COM11 mit 9600 Baud, 8N1 und Flow Control NONE. TDS210-Port noch unbekannt.
- **Software:** `TektronixTDS200Adapter` hat identify/diagnose/measure/capture_waveform; Core erlaubt nur die zwei neuen benannten Leseoperationen zusaetzlich; bestehende ESC-/Flashadapter und IAP unberuehrt. Optional pyserial.
- **Tests:** 8 neue Fake-Serial-Unit-Tests, ohne echte Oszi-Hardware. Kein echter Wellenform-/Messwerttest mit der neuen Version erfolgt; CI-Ergebnis im Pull Request.
- **Offen:** Echter COM11-Test, TDS210-Port bestimmen und pruefen, TDS210-Kommunikation, Wellenformskalierung, Datenuebertragungsdauer.
- **Dokumentation:** `docs/adapters/tds200.md`, `examples/remotelab.tds200.queue.example.json`, `tools/tds200_probe.py`. Queue weiterhin nur privat.
- **Naechste Schritte:** PR-CI, lokal `py -m tools.tds200_probe --port COM11 --action identify`, danach diagnose/measure/capture_waveform; erst dann TDS210 aktivieren.

---

# PROJECT_HANDOFF.md — verbindliche Schichtuebergabe

## NEUESTE EBiCS-ÜBERGABE: Drive Step 3 StockDash AutoDrive (23.10.2026)

**Dieser softwareseitig umgesetzte Stand ersetzt ältere Aussagen, nach denen EBiCS für normalen Fahrbetrieb zwingend Android/BLE/0xBA=5 benötigt.** Die unmittelbar folgende Nutzeranforderung „Android nur VESC-Tool-artige Konfiguration“ gilt weiter: Batterie- und Motorstromlimits sowie persistente/lesbare Parameter sind NICHT schon erledigt.

- **EBiCS ist NICHT hardwareseitig fahr- oder flashfreigegeben.** Neue **vollständige SOURCE + TESTS-ZIP** liegt im Chat: `EBiCS_r9_StockDash_AutoDrive_Step3_SOURCE_TESTS_20261023.zip`, 2.786.686 Bytes, SHA256 `ce6ff2b5cc94918788280689cfc994a70f8607592a1d34e499b9d3c65c3c133c` (254 ZIP-Dateien). Vollständige editierbare EBiCS r9 Governor 18.10. + Drive Step2-Basis, neuer Step3-Quellpatch, Native-/Cortex-M3-/Android-/BLE-Tests, Kalibrierungswerkzeug und genaue deutsche Abnahme. Sourcecode wurde **nicht in ein eigenes EBiCS-GitHub-Repository** hochgeladen, sondern der Arbeitsstand [im Task dokumentiert](https://github.com/ZachWay9bot/IntheLoopRemoteLab/issues/1#issuecomment-6373258179).
- `Firmware/src/g30_autodrive.c`: autonome Drive-Qualifikation nach Power-on ausschließlich aus dem originalen Stock-Dash: gültige UID-gebundene Werkskalibrierung aus im Image enthaltenen **echten** Zielmessungen, Bremse frei, Gas neutral, mindestens 500 ms Stillstand, frisches Dashboard/ADC, einmaliger Gate-off-DWT-Selbsttest. Erst danach wird die vorhandene sensorlose Rollstart-/FOC-Fahrt ohne BLE-/App-/RPC-Kontakt freigegeben. Das elektrische Minimum entspricht aus 15 Nutzer-genannten G30-Gen1-Polpaaren und **gemessenem** Radumfang etwa 3 km/h mit 1 % Sicherheitsreserve. Kein Gas-Selbststart im Stand.
- Motorservice separat durch `G30_MOTOR_INTERNAL_AUTO_ARM=4`, nur einmal/Power-on nach Factory-Profil, niemals als UART-Servicekommando. Service-5s-Bench unverändert, appgesteuerte Drive-Servicefunktion weiterhin optional. Dashboard-250-ms-/ADC-5-ms- und Fault-/IAP-/Update-Stop bleiben. Kein automatischer Neustart nach Stop/Fault/Dash-Verlust. Fremder Diagnose/Detect-Owner erzwingt Disarm und Lockout. `main.c` ergänzt Auto-Poll und read-only Register `0xF4` Autozustand/`0xF5` Sperrgrund.
- **ABSOLUTE SAFETY GATE:** `Firmware/include/g30_autodrive_profile.h` ist im ausgelieferten Kandidaten `G30_AUTODRIVE_PROFILE_PRESENT 0`, denn es fehlen die belegten G30-Daten. **Der mitgelieferte Default-Cortex-M3-Build aktiviert den Motor niemals selbst.** `make_autodrive_profile.py` plus **leere** JSON-Messdaten-Vorlage fordert UID, R/L/Flux, Strom-/Spannungs-/ADC-/Deadtime- und Geometriewerte inkl. Messbeleg. Keine Fantasiekonstanten. Es führt keine Flashoperation aus und kann Instrumentenbelege nur formal, nicht physikalisch, überprüfen.
- `RUN_DRIVE_STEP3_ALL.sh`: komplette Step2-Regressions-/Cortex-M3-ELF/BIN-/SHU-Paket-Prüfung PASS, neue echte C-Service-/Auto-Zustands-Hosttests in 4 Profilkonfigurationen PASS, 120 s synthetische Fahrt ohne BLE/RPC, Timeout-/Benchmark-/UID-/Geometrie-/STOP-/Detect-Lockout-Fälle PASS. Aktive generierte Profilvariante als ARM-Objekt testkompiliert. **Keine reale Hardware-/ISR-/Motorqualifikation.** Default-BIN 41.820 Bytes SHA256 `dcba2412c3295a510b05b35e6dc2ecb44a8465a090bd2d9a9e5ac23e6dfb0fe3`, unter historischem Output-Dateinamen `FO76_GOVERNOR`, **UNQUALIFIED / NICHT FLASHEN**. Altes reales FO76-Image damit NICHT gleichsetzen.
- IAP-/Update-/UART-Protokoll-/STM32-Backend-/Startup-/Linkerdateien und Android BLE/Crypto **bytegleich zur originalen 18.10.-Quelle**; DeltaEsc-Freeze unangetastet. ST-Link physisch ausgeschlossen, FO91-Rückflashregression muss vermieden werden.
- **Noch offen:** Quelle `G30_EBiCS_r9_RECOVERY_INVARIANT_SOURCE_20261020.zip` (Originalbytes weiterhin nicht verfügbar) gegen diesen neuen Step3-Stand diffen; originale G30-Motor-/UID-/Strom- und Geometriedaten messen; echter Rückflashpfad; Stock-Dash-km/h/ACK/Heartbeat und BMS physisch abnehmen. Batteriestromlimit unabhängig vom Phasen-/Motorstrom sowie VESC-Tool-artiger Android-Konfigurator sind noch NICHT implementiert. Kein reales Flashen, keine eigentliche Motorradfahrt.


## AKTUELL: EBiCS Android nur Konfiguration, Stock-Dash faehrt (23.10.2026)

**Neue ausdrueckliche Nutzeranforderung und Korrektur des bisherigen Drive-Step2-Workflows. Hat Vorrang vor allen aelteren Beschreibungen einer benoetigten Android-/BLE-Fahrfreigabe.**

- Android-App soll ein **VESC-Tool-artiger Konfigurator** werden: Battery Amps, Phase/Motor Amps, Motor R/L/Flux und weitere FOC-Koeffizienten, Batteriespannung/Unter-/Ueberspannung, Rampen, Motor-Detect, Diagnosen und Readback. Batterie-Ampere und Motor/Phasen-Ampere sind **verschiedene physikalische Limits**; nicht gleichsetzen.
- **Der normale Fahrbetrieb wird ohne Android-App, Handy oder BLE ueber das originale Ninebot-Dashboard gesteuert.** Gas, Bremse, Coast, neuer Rollstart bei ca. 3 km/h und Timeout-/Faultschutz gehoeren in die ESC-Firmware. Kein App-Knopf oder `0xBA=5` pro Fahrt.
- **Ist-Stand im Source wirklich geprueft:** r9-Step2-App kann ABI1-JSON-Motorprofil mit 18 Float-Parametern importieren und per One-Shot-RPC 112 Bytes mit UID+CRC ins ESC-**RAM** senden. `g30_motor_service_profile()` hat `max_iq` 0.1–3.0 A, separaten `trip_current` 0.5–12 A, `bus_min` 25–40 V, `bus_max` 26–43 V und weitere Profil-/Messqualifikationen. Keine separate Battery-Current-Max-Begrenzung, kein echtes persistentes ESC-Profil, kein vollwertiger UI-Konfigurationseditor. Diese fehlenden Funktionen **nicht** als bereits vorhanden darstellen.
- Parametereinstellungen duerfen die Hardware-/Stromschutzgrenzen nicht ungeprueft ausweiten; Aenderung nur bei sicher ausgeschaltetem Leistungszweig und bestaetigtem Readback. Eine persistente Flash-Ablage **nicht** vor belastbarem Loader-/Staging-/Rueckflash-Nachweis einfuehren. Bestehendes IAP/UART/Boot/Recovery unangetastet. ST-Link am Ziel nicht moeglich. App-lokale Profilspeicherung und manuelles Laden nach Reset sind moegliche Zwischenstufe, aber nicht gleichbedeutend mit autonomem Normalfahren.
- Der bisherige Drive-Step2-Android-`armDrive` ist ein **expliziter Bench-Servicepfad, nicht Produkt-UX**. Fuer Serien-/Normalfahrt sicheren dashboardautonomen Arm-/Drive-State separat in EBiCS entwickeln und echt testen. Kein unbeabsichtigter Selbststart.
- Vollstaendiger verbindlicher [Auftrag/Status](https://github.com/ZachWay9bot/IntheLoopRemoteLab/issues/1#issuecomment-6371953301). Zuerst neueren 20.10.-r9-Quellstand byteweise mit isoliertem 18.10.-Step2-Code abgleichen, dann Umsetzung in einer eigenen EBiCS-Quelle.
- **`DeltaEsc 0.10.3 Drive Ready` bleibt FROZEN.** Diese Dokumentationskorrektur ist **keine** EBiCS-Quellimplementierung oder Hardwarefreigabe.


## AKTUELLER EBiCS-ARBEITSSTAND — DRIVE STEP 2 (23.10.2026)

**Dies ist die aktuelle EBiCS-Softwareübergabe; ältere Aussagen unten zu r8 als einziger erreichbarer Quelle, r9 stets SOURCE BLOCKED oder nur geplantem DRIVE ARM sind historisch und nicht der neue Arbeitsstand.**

- Basis ist das wirklich materialisierte Original `G30_EBiCS_r9_FO76_GOVERNOR_BUILT_SOURCE_20261018.zip` (SHA256 `7c4125fdfcd2744da25fa69ab0f1861ea0a65eb429e671754fb41e536fecf4e9`) mit dem zuvor erfolgreich getesteten r9 **DRIVE STEP 1** (Quell-ZIP SHA256 `b450c46775885356bd49188b03967374a85fbd6f75ccb08791b79c11a7b52d62`).
- NEU erstellt: `EBiCS_r9_Drive_Step2_FULL_SOURCE_TESTS_20261023.zip` (im Chat bereitgestellt, **nicht in GitHub als Firmwarequelle eingecheckt**), 2.746.350 Bytes, SHA256 `2addf3f1c6e1fe3fef7ed91e1c6fbb4bd796c0df2ffc4cd0168bf7010fb50724`. Vollständige Firmware-/Android-Quellen, Patches, Native/ARM-/App-/BLE-Tests, Logs, deutsche Abnahme, Baselinevergleich.
- Firmware-DRIVE hat den separaten bestehenden Modus `0xBA=5` nur nach `0xBC`-One-Shot-Ticket; App erkennt Motorservice-State 4, kann ihn nun durch explizite Bestätigung nach UID-CRC-/Benchmark-/Neutral-/Brake-/Stillstandqualifikation per vorhandener Registerbrücke starten und STOP ausführen. Kein Auto-Arm, kein erneuter Start bei fehlendem ACK.
- Neu im echten `Firmware/src/main.c`: Stock-Dashboard-Gas, Bremse und Zeitstempel werden PRIMASK-atomar verarbeitet; bei Brake/Neutral werden Gates auf Coast gesetzt, bevor ADC-IRQ-Wiederfreigabe erfolgt. Keine Änderungen an IAP, UART-Protokoll, Linker, STM32-Hardwarebackend, TIM1-PWM-Implementierung oder Android BLE/Crypto/Manifest.
- `RUN_DRIVE_STEP2_ALL.sh` PASS: Original native Motorservice-/Governor-/2/4-kHz-FOC-/Brake-/Rearm-/Timeouttests, produktiver `rpc_write` One-Shot-RPC-Test, echter Dashboard-`0x61/0x64/0x65`-/BMS-Parserhosttest inkl. SOC und 2-s-Frische, Android Crypto/BLE-JVM-Mocks, 81 neue DRIVE-App-Assertions und 15 UI-/Permissions-Assertions, kompletter ARM Cortex-M3 ELF/BIN Link und SHU-v3-Formatpakettest. Full-Source-Safety-Diff PASS.
- Neue **UNQUALIFIED** BIN: 41.660 Bytes SHA256 `6fee4edfd402c9c6b712ea60d1e0cf50da90aa57631b6a3811342e47439acb4c`. Original-Buildskript nennt das neue Image historisch weiterhin `FO76_GOVERNOR`; niemals als das alte reale FO76-Original bezeichnen und **NICHT FLASHEN**.
- **Weiter OFFEN**: (1) Rohbytes und exakter Diff zu `G30_EBiCS_r9_RECOVERY_INVARIANT_SOURCE_20261020.zip`, (2) echter G30-Motor und IAP-Rueckflash ohne physisch nicht moeglichen ST-Link, (3) Strom-/ADC-/Deadtime-/Phasen-/15-Polpaar-Geometriepruefung, (4) native km/h-Dash-Ausgabe und realer BMS-/Dashboard-/ACK-/Heartbeat-Test, (5) Android-APK mit SDK Build-Tools real bauen und telefonisch testen. Kein Hardware-/Realfahrbetrieb nachgewiesen. Bitte diese Punkte nicht als abgeschlossen behandeln.
- Detaillierter, überprüfter [EBiCS GitHub Task-/Abnahmebericht](https://github.com/ZachWay9bot/IntheLoopRemoteLab/issues/1#issuecomment-6354422125). **Nur** der Bericht liegt auf GitHub; fuer den kompletten Firmware-Source-Push fehlt weiterhin ein eigenes EBiCS-Repository. Nicht auf das DeltaESC- oder SmartESC-Firmware-Repo ausweichen.
- `DeltaEsc 0.10.3 Drive Ready` bleibt **FROZEN**; SmartESC unberührt.


## NEUE VERBINDLICHE ARBEITSANWEISUNG: DeltaEsc 0.10.3 Drive Ready FROZEN (21.10.2026)

**Diese Anweisung hat fuer die weitere Firmwarearbeit Vorrang vor allen aelteren Passagen in diesem Dokument, die noch aktive DeltaESC-Entwicklung, drei parallele Firmwareprojekte oder neue Simulationen vorsehen.**

- **DELTAESC IST JETZT EINGEFROREN.** Benutzerdefinierter Freeze-Name: **`DeltaEsc 0.10.3 Drive Ready`**. Quelle: [Freeze-Branch](https://github.com/ZachWay9bot/DeltaESC-G30D/tree/freeze/deltaesc-0.10.3-drive-ready), [detailliertes Freeze-Protokoll](https://github.com/ZachWay9bot/DeltaESC-G30D/blob/freeze/deltaesc-0.10.3-drive-ready/docs/DELTAESC_0_10_3_DRIVE_READY_FREEZE.md). Exakter erfolgreich softwaregetesteter **Firmware-Source-Commit** `26629227ad7cc882fb3f68426153c83767ce5e3e`; Freeze-Branch aus Dokumentationsstand `3f74686b9fbf9455bdea25ab2ca2eed7a1bd65bb`, Freeze-Protokoll commit `5947dde8f2eb3db35834fbd28c2dadb1823f0761`. PR [#21](https://github.com/ZachWay9bot/DeltaESC-G30D/pull/21) ist Draft/FROZEN, **nicht mergen**.
- **DeltaESC nicht weiter entwickeln, refaktorieren, optimieren, synchronisieren, flashen, mergen oder fuer neue Experimente verwenden, bis der Nutzer es ausdruecklich wieder freigibt.** Keine neuen DeltaESC-Source-PRs, keine weiteren DeltaESC-Test-Jobs auf Verdacht. Auf das historische FO7x-IAP-/Rueckflashproblem keine neue Sperrlogik bauen. ST-Link ist physisch unmoeglich.
- **`Drive Ready` ist ein Name fuer einen getesteten SOFTWARE-FREEZE, KEINE reale G30-Fahr-/Flash-/Rueckflashfreigabe.** Gruene exakte CI vom Motor-Source-Commit: [Motor/ARM 39629916521](https://github.com/ZachWay9bot/DeltaESC-G30D/actions/runs/39629916521), [Quell-Audit 39629916571](https://github.com/ZachWay9bot/DeltaESC-G30D/actions/runs/39629916571), [UART/IAP-Audit 39629916747](https://github.com/ZachWay9bot/DeltaESC-G30D/actions/runs/39629916747).
- **Ab sofort nur noch die beiden verbleibenden Firmwareprojekte EBiCS und SmartESC bearbeiten.** Einziger aktiver gemeinsamer Entwicklungs-Task: [IntheLoopRemoteLab Issue #1: EBiCS + SmartESC fertigstellen](https://github.com/ZachWay9bot/IntheLoopRemoteLab/issues/1). Dieser Task legt Scope, Erfolgsbedingungen und Nicht-Verhandelbares fest. Dort weiterarbeiten, nicht erneut bei DeltaESC beginnen.
- Originale Flash-/IAP-/Recoverypfade von EBiCS und SmartESC bleiben ebenfalls unangetastet; keine Umgehung des Release-HOLD ohne Nutzerentscheidung. Ausschliesslich Software/Quelltests bis separate reale Hardwarefreigabe. Keine neue Virtual-Controller-Simulation als Ziel.

Stand: 2026-10-20
Contract: [PROJECT_CONTRACT.md](PROJECT_CONTRACT.md), Version 1.0

## KORREKTUR — reale FO76-Historie und IAP-only-Ziel (21.10.2026)

Der kommende Controller ist noch nicht eingetroffen; DRV 1.8.7 ist der
erwartete Lieferstand, DRV126 die geplante Basis. Bis auf Weiteres per IAP
flashen. **ST-Link ist physisch ausgeschlossen**, keine entsprechende
Alternative anbieten oder erneut erfragen. Motorentwicklung ist freigegeben.

Die private archivierte Issue-Historie wurde diesmal direkt gelesen
(keine neuen Jobs gesendet):
- FO76-Flash `fo76-repo-flash`: erfolgreich und verifiziert.
- `fo76-24v-wizard-once`: `success=true`, `DONE/PLATEAU`,
  Takeover `SUCCESS`, 40.000/40.000 ACTIVE-Ticks, max. 76 Strom-Counts,
  ausgewaehlter Observer 0 Clamps.
- FO76 -> FO78: erfolgreicher IAP-Weiterflash.
- FO80 -> `XBOTFO91V00911`: erfolgreich installiert; anschliessender
  Rueckflash zu FO80 scheiterte mit `IAP status 7`. Der dokumentierte
  FO91-Fingerprint-/128-KiB-Vorbehalt war eine Rueckflashregression.
- Die real geflashte FO76-Datei (21.712 Bytes, SHA256
  `35ceae5c635c66f667380fc8dd0777463aed5dde98014328d123be5965812554`)
  ist **nicht** bytegleich zur unten dokumentierten Source-Reproduktion
  (21.728 Bytes, `a8b7ca7d45fdfa32cbcbfdfbe98e2e655a266ecc57aea62f8149ecf3cbe74bcb`).
  Die gemeinsame Kennung `XBOTFO76V00761` ersetzt keinen Hashabgleich.
  Beide Belege erhalten; den Unterschied noch vergleichen.
- [Originalbelege und genaue Zuordnung](https://github.com/ZachWay9bot/DeltaESC-G30D/blob/dev/drive-reversible-20261021/docs/HARDWARE_HISTORY_FO76_FO91_20261021.md).

"Kein Hardwaretest" in den folgenden v0.10.3-Abschnitten gilt nur fuer den
neuen Kandidaten. Die frueheren realen Flash-/Motorerfolge sind bestaetigt
und duerfen nicht erneut als fehlend behandelt werden. Das ist keine
nachtraegliche Hardwarequalifikation des neuen Kandidaten.

## AKTUELL — DeltaESC-Motorfreigabe und Rueckflashprioritaet (21.10.2026)

Dieser Abschnitt uebersteuert die aelteren DeltaESC-Freigabe-/ST-Link-Angaben
unten. Vertrag aktuell v1.1: Der Besitzer hat Motorfreigabe und die fuer
Fahrbetrieb notwendigen Aenderungen ausdruecklich erteilt. Keine erneuten
Einzelgenehmigungen fuer Motorentwicklung verlangen. Prioritaet hat die
Rueckkehr ohne ST-Link; **ST-Link ist am Ziel nicht verfuegbar**.

- Konkrete Softwarekorrekturen liegen in [DeltaESC PR #21](https://github.com/ZachWay9bot/DeltaESC-G30D/pull/21),
  Branch `dev/drive-reversible-20261021`, Source-Commit `cc7df57d10da9d16c1e8387cd8622bf327e364bd`.
- Komplette editierbare Quelle `firmware/`, v0.10.3 `FW_BUILD=0x1030`.
  RC-Startmasken und Runtime-Eigentuemerpruefung konsistent; proportionale
  Gasvorgabe, normale Coast/Wiederanlauf-Funktion und Brake-Priority.
  E6/Fault bleiben terminal; keine neuen IAP-Sperren.
- Native 35 Komponenten-/Integrationsgruppen bestanden. Die echte
  `main.c` wird mit Register-Speicher und inerten ARM-Barrieren geprueft;
  kein Motor-/ADC-/Flash-Modell, kein Hardwaretest. Der unveraenderte
  IAP-Parser akzeptiert BEGIN nach E6, Motorfehlern und IAP-Order-Fehler;
  pending IAP verhindert einen Motorstart.
- Alle IAP-, UART-, CPU-Header- und Linkerdateien sind bytegleich zur
  oeffentlichen v0.10.2-Referenz. ARM-/CI-Status am exakten genannten Commit
  lesen; der erste Dreifach-Build fand einen ID-only-unused-function-Fehler,
  der durch passend bedingtes Kompilieren der Closed-Loop-Helfer korrigiert
  wurde. Kein frueheres CI-PASS auf den neuen Stand uebertragen.
- Der Fahrkandidat startet ohne Donor-R/L/Flux/Geometrie; F0-F5 bleibt
  transaktional/RAM, FF ergaenzt gemessene Geometrie und Readback, der alte
  F6-ADC-Read bleibt. Phase-Offset gilt fuer Observer UND passiven Seed.
- Offen: tatsaechlicher Rueckflash am aktuellen Ziel ohne ST-Link,
  G30-Messdaten, Leistungs-/Bremsvalidierung, BMS/SOC. Aktuelle Bremse
  coasts; Batterieanzeige ist weiterhin Platzhalter. Keine Fahrfertigkeit
  behaupten und keine neuen Images als flashfreigegeben ausgeben.
- Kein Controller geflasht, kein Motor aktiviert und keine private Queue
  geaendert. Weitere Details/aktuelle Uebergabe:
  [DeltaESC PROJECT_HANDOFF](https://github.com/ZachWay9bot/DeltaESC-G30D/blob/dev/drive-reversible-20261021/docs/PROJECT_HANDOFF.md).

### DeltaESC: abgeschlossene Softwarepruefung

- [CI 39573629137](https://github.com/ZachWay9bot/DeltaESC-G30D/actions/runs/39573629137)
  **PASS** am Source-Commit `cc7df57d10da9d16c1e8387cd8622bf327e364bd`:
  35 Komponenten-/Integrationsgruppen, Safe/ID-only/Drive-ARM-Builds,
  separater ARM-Profil-Fixture-Build, IAP-Symbole gelinkt und bestehender
  Anti-Lockout-Check bestanden. Kein Hardwaretest.
- Kandidat 32.748 Bytes, SHA256
  `707c17285e65bfb94074414a97f11f71dd57e401930e2aaa28532b3aadddd950`.
  Keine Flash-/Fahrfreigabe aus diesem Softwareergebnis ableiten.
- `g30_target_profile.h` bereitet Standalone-Start mit gemessenen
  Konstanten vor, ohne neue persistente Flashseiten. Unbekannte G30-Felder
  sind Null. Positive Profilwerte wurden explizit als Test-Fixture in
  separaten Host-/ARM-Laeufen verwendet, nicht in den Kandidaten uebernommen.
- DRV126-Originaldump erneut lokal gelesen und SHA256 gegen bekannte Referenz
  bestaetigt. Begrenzte Bootroutinen-Analyse zeigt Staging-Kopie und
  App-Handoff, aber keinen Nachweis eines app-unabhaengigen UART-Rettungswegs.
  Das private Abbild wurde nicht veroeffentlicht; Referenzdump identifiziert
  nicht automatisch den aktuell eingebauten Loader.
- Letzter Entwicklungszweig-Commit `6417e1ac5488e31a7ac60b07814d650099e58996`
  ergaenzt nur Uebergabe-Dokumentation. Quellinhalt bleibt der getestete.
- Naechste benoetigte reale Angaben: aktuell installierte Firmware und
  tatsaechlicher Flashtransport des DeltaESC-Zielcontrollers, danach
  Rueckflash-Nachweis ohne ST-Link und gemessene G30-Motordaten. Keine
  weitere Motorentwicklungs-Zustimmung ist offen.

## Historischer Auftrag vom 20.10.2026 / damalige Freigabe
- Verbindlichen Vertrag hinterlegen.
- Quellstand DeltaESC, EBiCS, SmartESC pruefen und dokumentieren.
- Simulation und Offlineentwicklung vorbereiten.
- Innerhalb dieser Aufgaben selbststaendig fortfahren; keine einzelne "weiter"-Freigabe nach jedem Softwaretest erforderlich.
- **Nicht freigegeben:** Flashen, Powerstage-/Motortests, Aenderungen an Bootloader/IAP/Recovery, Spekulation ueber unbekannte Flash-Hardware, Umgehung vorhandener Release-Holds, neue Sicherheitssperren, Versions-/Kompatibilitaetsgates.
- Kein Controller fuer echte Hardwaretests vorhanden. `xbot-remote-lab`-Queue ist privat und bleibt unberuehrt.

## Quellen / Kanonische Staende (nicht verwechseln)

### DeltaESC
- Repo: [DeltaESC-G30D](https://github.com/ZachWay9bot/DeltaESC-G30D), Branch `main`
- Gesehener Ausgangs-Commit: `0e95a3c604c7d22d6d3becb22a3e666973d846f6` (2026-10-19 UTC).
- Gesehen: `README.md`, `CURRENT_RELEASE.md`, `MEASUREMENTS.md`, `UART_RECOVERY_RELEASE_HOLD.md`, Quell-/BIN-/SHU-Dateinamen im Repo-Tree.
- Referenz: `v0.10.2 ACTIVE TELEMETRY RC`, FW_BUILD `0x1020`.
- Source: `downloads/DeltaESC_G30D_v0_10_2_COMPLETE_SOURCE.zip`; BIN `downloads/DeltaESC_G30D_v0_10_2_active_telemetry_rc.bin`.
- Laut Release: BIN SHA256 `2b6e26b656a25bdab2b2e98eca447452b66628208cecf956e0df01134cf9eb75`; CI-Build `39159514233`.
- Dokumentierter Sensorless-Ablauf: Rollstart -> BEMF/Observer -> ROLL_VERIFY -> begrenzte Torque-Uebergabe. Fo60/Fo69 **DONOR/XBOT**-Belege, kein realer G30D-Motorlauf dieses v0.10.2-Images.
- Status: experimenteller Bench-Kandidat, veroeffentlichter Flash-HOLD; ST-Link als frueher erreichbarer Pfad fuer originalen G30D getrennt vom vergossenen Controller betrachten.
- **Noch offen:** ADC/PWM/Deadtime/FOC auf genau der Zielhardware messen; nicht aus dem Donor-Test folgern.
- Archiv-ZIP in diesem Audit **nicht byteweise entpackt**; Aussagen ueber Funktionsdetails aus Repo-Dokumentation und sichtbaren Einzelquellen.

### EBiCS
- Kein separates EBiCS-GitHub-Repository unter den aktuell gelisteten `ZachWay9bot`-Repos gefunden.
- Letzte **explizit real dokumentierte** EBiCS-Firmware: `v0.3.4-r6 BUTTON_SHORT_FIX` auf G30D Gen1 (Bericht 2026-10-13).
- Belegt im Bericht: BLE Legacy-Crypto 5B/5C/5D, Power-Tasten-Bestaetigung, MIC verified; im spaeteren 13.10.-Handoff ESC-Registerleseroute, DRV `0x0034`, D0-Signatur `0x4730`, ABI 3, Fault `0x0011`.
- r6 BIN laut Bericht: 45.680 Bytes, SHA256 `d2433b3c446a40982439523d669e6a4d568b225ce9e6ced76c13b80c78d35645`. Unabhaengiger Checksum-Scan hier **nicht** ausgefuehrt.
- In der ChatGPT-Dateibibliothek identifiziert (aber Rohbytes in dieser Sitzung nicht materialisierbar):
  - `/DeltaESC G30D/G30_EBiCS_r9_FO76_GOVERNOR_BUILT_SOURCE_20261018.zip` (neuere Entwicklungsquelle, nicht automatisch real qualifiziert);
  - `/xbotwebdev/G30_EBiCS_r9_RECOVERY_INVARIANT_SOURCE_20261020.zip` (Quellen-/Recovery-Zweig, nicht als getestete Firmware darstellen);
  - `EBICS_2026-10-13_UEBERGABE_r6_BLE_OK.md`, `G30D_DeltaESC_EBiCS_UEBERGABE_2026-10-13.md`.
- Frueheres r6-Benchmark-Protokoll: ADC/Fault `0x0011`, Zyklusbudget `496/496` verletzt; **historischer** Befund, kann in juengeren r9-Quellen veraendert sein.
- **Noch offen:** Neuerste EBiCS-Quelle byteweise oeffnen, Build/Hosttests reproduzieren; ohne das kein Quell-Audit und keine Aussagen zur Wirkung der r9-Aenderungen. BL-/Recovery-Aenderungen nicht vornehmen.

### SmartESC
- Repo: [SmartESC_STM32_v21b](https://github.com/ZachWay9bot/SmartESC_STM32_v21b), Branch `vesc_comp`
- Gesehener Ausgangs-Commit: `13eea0c1ed927cdeb4111fc77c3d3b939ca326e6` (2026-10-19 UTC).
- Firmware laut `VERSION`/`README.md`: `SmartESC G30 NativeDash v0.8.7`.
- Sichtbare Quellpfade: `common_files/src/g30_sensorless_core.c`, `g30_sensorless.c`, `VescCommand.c`, `VescToSTM.c`, `g30_recovery_iap.c`, `g30p/`, `tools/`.
- Dokumentierte Funktionen: VESC Tool 6.06/USART1 PB6/PB7, Ninebot-Dash USART2/PA2, Brake-priorisiert-ueber-Throttle, sensorless Rollstart, Detect All.
- Ziel Gen1/Gen2: gemessene statt pauschal aus Seriennummer abgeleitete Motorkonstanten.
- 3-Sekunden-UART-Recovery ist **in der austauschbaren Application**, nicht in einem separaten Bootloader; laut `tools/recovery/RECOVERY_RELEASE_HOLD.md` kein garantierter Rescue-Pfad bei nicht startender App.
- Status: bestehender Release-HOLD, exaktes v0.8.7-Image noch nicht am neuen Controller hardwarequalifiziert. Alte BIN/ZIP im Repository sind historische Artefakte.
- **Noch offen:** Hostmodelle fuer Speed/Pole-Pairs, Brake-Priority, Detect-State, Observer und Faultabbruch; echter G30-Hardwaretest spaeter.

## Motorprofil-Trennung fuer IntheLoop Virtual Controller Pack (Korrektur 20.10.2026)
- **Donor/Testmotor:** E-Bike-Frontnabenmotor. Die bisherigen XBOT-Motorlauf-/BEMF-/Flux-Logs FO60, FO69 und FO70 beziehen sich auf diesen Testmotor und die damalige Testhardware, **nicht** auf den Ninebot G30 Gen1-Motor.
- **Vorlaeufige Donor-Referenzwerte** aus den Firmware-Unterlagen: R-Phase etwa 0,583 Ohm; Ld etwa 0,640 mH; PM-Flussverkettung etwa 12,1 mWb. Diese Werte nicht als G30-Gen1-Messungen deklarieren.
- **G30 Gen1 Zielmotor:** Eigene physikalische Messung ist laut Projektbesitzer demnaechst moeglich; R/L/Fluss, Polpaarzahl, Traegheit und Hall-/BEMF-Zuordnung fuer dieses Profil bis dahin **unbestimmt bzw. zu verifizieren**.
- Virtuelles Labor verwendet strikt getrennte Profile `ebike_front_hub_donor` (mit expliziter Provenienz) und `ninebot_g30_gen1` (zunaechst **nicht kalibriert**). Keine stille Uebernahme von Donorwerten in G30-Gen1-Modell oder Firmware-Defaults.
- G30 Gen2 ist spaeter ein **drittes** separates Profil, sofern benoetigt.
- Keine Aenderung an Firmware-Koeffizienten, Motorregelung oder Flash-/Recovery-Pfaden durch diese Dokumentationskorrektur.

## IntheLoopRemoteLab
- Repo: [IntheLoopRemoteLab](https://github.com/ZachWay9bot/IntheLoopRemoteLab), Branch `main`.
- Baseline vor Auftrag `v0.4.1-dev`; generic Core, GitHub-Issue-Transport, Loader, bestehender Simulator. Der laufende Core erlaubt `identify` und `diagnose` (keine Motor-/Flashoperationen).
- Neu: `PROJECT_CONTRACT.md` v1.0; `remotelab/adapters/offline_fixture.py` (nur synthetic); `examples/offline_firmware_adapters.example.json` mit drei Projekten; `tests/test_offline_firmware_fixture.py`.
- Auf Schreib-/Flash-/Recovery-Komponenten wurden **keine** Aenderungen vorgenommen.

## Nächste Schritte (innerhalb der Freigabe)
1. Naechste Offline-Hosttests an tatsaechlichen Firmwarefunktionen von DeltaESC/SmartESC vorbereiten; bisher sind nur RemoteLab-/Fixture-Tests CI-gruen.
2. Offline-Matrix und Testdaten-/Evidence-Konvention versionieren.
3. Vorhandene EBiCS-r6/r9-Quellen erst nach autorisiertem Bytezugriff wirklich lesen; r6 Hardware-Referenz **nicht** mit r9 Softwarestand verwechseln.
4. Projektweise isolierte Hosttests anhand **tatsaechlicher** Firmwarefunktionen entwickeln (keine simulierten Werte als FOC-/ADC-Validierung ausgeben).
5. Vor naechstem Hardwaretest die reale Zielhardware und den zu verwendenden existierenden Flashpfad gemeinsam bestaetigen.

## Nicht wiederholen
- Keine zusaetzlichen hypothetischen Bootloader-/Flashgroessen-/CRC-Sperren einfuehren.
- Erfolgreiche BLE-Handshake-Nachweise nicht erneut als ungeklaertes Problem behandeln.
- Erfolg einer Modellrechnung nicht als hardwarequalifizierten Motorlauf ausgeben.
- Keine Aktualisierung des privaten xbot-remote-lab oder anderer Firmware-Repos ohne konkreten Aenderungsbedarf.

## Chatwechsel-Prozedur
**Dieser Bericht und `PROJECT_CONTRACT.md` muessen vor dem ersten Schreibvorgang erneut geoeffnet werden.** SHA und offene Punkte mit aktuellem GitHub abgleichen. Unbekanntes explizit als unbekannt markieren. Nach wesentlichen Aenderungen Bericht versioniert fortschreiben.

## Fortschrittsnachtrag (20.10.2026)
- Zentrale Vertragsdatei erstellt, Commit `794468483824db8946adab0e3cf3f11e85ce7e3d`.
- Offline-Fixture-Adapter, 3-Projekt-Beispiel, Windows-Starter, Smoke-Runner, Unit-Tests und Offline-Plan erstellt. **Keine** Produktionsfirmware und kein Flash-/Recoverypfad geaendert.
- `tests/test_offline_firmware_fixture.py` sowie `tests/test_offline_smoke_runner.py` werden im bestehenden Unit-Test-Workflow ausgefuehrt.
- GitHub Actions `tests` auf Python 3.10/3.12 **PASS** am Commit `95aef8dc40a490dc03c6025112d56da559186604`, Run [39471270697](https://github.com/ZachWay9bot/IntheLoopRemoteLab/actions/runs/39471270697).
- Dokumentations-Verweise zu diesem Vertrag in DeltaESC `eb30fbfd61fba4768be399a3aedf98dc2c2039f0` und SmartESC `cd33fdb86a542c881b90adf70175bd82971012c6`; beide **nur Dokumentations-Commits**.
- Beleggrenze: Der RemoteLab-Durchlauf prueft synthetische Fixtures und Job-Dispatch, **nicht** STM32-Firmware-Code oder Realhardware. Die EBiCS-r9-Source-ZIPs wurden als Library-Metadaten gefunden, konnten aber aus der Library nicht als Rohdatei materialisiert werden.
- Neue lokale Run-Anleitung: `START_OFFLINE_3FW.cmd`. Source- und Testplanung: `docs/OFFLINE_DEVELOPMENT_DE.md`.

**Noch NICHT abgeschlossen:** echte DeltaESC-/EBiCS-/SmartESC-Firmware-Hostsimulationen, aktuelles EBiCS-r9-Byteaudit, neue Firmware-Builds sowie sämtliche Controller-Hardwaretests. Hier keinen Erfolg behaupten.

## AKTUELLE ARBEITSANWEISUNG — Firmware first, KEIN Simulator (20.10.2026, spaeter)

Der Projektbesitzer hat das zuvor diskutierte **IntheLoop Virtual Controller Pack / die Motor-/Dashboard-Simulation als aktuelles Entwicklungsziel ausdrücklich verworfen**. Wichtig ist ausschliesslich, die drei realen Firmwareprojekte schneller und nachvollziehbar moeglichst weit fertigzustellen. Bestehende synthetische Offline-Fixtures sind KEINE Firmwaretest-Belege und duerfen nicht als solche ausgegeben werden. Keine weitere Virtualisierung oder Simulation fuer diesen Auftrag anlegen.

Arbeitsstil: Bei jedem wesentlichen Schritt **vorher** angeben: (1) was, (2) warum, (3) Erfolgskriterium, (4) was wirklich hardwareabhängig offen bleibt, (5) ob es ein wichtiger Blocker ist. Regulaere bestandene Build-/Hosttests selbstaendig fortsetzen. Bei einem Blocker Optionen und Aufwand aufzeigen; der Nutzer entscheidet, ob wir daran bleiben. Keine ungefragten Aenderungen an Flash-/IAP-/Recovery-Routinen oder bestaetigt funktionierenden Funktionen.

### Erster echter Source-/CI-Befund
- SmartESC Branch `vesc_comp`, Commit `13eea0c1ed927cdeb4111fc77c3d3b939ca326e6`: GitHub Actions `Build G30 NativeDash on commit` Run [39340841437](https://github.com/ZachWay9bot/SmartESC_STM32_v21b/actions/runs/39340841437) **FAILED** im eigentlichen Schritt `Build G30P`.
- Joblog zeigt konkret `region 'FLASH' overflowed by 4 bytes` beim Linken von `g30p.elf`; **kein** generischer Compilerfehler, sondern 4-Byte-Grenze der gelinkten App. Keine Linkerregion vergoessern; ein minimaler, semantisch unveraenderter Codegroessen-Fix auf isoliertem Entwicklungszweig ist moegliche naechste Arbeit.
- Positiver `G30 UART Recovery Anti-Lockout Audit` Run [39471169437](https://github.com/ZachWay9bot/SmartESC_STM32_v21b/actions/runs/39471169437) ersetzt den fehlgeschlagenen App-Build NICHT.
- Im echten Quellcode `common_files/src/app.c` existiert unter `case APP_ADC:` kein `break` vor `case APP_ADC_UART:`, wodurch zusaetzlich `task_cli_init(&aux_uart)` durchlaufen wird. Moeglicher Funktionsfehler / fragliche Doppelinitialisierung; Beurteilung haengt von aktiver Konfiguration ab. Noch NICHT geaendert und NICHT als bewiesener Laufzeitfehler etikettieren.
- `common_files/inc/appconf_default.h` definiert standardmaessig `APPCONF_APP_TO_USE=APP_UART` vorbehaltlich anderer Overrides. Kein Beleg, dass `APP_ADC` im aktuellen Fahrzeug-Default tatsaechlich aktiviert wird.
- DeltaESC v0.10.2: dokumentierter alter kompletter Cortex-M3-/Host-CI-Build `39159514233` erfolgreich; aktuellste Runs sind nur `UART recovery safety audit`, keine neue aktive Motortest-Qualifikation.
- EBiCS r9: exakte neue Source-Archive liegen in der Library, aber konnten im bisherigen Zugriff nicht byteweise materialisiert werden. Keine Quellcode-Fixes als erledigt behaupten.

### Naechste sinnvolle Arbeitspakete
1. SmartESC 4-Byte-FLASH-Ueberlauf **isoliert** beseitigen und denselben Build in CI gruen bekommen, ohne Speicherlayout/Recovery zu aendern (hoch, Softwareblocker).
2. SmartESC `APP_ADC`-Fallthrough und Dashboard-Bremsprioritaet mit realem Quellstand untersuchen und gezielte Host-/Quelltests erstellen (hoch, sofern Pfad verwendet).
3. DeltaESC-Quell-ZIP fuer byteweises Audit bereitstellen, bestehende Testlogs/BIN-Identitaet pruefen; echte G30-Gen1-Motormessungen bleiben spaeter (mittel; kein Anlass fuer Modell-Simulation).
4. EBiCS r9 exaktes Archiv zugaenglich machen; insbesondere ADC-Budget/Bootpfad, UART/BLE und reale r6-Referenz vergleichen, ohne Restore-/Flashweg anzugreifen (hoch, Source-Zugriff derzeit Blocker).
5. Erst danach gemeinsame reproduzierbare Source-Builds und Softwareregressionen, jeweils an Original-Firmwarecode (hoch).

**Status: Dieses Update ist reine Projektorganisation und Source-/CI-Analyse; an den drei Firmwarequellen wurde noch nichts veraendert.**

## Verbindliche FO72-Rueckkehr — nachtraegliche Nutzerentscheidung vom 20.10.2026

**Fuer die XBOT/G30-identical-Firmwareentwicklung (NICHT fuer die RemoteLab-Agentversion)** gilt ab sofort `XBOTFO72V00721` (FW 0.7.2.1) als rueckzusetzende Originalbasis. Alle ab FO91/0.9.1 eingefuehrten experimentellen Bootloader-CRC-/Flashgroessen-IAP-Lockouts duerfen nicht wieder eingefuehrt oder als Voraussetzung fuer neuen Firmwarecode uebernommen werden.

Beweise aus privatem GitHub-RemoteLab-Issue #1:
- FO72-Flash erfolgreich, SHA256 des historischen 20.920-Byte-Images `1edf01b3127ac596d840119b2bbd1b60bc1f9ea493590e734abdd5ce20739d6d`.
- FO72 -> FO73-Flash erfolgreich; somit war FO72-IAP damals funktionsfaehig.
- FO72 Motor-Wizard war wegen `PARAM_FAULT/L_WEAK` **noch nicht erfolgreich**. FO73 hatte einen separaten LFIX; nicht stillschweigend in FO72 hineinkopieren.
- Spaeter FO91/0.9.1: Image `XBOTFO91V00911`, IAP-Error 7 und BootCRC/Flashgroessen-Guard laut r9-Rekonstruktion.

Die bindende Detailreferenz liegt in [xbot-remote-lab / FO72_SOURCE_ROLLBACK_BASELINE.md](https://github.com/ZachWay9bot/xbot-remote-lab/blob/main/FO72_SOURCE_ROLLBACK_BASELINE.md) (privates Repository).

**BLOCKER fuer echten Source-Rollback:** Das Original-Source-ZIP `XBOT_FO72_MOTOR_DETECTION_WIZARD_COMPLETE_SOURCE_20261017.zip` existiert in der Library unter `/xbotwebdev/`, aber seine Rohdaten sind in dieser Sitzung **nicht** freigegeben/materialisierbar. Das private GitHub-Repo hat keinen vollstaendigen FO72-Source-Checkout. Deshalb wurde bislang nur die Ruecksetzentscheidung versioniert, **noch keine Firmwarequelle zurueckgesetzt und keine Hardware geflasht**. Nur mit lesbaren Original-Source-Bytes FO72 wirklich restore'n; keinen falschen Reset oder Neuaufbau aus FO91 vortaeuschen.

Die drei laufenden Firmwareprojekte DeltaESC, EBiCS, SmartESC werden weiterhin separat behandelt; keine pauschale unbeauftragte Downgrade-/Recovery-Aenderung in ihnen.

## FO76-Quellpaket jetzt lokal geprueft (21.10.2026)

Der Benutzer hat `XBOT_FO76_CURRENT_GOVERNED_WIZARD_COMPLETE_SOURCE_20261018.zip` direkt hochgeladen. Originalarchiv-SHA256 `298a6624d729e7b3a71ba8787c3b9da05196251d74488584a22992886f18f97c`.

- FO76 ist **nicht** FO72; allerdings vollstaendige rekonstruierbare Original-Source von v0.7.6 und klar **vor FO91/0.9.1**.
- Im ausgepackten FO76-Archiv: 15 C-Sources, 22 native C-Tests, `Makefile`, `linker.ld`, IAP-Quelldatei, Bench und G30_PASSIVE.
- ARM-Neubuild **byteidentisch** zu beiden Archiv-BINs, checksum/decryption OK; 22/22 C-Tests PASS.
- BENCH `XBOTFO76V00761`, SHA256 `a8b7ca7d45fdfa32cbcbfdfbe98e2e655a266ecc57aea62f8149ecf3cbe74bcb`.
- G30_PASSIVE `XBOTFO76V00760`, SHA256 `e1aa7d2f35c4596220ad03a4284e38ce8abf9b4137226b99fdfb305386723154`.
- `src/iap.c` enthaelt **keinen** FO91-CRC/F1-Flashgroessen-Gate. Das entfernt NICHT bereits vorhandene Defekte im realen Controller; keine Hardware-Ruecksetzung.
- 4/19 Baseline-Hash-Eintraege der **alten** `BASELINE_GUARD_SHA256.txt` passen nicht mehr zur mitgelieferten FO76-Quelle. Einzelheiten in [FO72_SOURCE_ROLLBACK_BASELINE.md](https://github.com/ZachWay9bot/xbot-remote-lab/blob/main/FO72_SOURCE_ROLLBACK_BASELINE.md) des privaten XBOT-Repos.
- **Ab jetzt fuer Software-Weiterarbeit:** exakt dieses FO76-v0.7.6-Quellpaket als verfügbare vor-FO91-Basis nutzen, bis der Benutzer ggfs. FO72-Originalquelle verfuegbar macht. Kein fiktiver FO72-Quellbaum.
- **NICHT geschehen:** Source-Paket in private Repo `firmware/` importiert; bisher nur Pruefbericht und Basisentscheidung hinterlegt. Nie irrefuehrend als Quell-Rollback in GitHub bezeichnen.
- FO76 G30_PASSIVE ist messungs-only, kein fahrfertiges G30D-Image; Bench-Profileinstellungen stammen vom E-Bike-Frontnaben-Donor.
