# RemoteLab Job Queue Protocol v1

## Kommando

Ein Queue-Kommentar beginnt exakt mit:

```text
REMOTELAB-CMD/1
```

Danach folgt ein JSON-Objekt:

```json
{
  "id": "job-001",
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
- Stattdessen wird `status=execution-uncertain` gemeldet.
- Fuer einen erneuten Lauf ist eine neue Job-ID erforderlich.

Damit bleibt der Transport fuer spaetere Hardware-Schreiboperationen at-most-once.

## Aktuell freigegebene Core-Operationen

- `identify`
- `diagnose`

Weitere Operationen werden erst ueber Policies freigegeben.

## Beispiel

```text
REMOTELAB-CMD/1
{"id":"probe-001","device":"simulator","operation":"diagnose","args":{}}
```

Der Device-Name bezeichnet nur den geladenen Adapter. Das Queue-Protokoll selbst kennt keine geraetespezifische Logik.
