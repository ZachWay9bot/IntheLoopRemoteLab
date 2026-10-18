# GitHub Queue und Fine-grained PAT

## Projekt-Repository

Das RemoteLab-Repository enthaelt Source, Dokumentation, Tests und Releases.

Eine Runtime-Queue ist davon getrennt.

## Queue-Repository

Fuer einen GitHub-Issue-Transport wird ein separates privates Repository verwendet:

1. privates Repository erstellen
2. ein offenes Issue als Queue anlegen
3. Fine-grained PAT erstellen
4. bei Repository access nur das Queue-Repository auswaehlen
5. Repository Permissions:
   - **Issues: Read and write**
   - **Contents: Read-only**, falls Artefakte aus dem Queue-Repository geladen werden
   - **Metadata: Read**
6. keine unnoetigen Administrations- oder Workflow-Rechte vergeben

## Runtime-Credential

RemoteLab liest den Token aus:

- Umgebungsvariable `REMOTELAB_GITHUB_TOKEN`, oder
- Credential-Eintrag `RemoteLab-Core / github-token`

## Trennung

Die Queue transportiert Jobs und Ergebnisse. Sourcecode, Releases und Entwicklungsstand bleiben im Projekt-Repository.
