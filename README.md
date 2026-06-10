# 3RRS-Modell
Dieses Repo enthält die Software und das CAD-Modell zum 3RRS-Modell.
<img width="2558" height="1817" alt="3RRS" src="https://github.com/user-attachments/assets/1ed54f76-7991-40f1-b969-7a074ef759af" />
Im folgenden wird die Installation beschrieben.

## Installation 

### Voraussetungen (falls nicht bereits installiert)
- [Python](https://www.python.org/downloads/) ACHTUNG: Maintenance status security und nicht bugfix, damit die Kompatibilität zu den nötigen Bibliotheken gewährleistet ist. 
- [Python IDE](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/downloads)
- [Arduino Nano Treiber](https://download.bastelgarage.ch/?dir=.%2FCH340Treiber)

### Repository
Der Ordner mit allen Unterlagen kann mit folgendem Codezeilenbefehl kopiert werden.
```
git clone https://github.com/danielfhnw/3rrs
```
Alternativ kann auch GitHub Desktop oder die GitHub-Integration im VS Code verwendet werden.
Um in den 3rrs Ordner zu gelangen kann folgende Kommandozeileneingabe verwendet werden.
```
cd 3rrs
```

### Virtual Environement
Im 3rrs-Ordner soll nun ein virtuelles Environement erstellt werden. Dies dient dazu, dass alle Bibliotheken miteinander kompatibel bleiben und nicht durch Updates geändert werden.
```
python -m venv .venv
```
Um die nötigen Bibliotheken in das virtuelle Environement zu laden muss es zuerst aktiviert werden. Dies erfolgt über das activate-Script.
```
.venv\Scripts\activate.bat
```
Sobald das Environement aktiviert ist erscheint `(.venv)` vor dem Pfad.
Anschliessend müssen die nötigen Bibliotheken heruntergeladen werden. Dazu wird der folgende Befehl verwendet.
```
pip install -r requirements.txt
```
Sobald alles erfolgreich installiert wurde, ist das virtuelle Environement bereit.

### Environement Variable
Damit nicht in jedem Skript die COM-Ports angepasst werden müssen, werden in diesem Projekt Environement Variablen zur Speicherung verwendet. Dies hat den Vorteil, dass die Skripts updated werden können, ohne dass die COM-Ports überschrieben werden. Damit dies funktioniert muss im 3rrs-Ordner ein File erstellt werden mit dem Namen `.env`. Dies kann mit dem folgenden Befehl erstellt werden.
```
notepad .env
```
Diese Datei muss mit folgendem Inhalt gefüllt werden.
```
COM_PORT_MOTOR=COM80
COM_PORT_IMU=COM81
OFFSET_SERVO_1=2816
OFFSET_SERVO_2=1255
OFFSET_SERVO_3=1662
```
Dabei muss der COM-Port für den Seeeduino und das Motorboard entsprechend angepasst werden. Die  Servo-Offsets sind an der jeweiligen Hardware zu bestimmen und da sie von Modell zu Modell verschieden sind, ebenfalls als Umgebungsvariabeln abgelegt.

## BOM
- 3x https://www.waveshare.com/wiki/ST3215_Servo
- 1x https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A)?srsltid=AfmBOopFUcmjpQCkET0qZIshGwUuTE_U6VoR4gDlRMLTdKMSerG3c7sd
- 1x https://wiki.seeedstudio.com/Seeeduino_Lotus/
- 1x https://wiki.seeedstudio.com/Grove-6-Axis_Accelerometer&Gyroscope_BMI088/
