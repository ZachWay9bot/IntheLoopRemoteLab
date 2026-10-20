# RemoteLab unter Windows installieren

## Voraussetzungen

- Windows 10 oder 11
- Python 3.10 oder neuer
- Git optional
- fuer reale Hardware die zum Adapter passenden Treiber

## Repository holen

```cmd
git clone https://github.com/ZachWay9bot/IntheLoopRemoteLab.git
cd IntheLoopRemoteLab
```

## Tests

```cmd
py -m unittest discover -s tests -v
```

## Simulator

```cmd
START_SIMULATOR.cmd
```

oder:

```cmd
py -m remotelab
```

Das Audit-Log wird standardmaessig unter `runtime/audit.jsonl` erzeugt.

## Queue-Agent

Beispielkonfiguration kopieren:

```cmd
copy examples\remotelab.queue.example.json remotelab.json
```

Danach Queue-Daten und Adapter in `remotelab.json` konfigurieren.

Ein Poll:

```cmd
RUN_AGENT_ONCE.cmd
```

Dauerbetrieb:

```cmd
RUN_AGENT.cmd
```

Adapterspezifische Installation steht unter `docs/adapters/`.

## Offline-Entwicklung ohne Controller (drei Firmwareprojekte)

Im Repository-Ordner:

```cmd
START_OFFLINE_3FW.cmd
```

Dabei laufen normale Unit-Tests sowie die drei synthetischen Offline-Adapter.
**Dies ist kein Firmware-Build und kein Nachweis von Motor-/ADC-Hardwaretests.**
Verbindliche Regeln und aktuelle Schichtuebergabe: `PROJECT_CONTRACT.md`, `PROJECT_HANDOFF.md`.
