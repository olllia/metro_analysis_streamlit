# Анализ пассажиропотока Московского метрополитена (2021-2024)

## Описание проекта

Данный проект предоставляет интерактивное приложение на базе **Streamlit** для анализа данных о пассажиропотоке Московского метрополитена. Пользователь может применять фильтры для выбора интересующих его данных, а также просматривать визуализацию на карте и графиках.

## Содержимое репозитория

- **`laba11.py`**: Основной скрипт приложения
- **`metro_traffic.csv`**: Данные о пассажиропотоке Московского метро. Колонки:
  - `NameOfStation`: Название станции
  - `Line`: Линия метро
  - `Year`: Год
  - `Quarter`: Квартал
  - `IncomingPassengers`: Количество входящих пассажиров
  - `OutgoingPassengers`: Количество выходящих пассажиров
  - `global_id`: Идентификатор
- **`moscow_underground_coords.csv`**: Данные о географических координатах станций. Колонки:
  - `Название`: Название станции
  - `Линия`: Линия метро
  - `lat`: Широта
  - `long`: Долгота

## Основные возможности приложения

1. **Фильтры для анализа данных**:
   - Выбор линии метро
   - Выбор года
   - Выбор квартала
2. **Отображение ключевых метрик**:
   - Общее количество входящих пассажиров
   - Общее количество выходящих пассажиров
3. **Визуализация данных**:
   - Столбчатые графики пассажиропотока по станциям
   - Интерактивная карта с отображением станций и линий метро
4. **Просмотр данных**:
   - Таблица с исходными и отфильтрованными данными

## Установка и запуск

### 1. Установка зависимостей
Создайте виртуальное окружение (рекомендуется) и установите необходимые зависимости:

```bash
pip install -r requirements.txt
```

### 2. Запуск приложения
Для запуска приложения выполните:

```bash
streamlit run laba11.py
```

Приложение будет доступно в браузере по адресу: `http://localhost:8501`.

## Зависимости

Проект использует следующие библиотеки:

- `streamlit`: для создания веб-интерфейса
- `pandas`: для работы с данными
- `folium`: для визуализации карты
- `streamlit-folium`: для интеграции карт в приложение Streamlit
- `matplotlib`: для построения графиков

## Использование приложения

1. Запустите приложение
2. Настройте фильтры на боковой панели для выбора данных по линии, году и кварталу
3. Просмотрите ключевые метрики пассажиропотока
4. Изучите визуализацию на графике и карте
5. Ознакомьтесь с данными в таблице

## Примечания

- **Кэширование данных**: Для ускорения загрузки данных используется декоратор `@st.cache`
- **Цвета линий метро**: Цвета соответствуют официальным цветам линий Московского метрополитена
