# RemoteLab Job Queue Protocol v1

## Kommando

Ein Queue-Kommentar beginnt exakt mit:

```text
REMOTELAB-CMD/1
```

Direkt danach folgt ein JSON-Objekt:

```json
{
  "id": "sim-identify-001",
  "device": "simulator",
  "operation": "identify",
  "args": {}
}
```

Erlaubt sind exakt die Felder `id`, `device`, `operation` und `args`.

## Ergebnis

Der Agent schreibt:

```text
REMOTELAB-RESULT/1
```

gefolgt von einem kompakten JSON-Ergebnis.

## Deduplizierung

- Job-IDs werden lokal als abgeschlossen gespeichert.
- Der Kommentar-Cursor wird vor der Geraeteoperation persistent gespeichert.
- Ein laufender Job wird als `in_flight` gespeichert.
- Wird der Agent waehrend eines laufenden Jobs beendet, wird dieser Job beim Neustart nicht automatisch wiederholt.
- Stattdessen wird ein Ergebnis mit `status=execution-uncertain` erzeugt. Fuer einen erneuten Lauf ist eine neue Job-ID erforderlich.

Damit bleibt der Transport auch fuer spaetere Hardware-Schreiboperationen at-most-once.

## v0.4.1 Operationen

Der Core akzeptiert derzeit nur:

- `identify`
- `diagnose`

Andere Operationen werden vom Core abgewiesen.

## Beispiel Simulator

```text
REMOTELAB-CMD/1
{"id":"sim-001","device":"simulator","operation":"diagnose","args":{}}
```

## Beispiel XBOT read-only

```text
REMOTELAB-CMD/1
{"id":"xbot-id-001","device":"xbot_readonly","operation":"identify","args":{}}
```

oder:

```text
REMOTELAB-CMD/1
{"id":"xbot-diag-001","device":"xbot_readonly","operation":"diagnose","args":{}}
```
