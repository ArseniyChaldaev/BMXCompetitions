from datetime import datetime

import utils.DbHelper as DbHelper


class Competition:
    def __init__(self, unique_id=None, title='', date=None, city='', type_id=1, year=None):
        self.unique_id = unique_id
        self.title = str(title)
        if date:
            self.date = str(date)
            self.year = year
        else:
            self.date = f"{datetime.now():%d.%m.%Y}"
            self.year = datetime.now().year
        self.city = str(city)
        self.type_id = type_id

    def getValues(self):
        return self.title, self.date, self.city, self.type_id, self.year

    def save(self):
        if self.unique_id:
            query = f"""UPDATE competitions
                        SET title = ?, date = ?, city = ?, type_id = ?, year = ?
                        WHERE id = {self.unique_id}"""
        else:
            query = """INSERT INTO competitions(title, date, city, type_id, year)
                        VALUES(?, ?, ?, ?, ?)"""
        DbHelper.execute_on_db(query, self.getValues())


def getCompetitionById(competition_id):
    if not competition_id:
        return Competition()
    query = f'SELECT id, title, date, city, type_id, year FROM competitions WHERE id = {competition_id}'
    result = DbHelper.get_one_from_db(query)
    if result:
        return Competition(*result)
    return Competition()


def getCompetitions(type_id=None, city=None, year=None):
    query = "SELECT id, title, date, city, type_id, year FROM competitions"
    if type_id or city or year:
        query += " WHERE "
        conditions = []
        if type_id:
            conditions.append(f" type_id={type_id}")
        if city:
            conditions.append(f" city='{city}'")
        if year:
            conditions.append(f" year={year}")
        query += ' AND '.join(conditions)
    return [Competition(*row) for row in DbHelper.get_all_from_db(query)]


def deleteCompetition(competition_id):
    if competition_id:
        DbHelper.execute_on_db(f'DELETE FROM competitions WHERE id = {competition_id}')


def getCompetitionTypes():
    query = "SELECT id, title FROM competition_types"
    return DbHelper.get_all_from_db(query)


def getCities():
    query = "SELECT DISTINCT city FROM competitions ORDER BY city"
    return DbHelper.get_all_from_db(query)
