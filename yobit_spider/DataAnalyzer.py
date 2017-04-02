__author__ = 'tahsin'
import datetime
import sys

class Analyzer(object):
    def __init__(self, src_cur, dst_cur, data):
        self._src_currency = src_cur
        self._dst_currency = dst_cur
        self._data = data

    def analyze(self):
        for cur_item in self._data:
            if cur_item[0]['src_name'] == self._src_currency:
                if cur_item[0]['dst_name'] == self._dst_currency:
                    self._data = cur_item
                    break

        now = datetime.datetime.now()
        # check records for 5 min. before
        m = now.minute - 5 if now.minute - 5 >= 0 else 0
        # +2 due to time difference
        h = (now.hour + 2) % 24

        h = str(h) if h > 9 else "0" + str(h)
        m = str(m) if m > 9 else "0" + str(m)
        s = str(now.second) if now.second > 9 else "0" + str(now.second)

        formatted_time = ":".join([h, m, s])
        print(self._data)
        # filter with the time
        self._data = [x for x in self._data if x['time'] >= formatted_time]

        print("after filter")
        print(self._data)
        # sort the list based on time in descending order
        self._data = sorted(self._data, key=lambda k: k['time'], reverse=True)
        self._data.append({'biggest_percentage': self.calculate_biggest_difference(self._data)})
        return self._data

    def calculate_biggest_difference(self, data):
        if len(data) <= 1:
            return 0

        max = -sys.maxint
        diff = 0
        idx = 1
        while idx < len(data):
            diff = float(data[idx]['price']) - float(data[idx-1]['price'])
            if diff > max:
                max = diff

            idx += 1

        # return in percentage
        return max * 100
