# Offlineentwicklung: DeltaESC, EBiCS, SmartESC
Stand: 2026-10-20
Vertrag: [../PROJECT_CONTRACT.md](../PROJECT_CONTRACT.md)
Uebergabe: [../PROJECT_HANDOFF.md](../PROJECT_HANDOFF.md)

## Was wir HEUTE tatsaechlich testen
- Die existierende IntheLoopRemoteLab-Engine und Adapter-Ladefunktion nutzen.
- Drei voneinander getrennte **synthetische** Testadapter identifizieren/diagnostizieren.
- Audit/Job-Dispatch und die vorhandene Sperre fuer Flash- und Motoroperationen testen.
- Keine Hardware, keine echten UART-Frames, kein ausgefuehrter STM32-Code, keine FOC-Simulation in diesem Fixture-Test.
- Kein Beleg, dass Firmware elektrisch funktioniert oder fahrbereit ist.

Offline-Start:
```bat
START_OFFLINE_3FW.cmd
```
Oder: `py -m unittest discover -s tests -v`.

## Geplante echte Firmware-Hosttests (nur auf realem Source-Stand)
| Projekt | Quelle | Offline-Pruefung | Hardware bleibt offen |
|---|---|---|---|
| DeltaESC | v0.10.2 Source ZIP im eigenen GitHub-Repo | ADC Offset/Rekonstruktion, PWM/Deadtime-Registerlogik, Observer-FOC Zustandsautomat, Bremse/Coast, Loss-of-signal | elektrische PWM, Stromsensor, Gate-Signale, Motor-Fahrtest |
| EBiCS | r6 BLE-Hardware-Referenz; neuere r9 Source-ZIPs in Library | CMD 5B/5C/5D, BLE/ESC-Read, Timing-Budget, Faults, ADC-Rechenpfad, Kaltstart | r9 Hardwareverifikation, echte ADC-/TIM1-Messung |
| SmartESC | v0.8.7 in `SmartESC_STM32_v21b` / `vesc_comp` | VESC-Frame-Decoding, Motorpole/Speeds, Gas-Bremse-Prioritaet, Detect-Zustandsautomat, Observer-Fixedpoint | reale Sensorless-Uebergabe, Bremswirkung, Duty-/Deadtime-Proben |

**In den Fixture-Daten enthaltene Werte sind rein exemplarische Labels**. Echte Tests werden erst als bestanden bezeichnet, wenn der exakte Code kompiliert/ausgefuehrt und die Ausgabe dokumentiert wurde.

## Nächste werkzeugseitige Erweiterungen
1. Quell-/Testpakete mit sha256 und Herkunft einfrieren; EBiCS Library-ZIP ist derzeit als Metadaten auffindbar, aber nicht byteweise in dieser Sitzung lesbar.
2. Projektweise Host-Builds/Tests in isolierten Jobs; keine Aenderung am bestehenden IAP-/Recovery-Code.
3. Tests an echten Firmwarefunktionen, nicht an frei erfundenen Dummydaten. Jede Regression nennt Source-SHA, Testkommando, Log und Grenzen.
4. Erst spaeter reale Hardwareadapter auf Basis der **bereits bewaehrten** Kommunikationspfade und eines freigegebenen Testplans.

## Sicherheits- und Freigabegrenzen
Die aktuellen separaten DeltaESC-/SmartESC-Releases enthalten einen vorhandenen Flash-HOLD; er wird in diesem Offline-Arbeitspaket **nicht** verändert. Der generische Core bleibt read-only. Das sind Fakten ueber den IST-Stand, keine neue Anweisung zu hypothetischer Drittgeraete-Kompatibilitaet.

Kein automatischer Neustart beliebiger Motor-/Flash-Jobs, kein Freigabe-Bypass, kein neues Schloss am Firmware-Eingang. Bei unerwarteten Ergebnissen anhalten, Logs liefern, nicht das Grunddesign austauschen.

## Reproduzierbarkeit
- Repo `ZachWay9bot/IntheLoopRemoteLab`, Branch `main`.
- `py -m unittest discover -s tests -v` prueft die vorhandenen Tests und die drei Offline-Fixture-Adapter.
- GitHub Actions `.github/workflows/tests.yml` laeuft auf Python 3.10/3.12.
- Tests koennen ohne Controller ausgefuehrt werden.
