# Названия и ссылки для закупки прототипа v2

Это предварительные списки для стенда, не окончательная ведомость компонентов готового устройства.
Российские магазины сейчас недоступны из облачной среды: CONNECT 403; дополнительный запрос сетевого доступа был отменён пользователем. Поэтому ссылки ниже — поиск по названиям, не проверенные карточки товара. Наличие, цены, продавцы и совместимость конкретных плат не проверены.

Точный bare-chip BOM аудио-АЦП, регулятора питания и детектора аудиоджека ещё требует схемы. Не выдавать подбор за полностью рассчитанную электронику. Модуль XL4015 ниже — временное питание стенда, а не удовлетворение требования спаять регулятор с нуля. Старый SPI-дисплей не подтверждён для 60 FPS. Вариант с HDMI также требует проверки конкретной модели 60 Hz.

## 1. Бюджетный стенд / самостоятельная сборка входов

| Деталь | Количество | Ссылка на поиск | Статус |
|---|---:|---|---|
| Raspberry Pi Zero 2 W | 1 | [Ozon](https://www.ozon.ru/search/?text=Raspberry%20Pi%20Zero%202%20W) | Испытательный бюджетный кандидат |
| Гребёнка 2×20 pin 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B3%D1%80%D0%B5%D0%B1%D0%B5%D0%BD%D0%BA%D0%B0%202x20%202.54) | Если GPIO не припаян |
| Существующий TFT 2.8″ 320×240 SPI | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B4%D0%B8%D1%81%D0%BF%D0%BB%D0%B5%D0%B9%202.8%20320x240%20SPI) | Контроллер v1 пока не подтверждён; 60 FPS не проверены |
| PCM1808 I²S АЦП | 1 | [Ozon](https://www.ozon.ru/search/?text=PCM1808) | Покупку голого чипа отложить до корпуса/обвязки/драйвера |
| CMOS-осциллятор 12.288 MHz 3.3 V, серия Abracon ASV | 1 | [Ozon](https://www.ozon.ru/search/?text=Abracon%20ASV%2012.288MHz%203.3V) | Не двухвыводной кварц; для отдельного АЦП |
| PC817C DIP-4 | 1–2 | [Ozon](https://www.ozon.ru/search/?text=PC817C%20DIP4) | 1 для CV; дополнительный только по схеме детектора |
| Резистор MF-25 2.2 кОм 1% | 2 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B5%D0%B7%D0%B8%D1%81%D1%82%D0%BE%D1%80%20MF-25%202.2%20%D0%BA%D0%9E%D0%BC) | Для прототипирования CV |
| Резисторы MF-25 10 кОм / 100 кОм / 1 кОм | по 5 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B5%D0%B7%D0%B8%D1%81%D1%82%D0%BE%D1%80%D1%8B%2010%D0%BA%D0%9E%D0%BC%20100%D0%BA%D0%9E%D0%BC%201%D0%BA%D0%9E%D0%BC%200.25%D0%92%D1%82) | Запас для входной платы; не окончательное количество |
| 1N4148 DO-35 | 5 | [Ozon](https://www.ozon.ru/search/?text=1N4148%20DO-35) | Защита LED оптопары/запас |
| BAT54S | 2 | [Ozon](https://www.ozon.ru/search/?text=BAT54S) | Кандидат защиты аудио, схема ещё рассчитывается |
| Конденсаторы 100 нФ / 1 нФ / плёночные 1 мкФ / электролиты 10 мкФ 25 V | набор | [Ozon](https://www.ozon.ru/search/?text=%D0%BA%D0%BE%D0%BD%D0%B4%D0%B5%D0%BD%D1%81%D0%B0%D1%82%D0%BE%D1%80%D1%8B%20100%D0%BD%D0%A4%201%D0%BD%D0%A4%201%D0%BC%D0%BA%D0%A4%2010%D0%BC%D0%BA%D0%A4) | Набор для прототипирования, не утверждённая обвязка АЦП |
| XL4015 DC/DC 5 A, регулируемый модуль | 1 | [Ozon](https://www.ozon.ru/search/?text=XL4015%205A) | Временное питание прототипа; реальный ток и нагрев проверить |
| USB-A DC/DC зарядный модуль 12→5 V | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20%D0%B7%D0%B0%D1%80%D1%8F%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%2012V%205V%20%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%BE%D0%BA%D0%B0) | Нужны согласование зарядки и ограничение тока |
| USB micro-B OTG → USB-A female | 1 | [Ozon](https://www.ozon.ru/search/?text=micro%20USB%20OTG%20USB%20A%20female) | Для USB-картридера Zero |
| mini-HDMI → HDMI, Type C → Type A | 1 | [Ozon](https://www.ozon.ru/search/?text=mini%20HDMI%20HDMI%20%D0%BA%D0%BE%D1%80%D0%BE%D1%82%D0%BA%D0%B8%D0%B9%20%D0%BA%D0%B0%D0%B1%D0%B5%D0%BB%D1%8C) | Именно mini, не micro |
| Радиатор Raspberry Pi Zero | 1 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B0%D0%B4%D0%B8%D0%B0%D1%82%D0%BE%D1%80%20Raspberry%20Pi%20Zero) | Размер по компоновке |

## 2. Готовые узлы / минимум пайки

| Деталь | Количество | Ссылка на поиск | Статус |
|---|---:|---|---|
| Raspberry Pi 4 Model B 2 GB | 1 | [Ozon](https://www.ozon.ru/search/?text=Raspberry%20Pi%204%20Model%20B%202GB) | Больше запаса; не обязательная замена до тестов |
| Waveshare 4inch HDMI LCD, семейство | 1 | [Ozon](https://www.ozon.ru/search/?text=Waveshare%204inch%20HDMI%20LCD) | Точную ревизию/матрицу 60 Hz ещё проверить; не утверждён к покупке |
| Behringer U-CONTROL UCA202 или UCA222 | 1 | [Ozon](https://www.ozon.ru/search/?text=Behringer%20UCA202%20UCA222) | USB RCA line-in; ослабление Eurorack всё равно требуется |
| Готовый оптоизолированный вход PC817, один канал | 1 | [Ozon](https://www.ozon.ru/search/?text=PC817%20%D0%BE%D0%BF%D1%82%D0%BE%D0%B8%D0%B7%D0%BE%D0%BB%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%201%20%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB) | Выход 3.3 V, вход 5–12 V и защита отрицательной полярности должны быть проверены |
| DROK DC/DC 12→5 V 5 A | 1 | [Ozon](https://www.ozon.ru/search/?text=DROK%2012V%205V%205A) | Выбирать по подтверждённому непрерывному току, не надписи |
| Готовый USB-A зарядный DC/DC 12→5 V с ограничением тока | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20%D0%B7%D0%B0%D1%80%D1%8F%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%2012V%205V%20%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%BE%D0%BA%D0%B0) | Отдельно от USB-портов данных Pi |
| micro-HDMI → HDMI, Type D → Type A | 2 | [Ozon](https://www.ozon.ru/search/?text=micro%20HDMI%20HDMI%20Raspberry%20Pi%204) | Встроенный экран + внешний панельный выход |
| Радиатор Raspberry Pi 4 | 1 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B0%D0%B4%D0%B8%D0%B0%D1%82%D0%BE%D1%80%20Raspberry%20Pi%204) | Вентилятор по результатам температуры |
| Стерео RCA-кабель / гнездо для UCA202 | 1 | [Ozon](https://www.ozon.ru/search/?text=RCA%20%D0%BA%D0%B0%D0%B1%D0%B5%D0%BB%D1%8C%20%D0%BA%D0%BE%D1%80%D0%BE%D1%82%D0%BA%D0%B8%D0%B9) | Вход через рассчитанный делитель и защиту |
| MF-25 100 кОм и 10 кОм | по 2 | [Ozon](https://www.ozon.ru/search/?text=%D1%80%D0%B5%D0%B7%D0%B8%D1%81%D1%82%D0%BE%D1%80%20100%D0%BA%D0%9E%D0%BC%2010%D0%BA%D0%9E%D0%BC%200.25%D0%92%D1%82) | Заготовка делителя, не полная защита входа |

## Добавить в каждый из двух списков

| Деталь | Количество | Ссылка на поиск | Статус |
|---|---:|---|---|
| Kingston Canvas Select Plus microSD 32 GB A1 | 1 | [Ozon](https://www.ozon.ru/search/?text=Kingston%20Canvas%20Select%20Plus%2032GB) | ОС |
| Kingston Canvas Select Plus microSD 64 GB A1 | 1 | [Ozon](https://www.ozon.ru/search/?text=Kingston%20Canvas%20Select%20Plus%2064GB) | Видео |
| USB 2.0 microSD-картридер | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20microSD%20%D0%BA%D0%B0%D1%80%D1%82%D1%80%D0%B8%D0%B4%D0%B5%D1%80) | Для карты на лицевой панели |
| PJ-392, jack 3.5 мм панельный | 2 | [Ozon](https://www.ozon.ru/search/?text=PJ-392) | Проверить контакты; switch не подключать прямо к GPIO |
| IDC BH-10 / DC3-10P, 2×5, 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=IDC%20BH-10%202x5) | Разъём питания Eurorack |
| Кабель Eurorack 10→16 pin | 1 | [Ozon](https://www.ozon.ru/search/?text=Eurorack%2010%2016%20pin%20%D0%BA%D0%B0%D0%B1%D0%B5%D0%BB%D1%8C) | Питание |
| USB-A female панельный удлинитель | 1 | [Ozon](https://www.ozon.ru/search/?text=USB%20A%20female%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%83%D0%B4%D0%BB%D0%B8%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C) | Зарядный порт |
| HDMI female панельное гнездо | 1 | [Ozon](https://www.ozon.ru/search/?text=HDMI%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%83%D0%B4%D0%BB%D0%B8%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C) | Внешний видеовыход |
| Перфоплата FR-4 2.54 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%BF%D0%B5%D1%80%D1%84%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0%20FR4%202.54) | Входная плата |
| Провод МГТФ 0.2 мм² и монтажный 0.5 мм² | 2 м + 1 м | [Ozon](https://www.ozon.ru/search/?text=%D0%9C%D0%93%D0%A2%D0%A4%200.2%20%D0%BC%D0%BE%D0%BD%D1%82%D0%B0%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%BF%D1%80%D0%BE%D0%B2%D0%BE%D0%B4%200.5) | Сигналы и питание |
| Стойки M3, винты M3, гайки, шайбы | комплект | [Ozon](https://www.ozon.ru/search/?text=%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8%20M3%20%D0%BD%D0%B0%D0%B1%D0%BE%D1%80) | Длины после компоновки |
| Термоусадка 2/3/5 мм | комплект | [Ozon](https://www.ozon.ru/search/?text=%D1%82%D0%B5%D1%80%D0%BC%D0%BE%D1%83%D1%81%D0%B0%D0%B4%D0%BA%D0%B0%202%203%205%20%D0%BC%D0%BC) | Изоляция |
| Алюминиевый лист 2 мм | 1 | [Ozon](https://www.ozon.ru/search/?text=%D0%B0%D0%BB%D1%8E%D0%BC%D0%B8%D0%BD%D0%B8%D0%B5%D0%B2%D1%8B%D0%B9%20%D0%BB%D0%B8%D1%81%D1%82%202%20%D0%BC%D0%BC) | Панель по чертежу |

Дополнительные российские поиски: [Avito: Zero 2 W](https://www.avito.ru/all?q=Raspberry%20Pi%20Zero%202%20W), [Avito: Pi 4](https://www.avito.ru/all?q=Raspberry%20Pi%204), [Чип и Дип: PCM1808](https://www.chipdip.ru/search?searchtext=PCM1808), [Чип и Дип: PC817C](https://www.chipdip.ru/search?searchtext=PC817C).

Штыревой контакт jack обычно не является изолированным детектором штекера; нельзя давать готовую распайку GPIO только по названию PJ-392. Для схемы нужны корпус/плата АЦП, допустимый ток блока питания кейса, контроллер экрана и фактические уровни сигналов.
