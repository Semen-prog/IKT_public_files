import matplotlib.pyplot as plt

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