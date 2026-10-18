# RemoteLab unter Windows installieren

## Voraussetzungen

- Windows 10 oder 11
- Python 3.10 oder neuer
- Git optional
- fuer reale Hardware die zum Adapter passenden Treiber

## Repository holen

```cmd
git clone https://github.com/ZachWay9bot/RemoteLab.git
cd RemoteLab
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
