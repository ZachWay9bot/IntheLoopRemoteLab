# G30D Gen1 / DeltaESC: erster Hardwarekontakt (nur lesend)

**Wichtig**: Der XBOT-Agent ist kein universeller DeltaESC-Agent. Alte FOxx-XBOT-Statusabfragen nicht als G30D-DeltaESC-Status interpretieren. Kein ST-Link und kein Flash-/IAP-Experiment.

## Sofort lokal, ohne GitHub-Token und ohne Queue

Im Installationsordner (ZIP entpackt genügt, `git pull` ist nicht erforderlich):

```cmd
py -m pip install -e ".[serial]"
py -c "from remotelab.adapters.deltaesc import DeltaEscReadOnlyAdapter; print(DeltaEscReadOnlyAdapter(port='COM9').identify())"
```

Die zweite Zeile öffnet die angegebene COM-Schnittstelle einmal, sendet genau einen G30-Ninebot READ auf Register `0x10` und beendet die Sitzung. Keine Motorfreigabe, kein Gas, kein Flash, kein IAP-Reset und keine Schreiboperation.

`COM9` nur verwenden, wenn dies der **tatsächliche neue** USB-UART-Anschluss ist. Die G30-Yellow-Wire-UART muss elektrisch korrekt als Halbduplex/Open-Drain beschaltet sein. Kein direktes Push-Pull-TX auf dieselbe Leitung legen.

Ergebnisse:
- `is_deltaesc=True`: App-Identifikation `DELTAESC-G30D0` gelesen. Nur danach dürfen zur bestehenden DeltaESC-App passende weitere **Lese**register diagnostiziert werden.
- Anderer `identity`: zunächst tatsächlich vorhandene Stock-/Fremdfirmware zuordnen. Nicht blind DeltaESC-Diagnoseregister auf fremden Protokollen ausprobieren.
- `TimeoutError`: Kein verifiziertes Antworttelegramm, **nicht** gleichbedeutend mit Bootloader-/Flashdefekt. Port, Hardwarepegel und Protokollzuordnung prüfen.
- `PermissionError` zur GitHub-Queue: lokale Identifikation braucht keine GitHub-Queue.

## RemoteLab-Queue separat, erst mit privatem Relay-Repository

Der generische Agent `GitHubIssueClient.validate()` lehnt öffentliche Queue-Repositories ausdrücklich ab. Das öffentliche Repository `ZachWay9bot/DeltaESC-G30D` und sein Issue #22 sind **kein** funktionierender Agent-Relay. Die erste dort sichtbare Kommandozeile ist eine Dokumentation, kein Hardwareergebnis.

Das Beispiel `examples/remotelab.deltaesc.g30.queue.example.json` enthält deshalb bewusst `OWNER/PRIVATE_G30_QUEUE_REPO` und ist **nicht sofort als echte Queue ausführbar**. Erst nach Einrichtung eines ausdrücklich dafür vorgesehenen **privaten** Repos und Issues müssen `repo`, `issue`, `operator` und der COM-Port auf die tatsächlichen Werte gesetzt werden. Keinesfalls vorhandenes privates `xbot-remote-lab` als neue G30-Queue zweckentfremden.

Der einmalige lokale Lesebefehl ist bis dahin der technisch kürzeste Weg. Alte XBOT-Queue und die Firmware-Recovery-Pfade bleiben unberührt.
