import random

def generate_key(length):
    # Генерация случайного бинарного ключа заданной длины
    key = ''.join(random.choice('01') for _ in range(length))
    return key

def alice_send_qubits():
    # Алиса генерирует случайный бинарный ключ
    alice_key = generate_key(10)
    # Создание квантовых битов (qubits), например, используя поляризованные фотоны
    alice_qubits = [random.choice(['0', '1']) for _ in range(10)]
    return alice_key, alice_qubits

def bob_measure_qubits(alice_qubits):
    # Боб выбирает случайные биты для измерения
    bob_measurements = [random.choice(['0', '1']) for _ in alice_qubits]
    # Боб измеряет квантовые биты Алисы
    bob_results = [alice_qubits[i] if bob_measurements[i] == '0' else random.choice(['0', '1']) for i in range(len(alice_qubits))]
    return bob_results

def alice_announce_basis(alice_qubits):
    # Алиса объявляет базис, который она использовала при создании квантовых битов
    alice_basis = alice_qubits.copy()
    return alice_basis

def bob_announce_basis(bob_measurements):
    # Боб объявляет базис, который он использовал при измерении квантовых битов
    bob_basis = bob_measurements.copy()
    return bob_basis

def key_exchange(alice_key, bob_results):
    # Обмен результатами и создание общего ключа
    shared_key = ''.join([alice_key[i] for i in range(len(alice_key)) if alice_key[i] == bob_results[i]])
    return shared_key

# Пример использования протокола B92
alice_key, alice_qubits = alice_send_qubits()
bob_results = bob_measure_qubits(alice_qubits)
alice_basis = alice_announce_basis(alice_qubits)
bob_basis = bob_announce_basis(bob_results)
shared_key = key_exchange(alice_key, bob_results)

# Вывод информации
print("Алиса отправляет квантовые биты:", alice_qubits)
print("Боб измеряет квантовые биты и получает результаты:", bob_results)
print("Алиса объявляет свои базисы:", alice_basis)
print("Боб объявляет свои базисы:", bob_basis)
print("Обмен и создание общего ключа:", shared_key)
