# Project-Steam

Dit project is bedoeld de gebruikerservaring op het Steam-platform te verbeteren  door extra optie toevoegen en een Rasberry Pi PICO. Ons doel is om vrienden te kunnen opzoeken en om games te kunnen zoeken en in een lijst zien buiten Steam. Hiernaast zijn er ook extra optie zo als laat indicatie met Neopixels en een lcd-scherm. Er zijn ook statistiekalgoritmen, zoekalgoritmen, sorteeralgoritmen toegevoegd.

## Installation

Om de applicatie op te kunnen draaien moet er eerst de requirements worden geïnstalleerd.
```bash
  pip install -r requirements.txt
```
Om de applicatie volledig te laten werken moet er een steam api-key worden toegevoegd.
Dit kan worden gedaan door op deze link te klikken [Steam API-KEY](https://steamcommunity.com/dev/apikey).

Als u de steam API-KEY heb gekregen dan moet u eerst nog een .env bestand aan maken met er in `STEAM_API_KEY = <Uw Steam API-KEY>`


Hier na kan deze command worden uitgevoerd en het programma wordt op gestart.
```bash
  python main.py
```
## Raspberry pi PICO
Als je de Raspberry pi PICO wilt laten werken, moet je drie bestanden uploaden naar de PICO. Deze bestanden zijn te vinden in de map **RPICO**. Hieronder wordt ook uitgelegd hoe de kabels moeten worden aangesloten. Dit kan je op een breadboard doen.


|       Neopixel    |       Pin         |
| ----------------- | ----------------- |
| VCC               |  V3               |
| In                |  GPIO 13          |
| GND               |  GND              |

|  LCD 16x2 (I2C)   |       Pin         |
| ----------------- | ----------------- |
| GND               |  GND              |
| VCC               |  5V (VBUS)        |
| SDA               |  GPIO 8           |
| SCL               |  GPIO 9           |

![App Screenshot](https://i.imgur.com/DPaY8Pg.png)

## Screenshots

![App Screenshot](https://i.imgur.com/SBRY015.png)
![App Screenshot](https://i.imgur.com/XVvWLIw.png)
![App Screenshot](https://i.imgur.com/yo6cmes.png)
![App Screenshot](https://i.imgur.com/pHFD8ph.png)


## Authors

- [@Renzo](https://github.com/Nuboctane)
- [@Paco](https://github.com/LordPoc)
- [@Julian](https://github.com/JulianNL030)
- [@Ivan](https://github.com/SuperIvan525)
- [@Sofyan](https://github.com/soef0297)