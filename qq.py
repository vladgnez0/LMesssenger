import string
import secrets
from base64 import *
from tkinter import *
from base64 import b64encode
from Cryptodome.Cipher import AES
import tkinter.messagebox as mb
from tkinter.ttk import Combobox
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad


def show_error_length():
    error_msg = "Размер ключа должен быть равен 16 символов!"
    mb.showerror("Ошибка!", error_msg)


def show_error_length1():
    error_msg = "Размеры ключа и вектора инициализации должны быть равны по 16 символов!"
    mb.showerror("Ошибка!", error_msg)


def show_warning_iv():
    warning_msg = "Для режима ECB вектор инициализации не нужен."
    mb.showwarning("Ошибка!", warning_msg)
    text_iv.delete(0, END)


def gen(length):
    ld = string.ascii_letters + string.digits
    cs = ''.join(secrets.choice(ld) for i in range(length))
    return cs


def start():
    if combo1.get() == " " and combo2.get() == " ":
        text2.delete(4.0, END)

    text2.insert(5.0, "\n" + "\n" + "Для работы программы выберите режим шифрования, "
                                  "а затем что вы хотите сделать: Зашифровать или Расшифровать\n")

    if combo1.get() == "ECB" and (combo2.get() == "Зашифровать" or combo2.get() == "Расшифровать") and text_iv.get() != "":
        show_warning_iv()

    if combo1.get() == "ECB" and combo2.get() == "Зашифровать":
        clear_text2()

    key = bytes(text_key.get(), 'utf-8')
    data = text1.get()
    data = bytes(data, 'utf-8')
    text2.insert(END, "Ключ - " + str(key))

    try:
        cipher = AES.new(key, AES.MODE_ECB)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        text2.insert(END, "\n" + "\n" + "Шифротекст - " + ct)
    except ValueError:
        show_error_length()

    if combo1.get() == "ECB" and combo2.get() == "Расшифровать":
        clear_text2()

    key = text_key.get()
    key = bytes(key, 'utf-8')

    ct_bytes1 = text1.get()
    ct_bytes1 = ct_bytes1.encode('utf-8')
    ct_bytes = b64decode(ct_bytes1)
    cipher = AES.new(key, AES.MODE_ECB)
    original1 = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    original = original1.decode('utf-8')
    text2.insert(END, "Сообщение - " + original)

    # Continue the similar structure for CBC, CFB, and OFB modes...

def clear_text1():
     text1.delete(0, END)
     text_key.delete(0, END)
     text_iv.delete(0, END)



def clear_text2(): text2.delete(1.0, END)


def click_infoButton():
    if combo1.get() == "ECB":
        text2.delete(4.0, END)
        text2.insert(4.0, "\n" + "\n" + "Режим электронной кодовой книги (англ. Electronic Codebook, ECB) "
                                        "— один из вариантов использования симметричного блочного шифра, при "
                                        "котором каждый блок открытого текста заменяется блоком шифротекста.\n"
                                        "\nОсобенность:\n"
                                        "Режим устойчив к ошибкам, связанным с изменением битов блока (ошибка не "
                                        "распространяется на другие блоки), но неустойчив к ошибкам, связанным с "
                                        "потерей или вставкой битов, если не используется дополнительный механизм "
                                        "выравнивания блоков.\n"
                                        "\nДля данного режима дополнительно необходимо ввести ключ (16 символов).")
    elif combo1.get() == "CBC":
        text2.delete(4.0, END)
        text2.insert(END, "\n" + "\n" + "Режим сцепления блоков шифротекста (англ. Cipher Block Chaining, CBC) "
                                        "— один из режимов шифрования для симметричного блочного шифра "
                                        "блок открытого текста (кроме первого) побитово складывается по модулю 2 (операция XOR) "
                                        "с предыдущим результатом шифрования.\n"
                                        "\nОсобенность:\n"
                                        "Наличие механизма распространения ошибки: если при передаче произойдёт "
                                        "изменение одного бита шифротекста, данная ошибка распространится "
                                        "(через один) на следующий блок. Однако на последующие блоки "
                                        "ошибка не распространится, поэтому режим CBC также самовосстанавливающимся\n"
                                        "\nДля данного режима дополнительно необходимо "
                                        "ввести ключ (16 символов) и вектор инизиализации (Iv) (16 символов).")
    elif combo1.get() == "CFB":
        text2.delete(4.0, END)
        text2.insert(END, "\n" + "\n" + "Режим обратной связи по шифротексту, режим гаммирования с обратной связью "
                                        "(англ. Cipher Feedback Mode, CFB) — один из вариантов использования "
                                        "симметричного блочного шифра, при котором для шифрования следующего "
                                        "блока открытого текста он складывается по модулю 2 с "
                                        "перешифрованным предыдущего блока.\n"
                                        "\nОсобенность:\n"
                                        "Вектор инициализации IV, как и в режиме сцепления блоков шифротекста, можно делать известным, "
                                        "однако он должен быть уникальным.\n"
                                        "\nДля данного режима дополнительно необходимо "
                                        "ввести ключ (16 символов) и вектор инизиализации (Iv) (16 символов).")
    elif combo1.get() == "OFB":
        text2.delete(4.0, END)
        text2.insert(END, "\n" + "\n" + "Режим обратной связи по выходу (англ. Output Feedback, OFB) — один из "
                                        "вариантов использования симметричного блочного шифра. Особенностью "
                                        "режима является то, что в качестве входных данных для алгоритма блочного "
                                        "шифрования не используется само сообщение. Вместо "
                                        "этого блочный шифр байтов, который с "
                                        "используется для генерации псевдослучайного потока "
                                        "помощью операции XOR складывается с блоками "
                                        "открытого текста. Подобная "
                                        "схема шифрования называется потоковым шифром.\n"
                                        "\nОсобенность:\n"
                                        "Значение вектора инициализации должно быть уникальным для каждой "
                                        "процедуры шифрования одним ключом. Его необязательно сохранять в "
                                        "секрете и оно может быть передано вместе с шифротекстом.\n"
                                        "\nДля данного режима дополнительно необходимо "
                                        "ввести ключ (16 символов) и вектор инизиализации (Iv) (16 символов).")
    elif combo1.get() == " ":
        text2.delete(4.0, END)
        text2.insert(END, "\n" + "\n" + "AES (англ. Advanced Encryption Standard) — симметричный алгоритм блочного "
                                        "шифрования, принятый в качестве стандарта шифрования правительством США по "
                                        "результатам конкурса AES. Этот алгоритм хорошо проанализирован и сейчас "
                                        "широко используется, как это было с его предшественником DES.\n"
                                        "\nВ данной программе представлены несколько режимов работы данного алгоритма "
                                        "шифрования: ECB, CBC, CFB, OFB.")

