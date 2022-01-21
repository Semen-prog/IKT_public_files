import database_process as db
from tkinter import ttk
from tkinter import *
from user import User

W, H = 500, 500
master = Tk()
master.geometry('500x500')

bat_size = 660

def find():
    s = cmb1.get()
    if s == '':
        return
    m = Tk()
    m.geometry('500x500')
    conn, cur = db.get_connection()
    if s == "Name":
        l1 = Label(m, text="Выберите битву:", height=5, width=20, font="Arial 10")
        l2 = Label(m, text="Выберите войну:", height=5, width=20, font="Arial 10")
        names = set()
        wars = set()
        for i in range(1, bat_size + 1):
            ask = "SELECT name FROM battles WHERE isqno = " + str(i)
            cur.execute(ask)
            names.add(cur.fetchone()[0])
            ask = "SELECT war FROM battles WHERE isqno = " + str(i)
            cur.execute(ask)
            wars.add(cur.fetchone()[0])
        c1 = ttk.Combobox(m, values=list(names))
        c2 = ttk.Combobox(m, values=list(wars))
        but1 = Button(m, text="Сохранить", bg="white", command=lambda: user.update([[c1.get(), 1], [c2.get(), 2]]))
        but2 = Button(m, text="Удалить выбор", bg="white", command=lambda: user.update([[None, 1], [None, 2]]))
        l1.grid(row=0, column=0)
        c1.grid(row=0, column=1)
        l2.grid(row=1, column=0)
        c2.grid(row=1, column=1)
        but1.grid(row=2, column=1)
        but2.grid(row=3, column=1)
    elif s == "Members":
        l1 = Label(m, text="Выберите атакующего:", height=5, width=20, font="Arial 10")
        l2 = Label(m, text="Выберите защитника:", height=5, width=20, font="Arial 10")
        at = set()
        df = set()
        for i in range(1, bat_size + 1):
            ask = "SELECT attacker FROM battle_dyads WHERE isqno = " + str(i)
            cur.execute(ask)
            mem = cur.fetchall()
            for g in mem:
                at.add(g[0])
            ask = "SELECT defender FROM battle_dyads WHERE isqno = " + str(i)
            cur.execute(ask)
            mem = cur.fetchall()
            for g in mem:
                df.add(g[0])
        c1 = ttk.Combobox(m, values=list(at))
        c2 = ttk.Combobox(m, values=list(df))
        but1 = Button(m, text="Сохранить", bg="white", command=lambda: user.update([[c1.get(), 7], [c2.get(), 8]]))
        but2 = Button(m, text="Удалить выбор", bg="white", command=lambda: user.update([[None, 7], [None, 8]]))
        l1.grid(row=0, column=0)
        c1.grid(row=0, column=1)
        l2.grid(row=1, column=0)
        c2.grid(row=1, column=1)
        but1.grid(row=2, column=1)
        but2.grid(row=3, column=1)
    elif s == "Weather":
        l1 = Label(m, text="Осадки:", height=5, width=20, font="Arial 10")
        l2 = Label(m, text="Температура:", height=5, width=20, font="Arial 10")
        c1 = ttk.Combobox(m, values=["Heavy Precipitatiion", "Sunny (no precipitation)", "Light Precipitation", "Overcast (no precipitation)"])
        c2 = ttk.Combobox(m, values=["Hot", "Cold", "Temperate"])
        but1 = Button(m, text="Сохранить", bg="white", command=lambda: user.update([[c1.get(), 5], [c2.get(), 6]]))
        but2 = Button(m, text="Удалить выбор", bg="white", command=lambda: user.update([[None, 5], [None, 6]]))
        l1.grid(row=0, column=0)
        c1.grid(row=0, column=1)
        l2.grid(row=1, column=0)
        c2.grid(row=1, column=1)
        but1.grid(row=2, column=1)
        but2.grid(row=3, column=1)
    else:
        l1 = Label(m, text="Год начала:", height=5, width=20, font="Arial 10")
        l2 = Label(m, text="Длительность, дн:", height=5, width=20, font="Arial 10")
        e1 = Entry(m, width=20)
        e2 = Entry(m, width=20)
        but1 = Button(m, text="Сохранить", bg="white", command=lambda: user.update([[e1.get(), 4], [e2.get(), 3]]))
        but2 = Button(m, text="Удалить выбор", bg="white", command=lambda: user.update([[None, 4], [None, 3]]))
        l1.grid(row=0, column=0)
        e1.grid(row=0, column=1)
        l2.grid(row=1, column=0)
        e2.grid(row=1, column=1)
        but1.grid(row=2, column=1)
        but2.grid(row=3, column=1)

    mainloop()

