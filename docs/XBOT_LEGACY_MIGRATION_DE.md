# XBOT Legacy Migration

## Ausgangspunkt

Der produktive XBOT-RemoteLab-Agent funktioniert bereits mit realer Hardware. Er wird waehrend der RemoteLab-Core-Migration nicht ersetzt.

## Phase 1: Referenz sichern

Zu sichern sind:

- aktuell laufender Agent-Source
- aktive Konfiguration ohne Secrets im Repository
- Job-Protokoll
- Permit-/Expiry-Verhalten
- Lockout-Verhalten
- Flash-/Staging-/Identity-Pruefungen
- Diagnoseformate

## Phase 2: Read-only Adapter

Zuerst werden nur zwei Operationen portiert:

- `identify`
- `diagnose`

Der neue Adapter darf dabei weder flashen noch Motor-Kommandos senden.

## Phase 3: Mock-Serial

Der XBOT-Code wird gegen simulierte UART-Antworten getestet:

- gueltige Frames
- falsche Checksummen
- Timeouts
- abgeschnittene Frames
- falsche Firmware-Identitaet
- Lockout-/Permit-Zustaende

## Phase 4: echte Hardware read-only

Erst danach wird der neue Adapter parallel zum bestehenden Agenten auf echter Hardware getestet, ohne Schreiboperationen.

## Phase 5: Schreibpfad

Flashen und aktive Motor-Tests werden separat migriert. Sie benoetigen eigene Policies und explizite Freigaben.

## Wichtig

Bis Phase 4/5 erfolgreich abgeschlossen ist, bleibt der vorhandene produktive Agent der einzige Weg fuer XBOT-Flash- und Bench-Jobs.
