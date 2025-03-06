import random
# 0 - это ↑, а 1 - это ↗
def generate_key(length):
    # Генерация случайного бинарного ключа заданной длины
    key = ''.join(random.choice('01') for _ in range(length))
    return key
def alice_send_qubits(length):
    # Алиса генерирует случайный бинарный ключ
    alice_key = generate_key(length)
    # Создание квантовых битов (qubits), например, используя поляризованные фотоны
    alice_qubits = [random.choice(['0', '1']) for _ in range(length)]
    return alice_key, alice_qubits
def bob_measure_qubits(alice_qubits):
    # Боб выбирает случайные биты для измерения
    bob_measurements = [random.choice(['0', '1']) for _ in alice_qubits]
    # Боб измеряет квантовые биты Алисы
    bob_results = [alice_qubits[i] if bob_measurements[i] == '0' else random.choice(['0', '1']) for i in range(len(alice_qubits))]
    return bob_results
def alice_announce_basis(alice_qubits, bob_measurements):
    # Алиса сообщает Бобу, какие базисы она использовала при создании квантовых битов
    alice_basis = alice_qubits.copy()
    return alice_basis
def bob_announce_basis(bob_measurements):
    # Боб сообщает Алисе, какие базисы он использовал при измерении квантовых битов
    bob_basis = bob_measurements.copy()
    return bob_basis
def key_exchange(alice_key, bob_results):
    # Обмен результатами и создание общего ключа
    shared_key = ''.join([alice_key[i] for i in range(len(alice_key)) if alice_key[i] == bob_results[i]])
    return shared_key
