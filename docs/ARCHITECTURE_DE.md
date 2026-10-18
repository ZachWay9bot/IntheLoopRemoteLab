# RemoteLab Architektur

## Ebenen

RemoteLab trennt vier Verantwortlichkeiten:

1. **Core**: Jobvalidierung, Dispatch, Audit und Policies.
2. **Transport**: Jobannahme und Ergebnisrueckgabe.
3. **Adapter**: geraetespezifische Protokolle und Hardwarefunktionen.
4. **Projektlogik**: Firmware, Tests und projektspezifische Auswertung.

Ein Transport kennt keine Hardwareprotokolle. Der Core importiert keine konkreten Geraeteadapter.

## Adapter-Laden

Adapter werden zur Laufzeit aus der Konfiguration geladen:

```json
{
  "module": "some.package.adapter",
  "class": "SomeAdapter",
  "enabled": true,
  "args": {}
}
```

Dadurch kann neue Hardware hinzugefuegt werden, ohne Core oder Queue-Protokoll anzupassen.

## Sicherheitsstufen

### Stufe A
Simulator und reine Offline-Tests.

### Stufe B
Echte Hardware mit passiven Operationen wie `identify` und `diagnose`.

### Stufe C
Explizit freigegebene Schreiboperationen fuer einen konkreten Adapter.

### Stufe D
Aktive Tests mit projektspezifischen Permit-, Lockout- und Preflight-Regeln.

Ein Adapter wird erst hochgestuft, wenn die vorherige Stufe regressionsgetestet ist.