def paint():
    pass

def search():
    m = Tk()
    m.geometry('1000x1000')
    isqno = set([i for i in range(1, bat_size + 1)])
    conn, cur = db.get_connection()
    # scrollbar = Scrollbar(m)
    # scrollbar.pack(side="right", fill="y")
    if user.name:
        ask = 'SELECT isqno FROM battles WHERE name = "' + user.name + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if user.war:
        ask = 'SELECT isqno FROM battles WHERE war = "' + user.war + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if user.duration:
        ask = 'SELECT isqno FROM battles WHERE duration1 = "' + user.duration + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if user.year_start:
        ask = 'SELECT isqno FROM battle_durations WHERE datetime_min LIKE "' + user.year_start + '%"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if user.precipitation:
        ask = "SELECT value FROM enum_wx2 WHERE description = '" + user.precipitation + "'"
        cur.execute(ask)
        en = cur.fetchone()[0]
        ask = "SELECT isqno FROM weather WHERE wx2 = '" + en + "'"
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if user.temp:
        ask = "SELECT value FROM enum_wx3 WHERE description = '" + user.precipitation + "'"
        cur.execute(ask)
        en = cur.fetchone()[0]
        ask = "SELECT isqno FROM weather WHERE wx3 = '" + en + "'"
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if user.attacker:
        ask = 'SELECT isqno FROM battle_dyads WHERE attacker = "' + user.attacker + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if user.defender:
        ask = 'SELECT isqno FROM battle_dyads WHERE defender = "' + user.defender + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if len(isqno) == 0:
        lab = Label(m, text="Нет результатов", height=2, width=45, font="Arial 10 bold")
        lab.grid(row=0, column=0)
    else:
        ask = """SELECT name, war FROM battles
        WHERE """
        for el in isqno:
            cur.execute("SELECT name FROM battles WHERE isqno = " + str(el))
            a = cur.fetchone()[0]
            ask += "name = '" + a + "' OR "
        ask = ask[:-4]
        cur.execute(ask)
        tab = cur.fetchall()
        lab = Label(m, text="Результаты поиска:", height=2, width=15, font="Arial 10")
        lab.grid(row=0, column=0)
        trans = ['NAME', 'WAR']
        for j in range(len(tab[0])):
            lab = Label(m, text=trans[j], height=3, font="Arial 10 bold")
            lab.grid(row=1, column=j)
            for i in range(len(tab)):
                lab = Label(m, text=tab[i][j], height=3, font="Arial 10")
                lab.grid(row=i+2, column=j)
    mainloop()

user = User()

l2 = Label(master, text="Инфографика:", height=8, width=20, font="Arial 10")
l1 = Label(master, text="Фильтры битвы:", height=5, width=20, font="Arial 10")
cmb1 = ttk.Combobox(master, values=['Name', 'Weather', 'Members', 'Time'])
cmb2 = ttk.Combobox(master, values=['Date', 'Precipitation', "Temperature", 'Members', 'Duration'])
b1 = Button(master, text="Выбрать параметры", bg="white", command=find)
b2 = Button(master, text="Построить график", bg="white", command=paint)
b3 = Button(master, text="Найти битву", bg="white", command=search)
l2.grid(row=3, column=0)
l1.grid(row=0, column=0)
cmb1.grid(row=0, column=1)
cmb2.grid(row=3, column=1)
b1.grid(row=1, column=1)
b2.grid(row=4, column=1)
b3.grid(row=2, column=1)

mainloop()