window = Tk()
window.title("Программа AES")
window.geometry('580x490+400+400')
window.configure(bg='green')

# Поле ввода
label1 = Label(fg='black', bg='lightgrey', font=('TimesNewRoman', '12'), text="Поле ввода").place(x=20, y=2)
text1 = Entry(width=45, font=('TimesNewRoman', '12'))
text1.place(x=20, y=25)

# Поле ключа
label3 = Label(fg='black', bg='lightgrey', font=('TimesNewRoman', '12'), text="Поле ключа").place(x=20, y=55)
text_key = Entry(width=45, font=('TimesNewRoman', '12'))
text_key.place(x=20, y=80)

# Поле iv
label4 = Label(fg='black', bg='lightgrey', font=('TimesNewRoman', '12'), text="Поле iv").place(x=20, y=108)
text_iv = Entry(width=45, font=('TimesNewRoman', '12'))
text_iv.place(x=20, y=135)

# Комбо-Кнопка выбора режимов
values = [" ", "ECB", "CBC", "CFB", "OFB"]
values_var = StringVar(value=values[0])
combo1 = Combobox(window, width=17, values=values, textvariable=values_var)
label5 = Label(fg='black', bg='lightgrey', font=('TimesNewRoman', '12'), text="Режимы").place(x=440, y=2)
combo1.place(x=440, y=25)

# Комбо-Кнопка шифр/расшифр
values1 = [" ", "Зашифровать", "Расшифровать"]
values_var1 = StringVar(value=values1[0])
combo2 = Combobox(window, width=17, values=values1, textvariable=values_var1)
label6 = Label(fg='black', bg='lightgrey', font=('TimesNewRoman', '12'), text="шифр/расшифр").place(x=440, y=80)
combo2.place(x=440, y=105)

# Поле вывода
label2 = Label(fg='black', bg='lightgrey', font=('TimesNewRoman', '12'), text="Поле вывода").place(x=20, y=190)
text2 = Text(height=10, width=60, wrap=WORD, font=('TimesNewRoman', '12'))
text2.place(x=20, y=215)

# Кнопка запуска
startButton = Button(text="Запуск", width=10, bd=3, font=('TimesNewRoman', '10'), command=start)
startButton.place(x=176, y=450)



# Кнопка справка
infoButton = Button(text="Справка", width=10, bd=3, font=('TimesNewRoman', '10'), command=click_infoButton)
infoButton.place(x=20, y=450)

# Кнопка выйти
exitButton = Button(text="Выйти", width=10, bd=3, font=('TimesNewRoman', '10'), command=window.quit)
exitButton.place(x=480, y=450)

# Кнопка очистить2
clearButton2 = Button(text="Очистить", width=10, bd=3, font=('TimesNewRoman', '10'), command=clear_text2)
clearButton2.place(x=340, y=450)

text2.insert(1.0, "Случайный ключ - " + gen(16) + "\n")
text2.insert(2.0, "\n" + "Вектор инициализации (Iv) - " + gen(16))
window.mainloop()