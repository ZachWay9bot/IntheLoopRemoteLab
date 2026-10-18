# RemoteLab unter Windows installieren

## Voraussetzungen

- Windows 10 oder 11
- Python 3.10 oder neuer
- Git optional, aber empfohlen
- fuer reale Hardware spaeter die passenden USB-/UART-Treiber

## Repository holen

Mit Git:

```cmd
git clone https://github.com/ZachWay9bot/RemoteLab.git
cd RemoteLab
```

Oder das Repository als ZIP laden und entpacken.

## Offline-Test

```cmd
py -m unittest discover -s tests -v
```

Der v0.4-Stand benoetigt fuer Core und Simulator keine externen Python-Pakete.

## Simulator starten

```cmd
START_SIMULATOR.cmd
```

oder:

```cmd
py -m remotelab
```

Dabei wird unter `runtime/audit.jsonl` ein lokales Audit-Log erzeugt.

## Noch nicht tun

- produktiven XBOT-Agent ersetzen
- COM9 aus RemoteLab v0.4 oeffnen
- Firmware ueber den neuen Core flashen
- Motor-Testjobs ueber den neuen Core senden

Diese Pfade werden erst nach der read-only Migration aktiviert.
