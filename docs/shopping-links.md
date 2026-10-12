# Два компактных списка: всё покупается заново

У владельца остался только лабораторный источник **12 V / 2 A**. Компьютера,
экрана, карт и любых компонентов v1 нет. Оба списка включают новую Zero 2 W
и новый экран 2.8″. Для стенда используется имеющийся БП; в кейсе — стандартный
вход Eurorack +12 V/GND и внутреннее преобразование в 5 V.

Ссылки — поиск, не проверенные карточки. Цены скриншотов v1 — исторические
ориентиры; текущие цены и наличие в магазинах не проверены. В актуальные
списки не входят настольный аудиоинтерфейс, RCA, Pi 4, дорогой HDMI-дисплей
или внешний блок питания. Готовые узлы означают маленькие внутренние платы.

## 1. Самостоятельная пайка входных каскадов

| Название | Кол-во | Поиск в РФ | Примечание |
|---|---:|---|---|
| PCM1808, отдельная микросхема АЦП | 1 | [Ozon](https://www.ozon.ru/search/?text=PCM1808) | Корпус и обвязку подтвердить до заказа |
| CMOS-осциллятор 12.288 MHz / 3.3 V, серия Abracon ASV | 1 | [Ozon](https://www.ozon.ru/search/?text=Abracon%20ASV%2012.288MHz%203.3V) | Готовый генератор, не двухвыводной кварц |
| Переходник корпуса АЦП на 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=TSSOP%20DIP%20%D0%BF%D0%B5%D1%80%D0%B5%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA) | Корпус выбирать после микросхемы |
| PC817C, DIP-4 | 2 | [Ozon](https://www.ozon.ru/search/?text=PC817C%20DIP4) | Триггер и запас; на скриншоте 150 ₽ за упаковку 10 шт. |
| MF-25 2.2 кОм, 0.25 W, 1% | 2 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B5%D0%B7%D0%B8%D1%81%D1%82%D0%BE%D1%80%202.2%D0%BA%D0%9E%D0%BC%200.25%D0%92%D1%82) | Кандидат для входа оптопары |
| 1N4148, DO-35 | 5 | [Ozon](https://www.ozon.ru/search/?text=1N4148%20DO35) | Защита светодиода оптопары и запас |
| Raspberry Pi Zero 2 W | 1 | [Ozon](https://www.ozon.ru/search/?text=Raspberry%20Pi%20Zero%202%20W) | 2 880 ₽ на скриншоте |
| TFT 2.8″ 320×240 SPI | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B4%D0%B8%D1%81%D0%BF%D0%BB%D0%B5%D0%B9%202.8%20320x240%20SPI) | 772 ₽ на скриншоте; контроллер и 60 FPS требуют проверки |
| Kingston Canvas Select Plus microSD 32 GB | 1 | [Ozon](https://www.ozon.ru/search/?text=Kingston%20Canvas%20Select%20Plus%2032GB) | Системная карта |
| Kingston Canvas Select Plus microSD 64 GB | 1 | [Ozon](https://www.ozon.ru/search/?text=Kingston%20Canvas%20Select%20Plus%2064GB) | Карта видео спереди; 441 ₽ показаны на скриншоте |
| USB 2.0 microSD-картридер | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20microSD%20%D0%BA%D0%B0%D1%80%D1%82%D1%80%D0%B8%D0%B4%D0%B5%D1%80) | Фронтальная карта контента |
| Micro-USB OTG → USB-A female | 1 | [Ozon](https://www.ozon.ru/search/?text=micro%20USB%20OTG%20USB%20A%20female) | Подключение картридера |
| Гребёнка 2×20 pin, 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B3%D1%80%D0%B5%D0%B1%D0%B5%D0%BD%D0%BA%D0%B0%202x20%202.54) | GPIO Zero |
| PJ-392, jack 3.5 мм | 2 | [Ozon](https://www.ozon.ru/search/?text=PJ-392) | На скриншоте 125 ₽ за два; детектор кабеля требует схемы |
| IDC BH-10 / DC3-10P, 2×5 | 1 | [Ozon](https://www.ozon.ru/search/?text=IDC%20BH-10%202x5) | 149 ₽ на скриншоте; разъём питания Eurorack |
| Кабель Eurorack 10→16 pin | 1 | [Ozon](https://www.ozon.ru/search/?text=Eurorack%2010%2016%20pin%20%D0%BA%D0%B0%D0%B1%D0%B5%D0%BB%D1%8C) | Покупается отдельно от разъёма |
| DC/DC модуль MP1584EN | 1 | [Ozon](https://www.ozon.ru/search/?text=MP1584EN) | 184 ₽ на скриншоте; питание вычислительной части 5 V |
| DC/DC 6–24 V→5 V с двумя USB-A | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%BF%D0%BE%D0%BD%D0%B8%D0%B6%D0%B0%D1%8E%D1%89%D0%B8%D0%B9%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%206%2024%D0%92%205%D0%92%20USB%203%D0%90) | 203 ₽ на скриншоте; отдельная зарядная ветвь |
| USB-A female панельный удлинитель | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20A%20female%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%83%D0%B4%D0%BB%D0%B8%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C) | 248 ₽ показаны на скриншоте |
| Mini-HDMI→HDMI короткий кабель / панельный удлинитель | 1 | [Ozon](https://www.ozon.ru/search/?text=mini%20HDMI%20HDMI%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%83%D0%B4%D0%BB%D0%B8%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C) | Внешний видеовыход Zero |
| 1N5822, 3 A / 40 V, DO-201 | 2 | [Ozon](https://www.ozon.ru/search/?text=1N5822%20DO201) | Кандидат защиты питания по схеме |
| MF-R110, PTC 1.1 A | 1 | [Ozon](https://www.ozon.ru/search/?text=MF-R110) | Предохранитель; не точный ограничитель USB-тока |
| 470 мкФ / 25 V и 100 нФ | по 2 / по 10 | [Ozon](https://www.ozon.ru/search/?text=%D0%BA%D0%BE%D0%BD%D0%B4%D0%B5%D0%BD%D1%81%D0%B0%D1%82%D0%BE%D1%80%D1%8B%20470%D0%BC%D0%BA%D0%A4%2025%D0%92%20100%D0%BD%D0%A4) | Запас развязки; обвязка уточняется |
| MF-25 100 кОм / 10 кОм / 1 кОм, 0.25 W, 1% | по 5 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B5%D0%B7%D0%B8%D1%81%D1%82%D0%BE%D1%80%D1%8B%20100%D0%BA%D0%9E%D0%BC%2010%D0%BA%D0%9E%D0%BC%201%D0%BA%D0%9E%D0%BC%200.25%D0%92%D1%82) | Прототипирование входного каскада |
| 1 мкФ плёночный / 10 мкФ 25 V / 1 нФ | по 2 | [Ozon](https://www.ozon.ru/search/?text=%D0%BA%D0%BE%D0%BD%D0%B4%D0%B5%D0%BD%D1%81%D0%B0%D1%82%D0%BE%D1%80%D1%8B%201%D0%BC%D0%BA%D0%A4%20%D0%BF%D0%BB%D0%B5%D0%BD%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%2010%D0%BC%D0%BA%D0%A4%2025%D0%92%201%D0%BD%D0%A4) | Прототипирование входного каскада |
| BAT54S | 2 | [Ozon](https://www.ozon.ru/search/?text=BAT54S) | Кандидат сигнальной защиты по схеме |
| Перфоплата FR-4, 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%BF%D0%B5%D1%80%D1%84%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0%20FR4%202.54) | Входная плата |
| МГТФ 0.2 мм² / медный провод 0.5 мм² | 2 м / 1 м | [Ozon](https://www.ozon.ru/search/?text=%D0%9C%D0%93%D0%A2%D0%A4%200.2%20%D0%BF%D1%80%D0%BE%D0%B2%D0%BE%D0%B4%200.5) | Сигналы / питание |
| Стойки, винты и гайки M3; термоусадка 2/3/5 мм | комплект | [Ozon](https://www.ozon.ru/search/?text=%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8%20M3%20%D1%82%D0%B5%D1%80%D0%BC%D0%BE%D1%83%D1%81%D0%B0%D0%B4%D0%BA%D0%B0) | Монтаж |
| Алюминиевый лист 2 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B0%D0%BB%D1%8E%D0%BC%D0%B8%D0%BD%D0%B8%D0%B5%D0%B2%D1%8B%D0%B9%20%D0%BB%D0%B8%D1%81%D1%82%202%20%D0%BC%D0%BC) | Лицевая панель по чертежу |

Силовая часть пока представлена дешёвыми DC/DC из v1. Для самостоятельного
регулятора из голой микросхемы нужна рассчитанная схема дросселя, диода,
конденсаторов и платы. Микросхема PCM1808, переходник и наборы пассивов также
не являются полностью утверждённым bare-chip BOM: корпус и схема ещё проверяются.

## 2. Маленькие внутренние готовые платы, меньше пайки

| Название | Кол-во | Поиск в РФ | Примечание |
|---|---:|---|---|
| PCM1808 I²S ADC board с генератором 12.288 MHz | 1 | [Ozon](https://www.ozon.ru/search/?text=PCM1808%20I2S%20ADC%2012.288MHz) | Маленькая внутренняя плата; MCLK, режим и драйвер ещё проверяются |
| PC817, одноканальная оптоизолированная плата | 1 | [Ozon](https://www.ozon.ru/search/?text=PC817%20%D0%BE%D0%BF%D1%82%D0%BE%D0%B8%D0%B7%D0%BE%D0%BB%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%201%20%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB) | Выход 3.3 V; вход и защита отрицательных импульсов требуют проверки |
| Raspberry Pi Zero 2 W | 1 | [Ozon](https://www.ozon.ru/search/?text=Raspberry%20Pi%20Zero%202%20W) | 2 880 ₽ на скриншоте |
| TFT 2.8″ 320×240 SPI | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B4%D0%B8%D1%81%D0%BF%D0%BB%D0%B5%D0%B9%202.8%20320x240%20SPI) | 772 ₽ на скриншоте; контроллер и 60 FPS требуют проверки |
| Kingston Canvas Select Plus microSD 32 GB | 1 | [Ozon](https://www.ozon.ru/search/?text=Kingston%20Canvas%20Select%20Plus%2032GB) | Системная карта |
| Kingston Canvas Select Plus microSD 64 GB | 1 | [Ozon](https://www.ozon.ru/search/?text=Kingston%20Canvas%20Select%20Plus%2064GB) | Карта видео спереди; 441 ₽ показаны на скриншоте |
| USB 2.0 microSD-картридер | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20microSD%20%D0%BA%D0%B0%D1%80%D1%82%D1%80%D0%B8%D0%B4%D0%B5%D1%80) | Фронтальная карта контента |
| Micro-USB OTG → USB-A female | 1 | [Ozon](https://www.ozon.ru/search/?text=micro%20USB%20OTG%20USB%20A%20female) | Подключение картридера |
| Гребёнка 2×20 pin, 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B3%D1%80%D0%B5%D0%B1%D0%B5%D0%BD%D0%BA%D0%B0%202x20%202.54) | GPIO Zero |
| PJ-392, jack 3.5 мм | 2 | [Ozon](https://www.ozon.ru/search/?text=PJ-392) | На скриншоте 125 ₽ за два; детектор кабеля требует схемы |
| IDC BH-10 / DC3-10P, 2×5 | 1 | [Ozon](https://www.ozon.ru/search/?text=IDC%20BH-10%202x5) | 149 ₽ на скриншоте; разъём питания Eurorack |
| Кабель Eurorack 10→16 pin | 1 | [Ozon](https://www.ozon.ru/search/?text=Eurorack%2010%2016%20pin%20%D0%BA%D0%B0%D0%B1%D0%B5%D0%BB%D1%8C) | Покупается отдельно от разъёма |
| DC/DC модуль MP1584EN | 1 | [Ozon](https://www.ozon.ru/search/?text=MP1584EN) | 184 ₽ на скриншоте; питание вычислительной части 5 V |
| DC/DC 6–24 V→5 V с двумя USB-A | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%BF%D0%BE%D0%BD%D0%B8%D0%B6%D0%B0%D1%8E%D1%89%D0%B8%D0%B9%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%206%2024%D0%92%205%D0%92%20USB%203%D0%90) | 203 ₽ на скриншоте; отдельная зарядная ветвь |
| USB-A female панельный удлинитель | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20A%20female%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%83%D0%B4%D0%BB%D0%B8%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C) | 248 ₽ показаны на скриншоте |
| Mini-HDMI→HDMI короткий кабель / панельный удлинитель | 1 | [Ozon](https://www.ozon.ru/search/?text=mini%20HDMI%20HDMI%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%83%D0%B4%D0%BB%D0%B8%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C) | Внешний видеовыход Zero |
| 1N5822, 3 A / 40 V, DO-201 | 2 | [Ozon](https://www.ozon.ru/search/?text=1N5822%20DO201) | Кандидат защиты питания по схеме |
| MF-R110, PTC 1.1 A | 1 | [Ozon](https://www.ozon.ru/search/?text=MF-R110) | Предохранитель; не точный ограничитель USB-тока |
| 470 мкФ / 25 V и 100 нФ | по 2 / по 10 | [Ozon](https://www.ozon.ru/search/?text=%D0%BA%D0%BE%D0%BD%D0%B4%D0%B5%D0%BD%D1%81%D0%B0%D1%82%D0%BE%D1%80%D1%8B%20470%D0%BC%D0%BA%D0%A4%2025%D0%92%20100%D0%BD%D0%A4) | Запас развязки; обвязка уточняется |
| MF-25 100 кОм / 10 кОм / 1 кОм, 0.25 W, 1% | по 5 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B5%D0%B7%D0%B8%D1%81%D1%82%D0%BE%D1%80%D1%8B%20100%D0%BA%D0%9E%D0%BC%2010%D0%BA%D0%9E%D0%BC%201%D0%BA%D0%9E%D0%BC%200.25%D0%92%D1%82) | Прототипирование входного каскада |
| 1 мкФ плёночный / 10 мкФ 25 V / 1 нФ | по 2 | [Ozon](https://www.ozon.ru/search/?text=%D0%BA%D0%BE%D0%BD%D0%B4%D0%B5%D0%BD%D1%81%D0%B0%D1%82%D0%BE%D1%80%D1%8B%201%D0%BC%D0%BA%D0%A4%20%D0%BF%D0%BB%D0%B5%D0%BD%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%2010%D0%BC%D0%BA%D0%A4%2025%D0%92%201%D0%BD%D0%A4) | Прототипирование входного каскада |
| BAT54S | 2 | [Ozon](https://www.ozon.ru/search/?text=BAT54S) | Кандидат сигнальной защиты по схеме |
| Перфоплата FR-4, 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%BF%D0%B5%D1%80%D1%84%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0%20FR4%202.54) | Входная плата |
| МГТФ 0.2 мм² / медный провод 0.5 мм² | 2 м / 1 м | [Ozon](https://www.ozon.ru/search/?text=%D0%9C%D0%93%D0%A2%D0%A4%200.2%20%D0%BF%D1%80%D0%BE%D0%B2%D0%BE%D0%B4%200.5) | Сигналы / питание |
| Стойки, винты и гайки M3; термоусадка 2/3/5 мм | комплект | [Ozon](https://www.ozon.ru/search/?text=%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8%20M3%20%D1%82%D0%B5%D1%80%D0%BC%D0%BE%D1%83%D1%81%D0%B0%D0%B4%D0%BA%D0%B0) | Монтаж |
| Алюминиевый лист 2 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B0%D0%BB%D1%8E%D0%BC%D0%B8%D0%BD%D0%B8%D0%B5%D0%B2%D1%8B%D0%B9%20%D0%BB%D0%B8%D1%81%D1%82%202%20%D0%BC%D0%BC) | Лицевая панель по чертежу |

Здесь меньше пайки АЦП, генератора и триггерного узла. Ослабление и защита
аудио, соединения питания и лицевая панель остаются. Arduino не требуется.

## Питание и незакрытые проверки

БП 12 V / 2 A уже есть. Нужен внутренний DC/DC 12→5 V для Pi и отдельной
зарядной ветви. Для этой архитектуры отрицательная шина питания не обязательна.
Схема рассчитает пиковый ток и защиту; надпись «3 A» на плате не доказывает
непрерывный ток. MF-R110 — предохранитель, а не точный ограничитель 1 A.

60 полных кадров/с на SPI-дисплее v1 не подтверждены: 320×240 RGB565 требует
73.728 Mbit/s без накладных расходов. Обвязка АЦП, Linux-драйвер, пороги триггера
и безопасное обнаружение кабеля ещё требуют схемы и проверки. Поэтому это
перечни для прототипа, не обещание готовой схемы и подтверждённых 60 FPS.
