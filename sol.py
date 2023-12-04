import csv
import argparse
from sortedcontainers import SortedList


def intersect(l1, r1, l2, r2):
    return not (l2 >= r1 or r2 <= l1)


class BookManager:

    def __init__(self):
        self.events_start = SortedList()
        self.events_end = {}
        self.data = []

    def add(self, start_time, end_time):
        self.data.append([start_time, end_time])
        if start_time > end_time:
            #print('Start time cannot be bigger than end_time', start_time, end_time)
            return False
        if not self.events_end:
            self.events_start.add(start_time)
            self.events_end[start_time] = end_time
            return True
        index = self.events_start.bisect_left(start_time)
        # checking neighbour in the left
        if index > 0:
            L = self.events_start[index - 1]
            R = self.events_end[L]
            if intersect(start_time, end_time, L, R): return False
        # checking neighbour in the right
        if index < len(self.events_start):
            L = self.events_start[index]
            R = self.events_end[L]
            if intersect(start_time, end_time, L, R): return False
        self.events_start.add(start_time)
        self.events_end[start_time] = end_time
        return True

    def remove(self, index):
        if index < 0 or index >= len(self.data):
            print('removal index should be in a range')
            return False
        start_time, end_time = self.data[index][0], self.data[index][1]
        if start_time not in self.events_end:
            print('already removed this event')
            return False
        self.events_start.remove(start_time)
        del self.events_end[start_time]
        return True


def process_events(filename, delimiter=','):
    book_manager = BookManager()

    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=delimiter)
        
        for row in csv_reader:
            start_time, end_time = int(row[0]), int(row[1])
            if start_time == 0:
                book_manager.remove(end_time)
            else:
                print(book_manager.add(start_time, end_time))


def main():
    parser = argparse.ArgumentParser(description='Read and print events processor')

    parser.add_argument('filename', type=str, help='path to csv')
    parser.add_argument('--delimiter', type=str, default=',', help='delimiter specification in case different from comma')

    args = parser.parse_args()

    process_events(args.filename, args.delimiter)


if __name__ == "__main__":
    main()

