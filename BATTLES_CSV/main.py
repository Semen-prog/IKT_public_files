import os
import sqlite3

from flask import Flask, render_template, session, g, request
from flask_sqlalchemy import SQLAlchemy
from geopy import Nominatim
from werkzeug.utils import redirect

from database_process import get_connection

import matplotlib.pyplot as plt
from tkinter import *


def paint_pie(members):
    mem, val = [], []
    for a in members:
        mem.append(a)
        val.append(members[a])

    fig, ax = plt.subplots()
    ax.pie(val, labels=mem)
    ax.axis("equal")
    plt.show()

def paint_date(dates):
    k = []
    for date in dates:
        k.append(date)

    k.sort()
    val = []
    for i in range(len(k)):
        val.append(dates[k[i]])
    fig, ax = plt.subplots()
    ax.bar(k, val, width=0.5)
    ax.axis([k[0] - 10, k[-1] + 10, 0, max(val) + 1])
    plt.show()

def paint_map(tab):
    W, H = 929, 465
    master = Tk()
    cnv = Canvas(master, width=W, height=H)
    cnv.pack()
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    img = PhotoImage(master=cnv, file=APP_ROOT + "\\map.png")
    cnv.create_image(0, 0, anchor=NW, image=img)
    cnt = 1
    d = {}

    for (loc, y, x) in tab:
        l = cnv.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")
        print(x, y, cnt, loc)
        d[cnt] = [loc, x, y]
        cnt += 1

    def motion(event):
        cnv.delete('todel')
        x, y = event.x, event.y
        for i in d:
            loc, x0, y0 = d[i]
            if ((x - x0) ** 2 + (y - y0) ** 2) <= 4:
                cnv.create_text(x - 4, y - 4, text=loc[0] + loc[1:].lower(), fill='white', font='Arial 10', tag='todel')

                break


    cnv.bind('<Motion>', motion)
    mainloop()

app = Flask(__name__)
app.secret_key = 'f2ab45a3111c3c3b39daddd70dae55f2340f3cbe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
teacher_check_code = 'b42d7a08b78560ffc949fa045b99145c45027e53'
db = SQLAlchemy(app)

bat_size = 660


def members_func(res, tp):
    conn, cur = get_connection('battles.db')
    ask = """SELECT attacker, defender FROM battle_dyads
        INNER JOIN battles
            ON battle_dyads.isqno = battles.isqno
        WHERE """
    for r in res:
        ask += "battles.isqno = " + str(r) + " OR "
    ask = ask[:-4]
    cur.execute(ask)
    tab = cur.fetchall()
    attackers, defenders = {}, {}
    for [attacker, defender] in tab:
        if attacker not in attackers:
            attackers[attacker] = 0
        attackers[attacker] += 1
        if defender not in defenders:
            defenders[defender] = 0
        defenders[defender] += 1
    if not tp:
        paint_pie(attackers)
    else:
        paint_pie(defenders)

def weather_func(res, tp):
    conn, cur = get_connection('battles.db')
    ask = """SELECT description FROM weather
        INNER JOIN enum_wx2
            ON weather.wx2 = enum_wx2.value
        WHERE """
    for r in res:
        ask += "isqno = " + str(r) + " OR "
    ask = ask[:-4]
    cur.execute(ask)
    tab = cur.fetchall()
    precipitation, temperature = {}, {}
    for [precip] in tab:
        if precip not in precipitation:
            precipitation[precip] = 0
        precipitation[precip] += 1
    ask = """SELECT description FROM weather
            INNER JOIN enum_wx3
                ON weather.wx3 = enum_wx3.value
            WHERE """
    for r in res:
        ask += "isqno = " + str(r) + " OR "
    ask = ask[:-4]
    cur.execute(ask)
    tab = cur.fetchall()
    for [temp] in tab:
        if temp not in temperature:
            temperature[temp] = 0
        temperature[temp] += 1
    if not tp:
        paint_pie(precipitation)
    else:
        paint_pie(temperature)

def time_func(res, tp):
    conn, cur = get_connection('battles.db')
    ask = """SELECT datetime_min, duration1 FROM battle_durations
            INNER JOIN battles
                ON battle_durations.isqno = battles.isqno
            WHERE """
    for r in res:
        ask += "battles.isqno = " + str(r) + " OR "
    ask = ask[:-4]
    cur.execute(ask)
    tab = cur.fetchall()
    times_start, durations = {}, {}
    for [tm, dr] in tab:
        tm, dr = int(tm[:4]), float(dr)
        if tm not in times_start:
            times_start[tm] = 0
        times_start[tm] += 1
        if dr not in durations:
            durations[dr] = 0
        durations[dr] += 1
    if not tp:
        paint_date(times_start)
    else:
        paint_date(durations)

def map_func(res):
    ask = "SELECT locn FROM battles WHERE isqno = "
    for r in res:
        ask += str(r) + ' OR isqno = '
    ask = ask[:-12]
    conn, cur = get_connection('battles.db')
    ans = cur.execute(ask).fetchall()
    tab = []

    W_map, H_map = 929, 465
    geolocator = Nominatim(user_agent="main")
    for [loc] in ans:
        location = geolocator.geocode(loc)
        tab.append((loc, H_map - ((location.latitude + 90) / 180 * H_map), (location.longitude + 180) / 360 * W_map))

    paint_map(tab)


