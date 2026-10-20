# PROJECT_HANDOFF.md — verbindliche Schichtuebergabe
Stand: 2026-10-20
Contract: [PROJECT_CONTRACT.md](PROJECT_CONTRACT.md), Version 1.0

## Aktueller Auftrag / explizite Freigabe
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
