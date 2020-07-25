import asyncio
import time

from printer import Printer


sec_calc = lambda h, m, s: 3600 * int(h) + 60 * int(m) + float(s)
time_minus = lambda t2, t1: (t2 - t1) % 86400
time_str_calc = lambda sec: f'{sec//3600:02.0f}:{sec%3600//60:02.0f}:{sec%60:02.0f}'


def sec_now():
    time_tuple = time.localtime()
    return sec_calc(time_tuple.tm_hour, time_tuple.tm_min, time_tuple.tm_sec)


class Schedule:
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Schedule, cls).__new__(cls)
            cls.instance.scheduled_sleep = False
        return cls.instance

    async def run(self, schedule_str):
        if schedule_str == '':
            Printer().printer("请填入定时休眠时间段", "Warning", "red")
            self.scheduled_sleep = False
            return
        second_array = sorted([[sec_calc(*time_str.split(':')) for time_str in
                                time_str_pair.split('-')] for time_str_pair in schedule_str.split(';')])
        second_array = [[start, end] for (start, end) in second_array if start != end]
        if not len(second_array):
            Printer().printer("请填入有效时间段", "Warning", "red")
            self.scheduled_sleep = False
            return
        # 按顺序合并有overlap的时间段
        second_rearrng = [second_array[0]]
        pos = 1
        while pos < len(second_array):
            if time_minus(second_array[pos][0], second_rearrng[-1][0]) <= \
                    time_minus(second_rearrng[-1][1], second_rearrng[-1][0]):
                if time_minus(second_rearrng[-1][1], second_rearrng[-1][0]) < \
                        time_minus(second_array[pos][1], second_rearrng[-1][0]):
                    second_rearrng[-1][1] = second_array[pos][1]
            else:
                second_rearrng.append(second_array[pos])
            pos += 1
        # 考虑最后一个跨0点时间段覆盖最开始几个时间段端点的情况
        if second_rearrng[-1][1] < second_rearrng[-1][0]:
            while len(second_rearrng) > 1:
                if second_rearrng[-1][1] > second_rearrng[0][0]:
                    if second_rearrng[-1][1] < second_rearrng[0][1]:
                        second_rearrng[-1][1] = second_rearrng[0][1]
                    del second_rearrng[0]
                else:
                    break
        sec_sequence = __import__('functools').reduce(lambda x, y: x+y, second_rearrng)

        sec_init = sec_now()
        for i in range(len(sec_sequence)):
            if sec_sequence[i] > sec_init:
                stage = i
                break
        else:
            stage = len(sec_sequence)-1 if sec_sequence[-1] < sec_sequence[-2] else 0
        # 当前时间在0时后且在最后一个包含0时的时间段内
        if stage == 0 and sec_init < sec_sequence[-1] < sec_sequence[-2]:
            stage = len(sec_sequence)-1

        if stage % 2 == 1:
            self.scheduled_sleep = True
            Printer().printer(f"当前处于定时休眠时间段内，下一次取消休眠时间为 {time_str_calc(sec_sequence[stage])}", "Info", "green")
        else:
            self.scheduled_sleep = False
            Printer().printer(f"当前处于定时休眠时间段外，下一次开始休眠时间为 {time_str_calc(sec_sequence[stage])}", "Info", "green")
        while True:
            sleep_time = (sec_sequence[stage] - sec_now()) % 86400
            # 避免因误差刚好过了下个时间点
            sleep_time = 0 if sleep_time > 86395 else sleep_time
            await asyncio.sleep(sleep_time)
            stage += 1
            stage = stage % len(sec_sequence)
            if stage % 2 == 0:
                Printer().printer(f"结束定时休眠，下一次开始休眠时间为 {time_str_calc(sec_sequence[stage])}", "Info", "green")
                self.scheduled_sleep = False
            else:
                Printer().printer(f"开始定时休眠，本次结束休眠时间为 {time_str_calc(sec_sequence[stage])}", "Info", "green")
                self.scheduled_sleep = True