def count_res():
    isqno = set([i for i in range(1, bat_size + 1)])
    conn, cur = get_connection('battles.db')
    if session['name'] != 'Не выбрано':
        ask = 'SELECT isqno FROM battles WHERE name = "' + session['name'] + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if session['war'] != 'Не выбрано':
        ask = 'SELECT isqno FROM battles WHERE war = "' + session['war'] + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if session['duration'] != '####':
        ask = 'SELECT isqno FROM battles WHERE duration1 = "' + session['duration'] + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if session['year_start'] != '####':
        ask = 'SELECT isqno FROM battle_durations WHERE datetime_min LIKE "' + session['year_start'] + '%"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if session['precipitation'] != 'Не выбрано':
        ask = "SELECT value FROM enum_wx2 WHERE description = '" + session['precipitation'] + "'"
        cur.execute(ask)
        en = cur.fetchone()[0]
        ask = "SELECT isqno FROM weather WHERE wx2 = '" + en + "'"
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if session['temp'] != 'Не выбрано':
        ask = "SELECT value FROM enum_wx3 WHERE description = '" + session['temp'] + "'"
        cur.execute(ask)
        en = cur.fetchone()[0]
        ask = "SELECT isqno FROM weather WHERE wx3 = '" + en + "'"
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if session['attacker'] != 'Не выбрано':
        ask = 'SELECT isqno FROM battle_dyads WHERE attacker = "' + session['attacker'] + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st
    if session['defender'] != 'Не выбрано':
        ask = 'SELECT isqno FROM battle_dyads WHERE defender = "' + session['defender'] + '"'
        cur.execute(ask)
        vars = cur.fetchall()
        st = set()
        for v in vars:
            st.add(v[0])
        isqno &= st

    return isqno


@app.before_request
def initialize():
    g.name = session['name']
    g.war = session['war']
    g.duration = session['duration']
    g.year_start = session['year_start']
    g.precipitation = session['precipitation']
    g.temp = session['temp']
    g.attacker = session['attacker']
    g.defender = session['defender']


@app.before_first_request
def init():
    session['name'] = 'Не выбрано'
    session['war'] = 'Не выбрано'
    session['attacker'] = 'Не выбрано'
    session['defender'] = 'Не выбрано'
    session['precipitation'] = 'Не выбрано'
    session['temp'] = 'Не выбрано'
    session['year_start'] = '####'
    session['duration'] = '####'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/filters')
def filters():
    link_list = ['/change/type=names', '/change/type=temperature', '/change/type=members', '/change/type=time']
    return render_template('filters.html', link_list=link_list)


@app.route('/change/type=<string:type>', methods=['POST', 'GET'])
def changes(type):
    tp, list1, list2 = None, None, None
    if type == 'names':
        if request.method == 'POST':
            session['name'] = request.form['bat']
            session['war'] = request.form['war']
            return redirect('/filters')
        conn, cur = get_connection('battles.db')
        ask = 'SELECT name FROM battles'
        w = cur.execute(ask).fetchall()
        w.append(('Не выбрано',))
        q_name = [g.name]
        for i in w:
            if g.name != i[0]:
                q_name.append(i[0])
        ask = 'SELECT war FROM battles'
        w = set(cur.execute(ask).fetchall())
        w.add(('Не выбрано',))
        q_war = [g.war]
        for i in w:
            if g.war != i[0]:
                q_war.append(i[0])

        tp = 0
        list1 = q_name
        list2 = q_war

    elif type == 'members':
        if request.method == 'POST':
            session['attacker'] = request.form['at']
            session['defender'] = request.form['def']
            return redirect('/filters')
        conn, cur = get_connection('battles.db')
        ask = 'SELECT attacker FROM battle_dyads'
        w = set(cur.execute(ask).fetchall())
        w.add(('Не выбрано',))
        q_at = [g.attacker]
        for i in w:
            if g.attacker != i[0]:
                q_at.append(i[0])

        ask = 'SELECT defender FROM battle_dyads'
        w = set(cur.execute(ask).fetchall())
        w.add(('Не выбрано',))
        q_def = [g.defender]
        for i in w:
            if g.defender != i[0]:
                q_def.append(i[0])

        tp = 1
        list1 = q_at
        list2 = q_def

    elif type == 'temperature':
        if request.method == 'POST':
            session['temp'] = request.form['temp']
            session['precipitation'] = request.form['precip']
            return redirect('/filters')
        w = {'Hot', 'Cold', 'Temperate'}
        w.add('Не выбрано')
        q_temp = [g.temp]
        for i in w:
            if g.temp != i:
                q_temp.append(i)

        w = {'Heavy Precipitatiion', 'Sunny (no precipitation)', 'Light Precipitation', 'Overcast (no precipitation)'}
        w.add('Не выбрано')
        q_prc = [g.precipitation]
        for i in w:
            if g.precipitation != i:
                q_prc.append(i)

        tp = 2
        list1 = q_temp
        list2 = q_prc
    else:
        if request.method == 'POST':
            session['year_start'] = request.form['yearStart']
            session['duration'] = request.form['duration']
            return redirect('/filters')
        tp = 3
        list1 = []
        list2 = []

    return render_template('changes.html', type=tp, list1=list1, list2=list2)


@app.route('/result')
def result():
    cnt_result = len(count_res())
    return render_template('result.html', cnt=cnt_result)


@app.route('/paint/type=<string:type>')
def paint(type):
    res = list(count_res())
    if type == 'precip':
        weather_func(res, 0)
    elif type == 'temp':
        weather_func(res, 1)
    elif type == 'attack':
        members_func(res, 0)
    elif type == 'defend':
        members_func(res, 1)
    elif type == 'ystart':
        time_func(res, 0)
    elif type == 'duration':
        time_func(res, 1)
    else:
        map_func(res)
    return redirect('/result')

if __name__ == '__main__':
    app.run(debug=True)