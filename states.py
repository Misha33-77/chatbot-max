
class States:
    START = 'start'
    CHOOSE_SERVICE = 'choose_service'
    CHOOSE_DATE = 'choose_date'
    CHOOSE_TIME = 'choose_time'
    CONFIRM = 'confirm'

# Хранилище состояний пользователей (в памяти)
# Ключ: user_id, значение: словарь с состоянием и данными
user_states = {}

def get_state(user_id: int) -> dict:
    return user_states.get(user_id, {
        'state': States.START,
        'service': None,
        'date': None,
        'time': None
    })

def set_state(user_id: int, state: str, **kwargs):
    current = get_state(user_id)
    current['state'] = state
    current.update(kwargs)
    user_states[user_id] = current