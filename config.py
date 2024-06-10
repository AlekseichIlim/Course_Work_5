from configparser import ConfigParser


names_company = ['Группа Илим', 'Яндекс', 'Яндекс Команда для бизнеса',
                 'Газпром автоматизация', 'Русал Комплектация',
                 'НК Роснефть-МЗ Нефтепродукт', 'Газпром нефть',
                 'Ростелеком Информационные Технологии',
                 'Ростелеком - Центры обработки данных', 'Сбер Бизнес Софт']

def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db

