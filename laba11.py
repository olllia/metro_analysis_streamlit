import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Загрузка данных
@st.cache
def load_data():
    file_path = "metro_traffic.csv"  # Файл с данными о пассажиропотоке
    data = pd.read_csv(file_path, delimiter=";")
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]  # Удаляем пустые столбцы
    return data

# Загрузка данных с координатами
@st.cache
def load_coords():
    coords_path = "moscow_underground_coords.csv"  # Файл с данными о координатах станций
    coords = pd.read_csv(coords_path)
    return coords

# Цвета линий
line_colors = {
    'Сокольническая линия': '#EF161E',
    'Замоскворецкая линия': '#2DBE2C',
    'Арбатско-Покровская линия': '#0078BE',
    'Филёвская линия': '#00BFFF',
    'Кольцевая линия': '#8D5B2D',
    'Калужско-Рижская линия': '#ED9121',
    'Таганско-Краснопресненская линия': '#800080',
    'Калининская линия': '#FFD702',
    'Солнцевская линия': '#FFD702',
    'Калининско-Солнцевская линия': '#FFD702',
    'Серпуховско-Тимирязевская линия': '#999999',
    'Люблинско-Дмитровская линия': '#99CC00',
    'Большая кольцевая линия': '#82C0C0',
    'Каховская линия': '#231F20',
    'Бутовская линия': '#A1B3D4',
    'Московский монорельс': '#B9C8E7',
    'Московское центральное кольцо': '#FFC6C2',
    'Некрасовская линия': '#DE64A1',
    'Троицкая линия': '#0f4343'
}

# Основной код Streamlit
st.title("Анализ пассажиропотока Московского метрополитена")

# Загрузка данных
data = load_data()
coords = load_coords()

# Фильтры
st.sidebar.header("Фильтры")
selected_line = st.sidebar.selectbox("Выберите линию метро", ["Все линии"] + list(data['Line'].unique()))
selected_year = st.sidebar.selectbox("Выберите год", ["Все годы"] + sorted(data['Year'].unique()))
selected_quarter = st.sidebar.selectbox("Выберите квартал", ["Все кварталы"] + list(data['Quarter'].unique()))

# Сброс фильтров
reset_filters = st.sidebar.button("Сбросить фильтры")

if reset_filters:
    selected_line = "Все линии"
    selected_year = "Все годы"
    selected_quarter = "Все кварталы"

# Применяем фильтры
filtered_data = data.copy()

if selected_line != "Все линии":
    filtered_data = filtered_data[filtered_data['Line'] == selected_line]

if selected_year != "Все годы":
    filtered_data = filtered_data[filtered_data['Year'] == selected_year]

if selected_quarter != "Все кварталы":
    filtered_data = filtered_data[filtered_data['Quarter'] == selected_quarter]

# Преобразуем значения в числовой формат
filtered_data['IncomingPassengers'] = pd.to_numeric(filtered_data['IncomingPassengers'], errors='coerce')
filtered_data['OutgoingPassengers'] = pd.to_numeric(filtered_data['OutgoingPassengers'], errors='coerce')

# Проверка данных
if not filtered_data.empty:
    # Общие данные
    incoming_total = filtered_data['IncomingPassengers'].sum()
    outgoing_total = filtered_data['OutgoingPassengers'].sum()

    # Вывод данных в виде плашек
    st.metric("Количество входов пассажиров:", f"{incoming_total:,}")
    st.metric("Количество выходов пассажиров:", f"{outgoing_total:,}")

    # График
    fig, ax = plt.subplots(figsize=(10, 6))
    stations = filtered_data['NameOfStation']
    ax.bar(stations, filtered_data['IncomingPassengers'], label="Входы", color="blue", alpha=0.7)
    ax.bar(stations, filtered_data['OutgoingPassengers'], label="Выходы", color="green", alpha=0.7, bottom=filtered_data['IncomingPassengers'])
    ax.set_title(f"Пассажиропоток на линии {selected_line} ({selected_year}, {selected_quarter})")
    ax.set_ylabel("Количество пассажиров")
    ax.set_xticklabels(stations, rotation=45, ha='right')
    ax.legend()
    st.pyplot(fig)

    # Строим карту
    if 'lat' in coords.columns and 'long' in coords.columns:
        st.write(f"Отображаем станции на карте для линии {selected_line}")

        # Фильтруем координаты станций по выбранной линии
        if selected_line != "Все линии":
            line_coords = coords[coords['Линия'] == selected_line]
        else:
            line_coords = coords

        map_center = [55.7558, 37.6173]  # Координаты центра Москвы
        m = folium.Map(location=map_center, zoom_start=10)

        # Группировка по линиям
        group = folium.FeatureGroup(name=selected_line)

        # Добавление маркеров для каждой станции
        for _, row in line_coords.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['long']],
                radius=8,
                color=line_colors.get(row['Линия'], 'black'),
                fill=True,
                fill_color=line_colors.get(row['Линия'], 'black'),
                fill_opacity=1,
                tooltip=row['Название']
            ).add_to(group)

        # Добавление линий
        line_points = line_coords[['lat', 'long']].values
        if selected_line in ['Кольцевая линия', 'Большая кольцевая линия', 'Московское центральное кольцо']:
            line_points = list(line_points)
            line_points.append(line_points[0])  # Замкнуть круг для кольцевых линий
        folium.PolyLine(line_points, color=line_colors.get(selected_line, 'black'), weight=5).add_to(group)

        group.add_to(m)
        folium.LayerControl().add_to(m)
        st_folium(m, width=700, height=500)

    # Выводим таблицу с отфильтрованными данными
    st.write("Таблица с отфильтрованными данными:")
    st.dataframe(filtered_data)

else:
    st.write("Нет данных для отображения. Пожалуйста, примените фильтры.")
    st.write("Полные данные:")
    st.dataframe(data)
