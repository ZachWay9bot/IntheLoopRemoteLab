# RemoteLab

RemoteLab ist eine generische Hardware-in-the-Loop-Infrastruktur fuer Entwicklungsprojekte mit realer externer Hardware.

Entwicklungslogik, Jobsteuerung, Audit und Transporte bleiben hardwareunabhaengig. Geraetespezifische Protokolle und Funktionen leben ausschliesslich in Adaptern.

## Status

**v0.4.1-dev**

- generischer Core
- lokaler Simulator
- dynamisch geladene Device-Adapter
- generischer GitHub-Issue-Transport
- persistente Job-Deduplizierung und Audit
- Hardware-Schreiboperationen im aktuellen Core gesperrt
- CI fuer Python 3.10 und 3.12

## Struktur

```text
RemoteLab
├─ remotelab/
│  ├─ core/
│  ├─ transports/
│  ├─ auth/
│  └─ adapters/
├─ docs/
│  └─ adapters/
├─ examples/
├─ tests/
└─ tools/
```

Der Core kennt keine konkrete Hardware. Adapter werden per Modul- und Klassenname aus der Konfiguration geladen.

## Quick Start

```cmd
py -m unittest discover -s tests -v
py -m remotelab
```

## Queue-Agent

Konfiguration aus `examples/remotelab.queue.example.json` nach `remotelab.json` kopieren und anpassen.

Ein Poll:

```cmd
py -m remotelab once --config remotelab.json
```

Dauerbetrieb:

```cmd
py -m remotelab run --config remotelab.json
```

Das Job-Protokoll ist unter `docs/JOB_QUEUE_PROTOCOL_DE.md` beschrieben.

## Adapter

Geraetespezifische Hinweise liegen ausschliesslich unter `docs/adapters/`.

## Verbindliche Projektregeln / Schichtuebergabe

- [PROJECT_CONTRACT.md](PROJECT_CONTRACT.md) — freigegebener Entwicklungsvertrag; funktionierende Firmware-/Recoverypfade nicht ungefragt veraendern.
- [PROJECT_HANDOFF.md](PROJECT_HANDOFF.md) — aktuelle Quellstaende, Evidenz, Freigaben und naechste Schritte fuer DeltaESC, EBiCS und SmartESC.

## Drei Firmwareprojekte ohne Controller vorbereiten

Unter Windows:

```cmd
START_OFFLINE_3FW.cmd
```

Das startet die bestehenden Unit-Tests und den synthetischen Offline-Fixture-Test fuer alle drei Projekte. **Es wird keine Firmware ausgefuehrt, nichts geflasht und kein Motor angesteuert.** Die Quelle fuer echte zukuenftige Hosttests ist [docs/OFFLINE_DEVELOPMENT_DE.md](docs/OFFLINE_DEVELOPMENT_DE.md).
