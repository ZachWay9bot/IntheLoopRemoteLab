# RemoteLab Architektur

## 1. Trennung der Verantwortlichkeiten

RemoteLab wird in vier Ebenen geteilt:

1. **Core**: Jobvalidierung, Dispatch, Audit, Policies.
2. **Transport**: Woher Jobs kommen und wohin Ergebnisse gehen.
3. **Adapter**: Geraetespezifische Protokolle und Diagnose.
4. **Projektlogik**: Firmware, Tests und projektspezifische Auswertung.

Hardwareprotokolle duerfen nicht in den Transport wandern. GitHub-Code darf nicht wissen, wie ein XBOT geflasht wird.

## 2. Projekt-Repository

`ZachWay9bot/RemoteLab` ist Source-/Dokumentations-/Release-Repository.

Es ist **keine Job-Queue**.

## 3. Bestehendes XBOT

Der produktive XBOT-Agent, sein Queue-Repository und sein bestehender Jobkanal bleiben unveraendert.

Der Adapter `xbot_legacy` ist in v0.4 nur eine Migrationsgrenze. Er besitzt keinen COM-Zugriff und keine Flashfunktion.

## 4. Sicherheitsstufen

### Stufe A
Simulator, reine Offline-Tests.

### Stufe B
Echte Hardware, nur `identify` und `diagnose`.

### Stufe C
Explizite Schreibfreigabe fuer einen konkreten Adapter.

### Stufe D
Aktive Tests mit zusaetzlichen Permit-/Lockout-Regeln.

Ein Adapter darf erst hochgestuft werden, wenn die vorherige Stufe regressionsgetestet ist.
