# RemoteLab

RemoteLab ist eine generische Hardware-in-the-Loop-Infrastruktur fuer Entwicklungsprojekte mit realer externer Hardware.

Der zentrale Gedanke: Entwicklungslogik, Jobsteuerung und Audit gehoeren in einen hardwareunabhaengigen Core. Protokolle, Flashwege und aktive Tests werden ueber getrennte Device-Adapter angebunden.

## Status

**v0.4.1-dev**

- generischer Core
- lokaler Simulator
- read-only Adapter-Schnittstelle
- XBOT als Legacy-Adapter vorgesehen\n- optionaler read-only XBOT-Adapter fuer Identitaet und 0xF0-Diagnose
- bestehende XBOT-Job-Queue bleibt unveraendert und ist **nicht** dieses Repository
- Hardware-Schreiboperationen sind im neuen Core zunaechst gesperrt

## Repository vs. Job-Queue

Dieses Repository ist das **Projekt-Repository** fuer Source, Dokumentation, Tests und Releases.

Die bereits produktiv verwendete XBOT-Queue bleibt separat und unveraendert. RemoteLab wird spaeter verschiedene Transport-Backends unterstuetzen koennen, darunter lokale Jobs und GitHub-Issue-Queues.

## Zielarchitektur

```text
ChatGPT / Entwickler
        |
        v
   RemoteLab Core
   |     |      |
   |     |      +-- Audit / Permits / Policies
   |     +--------- Job Engine
   +--------------- Transports
        |
        +-- local
        +-- github_issue (spaeter generisch)
        +-- xbot_legacy
                 |
                 v
              Adapter
        +-- XBOT
        +-- ESP32
        +-- STM32
        +-- RP2040
        +-- Messgeraete
```

## Sicherheit bei der Migration

Der produktive XBOT-Agent wird nicht ersetzt, bis der neue Core mit Simulatoren und read-only Hardwarepfaden validiert ist. Insbesondere werden Flash- und Motor-Testpfade nicht einfach aus einem aelteren Agentstand uebernommen.

## Quick Start

Windows mit Python 3:

```cmd
py -m unittest discover -s tests -v
py -m remotelab
```

Weitere Dokumentation liegt unter `docs/`.


## Queue-Agent

Konfiguration aus `examples/remotelab.queue.example.json` nach `remotelab.json` kopieren und anpassen.

Ein einzelner Poll:

```cmd
py -m remotelab once --config remotelab.json
```

Dauerbetrieb:

```cmd
py -m remotelab run --config remotelab.json
```

Das generische Queue-Protokoll ist unter `docs/JOB_QUEUE_PROTOCOL_DE.md` dokumentiert.
