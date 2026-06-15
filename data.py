
SERVICES = [
    {'id': 'haircut',  'name': 'Стрижка',     'price': '1500 руб.', 'duration': '60 мин.'},
    {'id': 'coloring', 'name': 'Окрашивание', 'price': '3500 руб.', 'duration': '120 мин.'},
    {'id': 'manicure', 'name': 'Маникюр',     'price': '1200 руб.', 'duration': '60 мин.'},
    {'id': 'massage',  'name': 'Массаж',      'price': '2000 руб.', 'duration': '60 мин.'},
]

# Доступные даты (в реальном проекте — из базы данных)
AVAILABLE_DATES = [
    '2026-06-01', '2026-06-02', '2026-06-03',
    '2026-06-04', '2026-06-05',
]

# Доступные временные слоты
AVAILABLE_TIMES = ['10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00']

def get_service_by_id(service_id: str) -> dict | None:
    return next((s for s in SERVICES if s['id'] == service_id), None)

def format_date(date_str: str) -> str:
    """Преобразует '2026-06-01' в '01.06.2026 (Пн)'"""
    from datetime import datetime
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    d = datetime.strptime(date_str, '%Y-%m-%d')
    return f"{d.strftime('%d.%m.%Y')} ({days[d.weekday()]})"