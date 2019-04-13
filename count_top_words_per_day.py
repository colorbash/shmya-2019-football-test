from datetime import datetime
from collections import OrderedDict


class Parser:
    _string_counter = 0
    _histograms_per_day = {}
    MIN_WORD_LEN = 4
    READ_LINE_LIMIT = -1
    TOP_WORDS_LENGTH = 10
    USUAL_TOP_WORDS = ['2018', 'порно', 'скачать', 'онлайн', 'купить', 'погода', 'смотреть', 'бесплатно', 'сайт',
                       'официальный', 'фильм', 'фото', 'секс', 'видео', 'одноклассники', 'фильмы', 'авито', 'можно',
                       'сколько', 'слушать', 'почта', 'хорошем', 'качестве', 'магазин', 'сериал', 'отзывы', 'личный',
                       '2017']  # Found by top of all file

    @staticmethod
    def parse_file(filename):
        with open(filename, 'r') as file:
            file.readline()  # miss headers
            for line in file:
                Parser._parse_line(line)
                if Parser._string_counter > Parser.READ_LINE_LIMIT > 0:
                    break
            Parser._print_results()

    @staticmethod
    def _parse_date(line):
        dt_str = line[len(line) - 20:len(line) - 1]
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def _count_word(word, dt):
        if len(word) < Parser.MIN_WORD_LEN or word in Parser.USUAL_TOP_WORDS:
            return
        date = dt.date()
        if date not in Parser._histograms_per_day:
            Parser._histograms_per_day[date] = {}
        if word not in Parser._histograms_per_day[date]:
            Parser._histograms_per_day[date][word] = 1
        else:
            Parser._histograms_per_day[date][word] += 1

    @staticmethod
    def _parse_line(line):
        dt = Parser._parse_date(line)
        words = line[:len(line) - 21].split(' ')
        for word in words:
            Parser._count_word(word, dt)

        Parser._string_counter += 1
        if Parser._string_counter % 10000 == 0:
            print(Parser._string_counter)


    @staticmethod
    def _print_results():
        sorted_histograms_per_day = OrderedDict(sorted(Parser._histograms_per_day.items(), key=lambda t: t[0]))
        for date in sorted_histograms_per_day:
            print('\n')
            print('=======================================')
            print(date)
            print('=======================================')
            top = OrderedDict(sorted(Parser._histograms_per_day[date].items(), key=lambda t: t[1], reverse=True))
            for word_frequency in list(top.items())[0:Parser.TOP_WORDS_LENGTH]:
                print(word_frequency)


Parser.parse_file('football')

