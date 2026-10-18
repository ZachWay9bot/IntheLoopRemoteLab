# Neues Geraet an RemoteLab anbinden

## Minimaler Adapter

Ein neuer Adapter erbt von `DeviceAdapter` und implementiert:

```python
class MyAdapter(DeviceAdapter):
    name = "my_device"

    def identify(self) -> dict:
        ...

    def diagnose(self) -> dict:
        ...
```

Damit kann das Geraet im ersten Schritt nur gelesen werden.

## Schreiboperationen

`flash()` und `run_test()` bleiben in der Basisklasse gesperrt. Ein Projekt darf diese Funktionen erst ueberschreiben, wenn:

1. Recovery geklaert ist
2. Image-/Identity-Pruefung existiert
3. Offline-/Mock-Tests vorhanden sind
4. Hardware-Preflight definiert ist
5. Audit und Fehlerpfad getestet sind

## Transport unabhaengig halten

Ein Adapter darf nicht voraussetzen, dass Jobs ueber GitHub kommen. Derselbe Adapter soll spaeter mit lokalem Transport, GitHub-Issue-Transport oder anderer Steuerung funktionieren.

## Beispiel-Ziele

- ESP32 ueber esptool
- STM32 ueber ST-Link oder eigenen Bootloader
- RP2040 ueber UF2/PicoProbe
- serielle Messgeraete
- programmierbare Netzteile
- Oszilloskope mit Remote-Schnittstelle
