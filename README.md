# AFD Pump Controller для Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

Интеграция для управления **AFD Pump Controller** – автоматическим дозатором удобрений на базе ESP8266.

## Возможности

- Управление насосом (выключатель)
- Датчик уровня жидкости
- Датчик откалиброванного расхода (мл/с)
- Калибровка: запуск/остановка, установка целевого объёма
- Дозирование: установка объёма, запуск/остановка
- Управление яркостью встроенного светодиода
- Управление расписанием через сервисы

## Установка

1. Добавьте репозиторий в HACS как пользовательский.
2. Нажмите "Download" и перезагрузите Home Assistant.
3. В разделе "Интеграции" нажмите "Add Integration" и найдите **AFD Pump Controller**.
4. Введите MQTT префикс топиков (по умолчанию `AFD`).

## Конфигурация

Интеграция использует существующую MQTT интеграцию Home Assistant. Убедитесь, что ваш MQTT брокер настроен.

После добавления устройства в Home Assistant появятся сущности:
- `switch.afd_pump` – включение/отключение насоса
- `binary_sensor.afd_pump_water_level` – уровень жидкости (LOW = проблема)
- `sensor.afd_pump_flow_rate` – расход (мл/с)
- `sensor.afd_pump_calibration_state` – статус калибровки
- `sensor.afd_pump_dispense_volume` – текущий объём дозирования
- `sensor.afd_pump_led_brightness` – яркость LED
- `number.afd_pump_set_dispense_volume` – изменение объёма дозирования
- `number.afd_pump_calibration_target_volume` – изменение целевого объёма калибровки
- `number.afd_pump_led_brightness_set` – изменение яркости
- `button.afd_pump_start_calibration`, `...stop_calibration`
- `button.afd_pump_run_dispense`, `...stop_dispense`

## Сервисы

Дополнительные сервисы (вызываются через Developer Tools → Services):

- `afd_pump.calibrate_start`
- `afd_pump.calibrate_stop`
- `afd_pump.calibrate_set_volume`
- `afd_pump.dispense_run`
- `afd_pump.dispense_stop`
- `afd_pump.dispense_set_volume`
- `afd_pump.set_brightness`
- `afd_pump.schedule_add`
- `afd_pump.schedule_remove`
- `afd_pump.schedule_update`
- `afd_pump.schedule_get`

## Поддержка

Создавайте [Issues](https://github.com/your-username/afd-pump-ha/issues) на GitHub.

## Лицензия

MIT