# Neues Geraet an RemoteLab anbinden

## Adapter implementieren

Ein Adapter erbt von `DeviceAdapter`:

```python
from remotelab.adapters.base import DeviceAdapter

class MyAdapter(DeviceAdapter):
    name = "my_device"

    def identify(self) -> dict:
        ...

    def diagnose(self) -> dict:
        ...
```

## Konfiguration

Der Core braucht keine Codeaenderung:

```json
{
  "module": "my_package.my_adapter",
  "class": "MyAdapter",
  "enabled": true,
  "args": {
    "port": "COM4"
  }
}
```

## Schreiboperationen

`flash()` und `run_test()` bleiben in der Basisklasse gesperrt, bis der Adapter einen validierten Schreibpfad besitzt.

Vor einer Freigabe sollten mindestens vorhanden sein:

1. Recovery-Strategie
2. Image- oder Identity-Pruefung
3. Offline- und Mock-Tests
4. Hardware-Preflight
5. Audit- und Fehlerpfad
6. klare Grenzen fuer aktive Operationen

## Transport unabhaengig halten

Ein Adapter kennt keinen Queue-Anbieter. Derselbe Adapter muss mit lokalem Transport, GitHub-Issue-Transport oder spaeteren Transporten funktionieren koennen.
