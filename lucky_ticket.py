import datetime
from threading import Thread
from multiprocessing import Process


def count_lucky_ticket(start, end):
    """считаем к-во возможных счастливых билетов"""
    count = 0
    for i in range(start, end):
        ticket = str(i).rjust(6, '0')
        num_1 = int(ticket[0]) + int(ticket[1]) + int(ticket[2])
        num_2 = int(ticket[3]) + int(ticket[4]) + int(ticket[5])
        if num_1 == num_2:
            count += 1

    print('${}$'.format(count))

print('------count with Process--------')
time_start = datetime.datetime.now()

# создаем потоки для счастливых билетов, каждый обрабатывает четверть диапазона
p1 = Process(target=count_lucky_ticket, args=(0, 250000,))
p2 = Process(target=count_lucky_ticket, args=(250000, 500000,))
p3 = Process(target=count_lucky_ticket, args=(500000, 750000,))
p4 = Process(target=count_lucky_ticket, args=(750000, 1000000,))

p1.start()
p2.start()
p3.start()
p4.start()

p1.join()
p2.join()
p3.join()
p4.join()

print(datetime.datetime.now() - time_start)

print('-------count with Thread---------')
time_start = datetime.datetime.now()

t1 = Thread(target=count_lucky_ticket, args=[0, 250000])
t2 = Thread(target=count_lucky_ticket, args=[250000, 500000])
t3 = Thread(target=count_lucky_ticket, args=[500000, 750000])
t4 = Thread(target=count_lucky_ticket, args=[750000, 1000000])

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print(datetime.datetime.now() - time_start)