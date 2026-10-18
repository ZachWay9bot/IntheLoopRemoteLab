# XBOT adapter

Dieser Adapter kapselt die geraetespezifische Kommunikation fuer den bestehenden Controller.

## Aktueller Umfang

Der produktive Schreib- und Testpfad wird waehrend der Migration nicht ersetzt. Der neue Adapter beginnt mit:

- `identify`
- `diagnose`

Die read-only Variante sendet nur die benoetigten Lese- und Diagnosekommandos.

## Installation

Serielle Unterstuetzung installieren:

```cmd
py -m pip install -e ".[serial]"
```

## Konfiguration

```json
{
  "module": "remotelab.adapters.xbot",
  "class": "XbotReadOnlyAdapter",
  "enabled": true,
  "args": {
    "port": "COM9"
  }
}
```

## Migration

Vor der Freigabe weiterer Operationen werden Protokoll, Timeouts, Identitaetspruefung und Fehlerpfade gegen Mock-Serial und anschliessend gegen reale Hardware validiert. Schreiboperationen bleiben bis dahin im Core gesperrt.
