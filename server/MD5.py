import math
''' 
1. Инициализация переменных: Начальные значения хеш-переменных A, B, C, D задаются определенными константами, которые используются в ходе алгоритма.

2. Подготовка сообщения: Исходное сообщение разбивается на блоки фиксированного размера. Добавляется бит "1" после сообщения и также нули так, чтобы длина сообщения в битах стала на 64 бита меньше, чем кратна 512.

3. Добавление длины сообщения: К оставшейся части блока сообщения добавляется длина исходного сообщения (в битах), представленная в виде 64-битного числа (little-endian).

4. Итерационные раунды: Затем для каждого блока сообщения выполняются 64 итерационных раунда, каждый раз обрабатывая 16 32-битных слов сообщения. В каждом раунде происходит комбинация преобразований, таких как битовые логические операции (AND, OR, XOR), сдвиги и сложения.

5. Обновление переменных: После всех раундов значения хеш-переменных A, B, C, D обновляются на основе выполненных операций в каждом раунде.

6. Формирование окончательного хеша: Полученные значения переменных A, B, C, D объединяются в определенной последовательности для формирования 128-битного дайджеста сообщения - окончательного хеш-значения.
1. **Константы**: В начале кода определены константы, такие как `rotate_amounts`, `constants`, `init_values`, `functions`, и `index_functions`. Эти константы используются в дальнейшем в ходе выполнения алгоритма для реализации итераций и битовых операций.

2. **left_rotate**: Это функция, которая выполняет циклический сдвиг битов влево на указанное количество позиций.

3. **md5**: Это основная функция, которая принимает на вход сообщение и выполняет все шаги алгоритма MD5 для получения итогового хеш-значения.

4. **md5_to_hex**: Эта функция преобразует окончательное хеш-значение (представленное в виде числа) в шестнадцатеричную строку.

В ходе выполнения алгоритма `md5`, сообщение разбивается на блоки, затем для каждого блока выполняется ряд итераций, в которых используются определенные константы, функции и сдвиги. На выходе получается 128-битное хеш-значение, которое в конечном итоге преобразуется в шестнадцатеричную строку с помощью функции `md5_to_hex`.
'''
rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + \
            16 * [lambda b, c, d: (d & b) | (~d & c)] + \
            16 * [lambda b, c, d: b ^ c ^ d] + \
            16 * [lambda b, c, d: c ^ (b | ~d)]

index_functions = 16 * [lambda i: i] + \
                  16 * [lambda i: (5 * i + 1) % 16] + \
                  16 * [lambda i: (3 * i + 5) % 16] + \
                  16 * [lambda i: (7 * i) % 16]


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(message):
    message = bytearray(message)  # copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')

    hash_pieces = init_values[:]

    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))


def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))


if __name__ == '__main__':
    demo = [b"", b"a", b"abc", b"message digest", b"abcdefghijklmnopqrstuvwxyz",
            b"fdgdsf",
            b"12345678901234567890123456789012345678901234567890123456789012345678901234567890"]
    for message in demo:
        print(md5_to_hex(md5(message)), ' <= "', message.decode('ascii'), '"', sep='')