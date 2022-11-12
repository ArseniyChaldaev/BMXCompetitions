import base64
import os
from datetime import datetime

import utils.DbHelper as DbHelper
from GlobalVars import DEFAULT_IMAGE_PATH, DEFAULT_IMAGE


class Sportsman:
    def __init__(self, unique_id=None, name='', surname='', birthday=None, gender=1, photo='', year=None, score=None):
        self.unique_id = unique_id
        self.name = str(name)
        self.surname = str(surname)
        self.birthday = str(birthday)
        self.gender = gender
        if photo:
            self.photo = photo
        else:
            self.setPhoto(DEFAULT_IMAGE_PATH)
        self.year = year
        self.score = score if score else 0

    def getValues(self):
        return self.name, self.surname, self.birthday, self.gender, self.photo, self.year

    def save(self):
        if self.unique_id:
            query = f"""UPDATE sportsmen 
                        SET name = ?, surname = ?, birthday = ?, gender = ?, photo = ?, year = ?
                        WHERE id = {self.unique_id}"""
        else:
            query = """INSERT INTO sportsmen(name, surname, birthday, gender, photo, year)
                        VALUES(?, ?, ?, ?, ?, ?)"""
        DbHelper.execute_on_db(query, self.getValues())

    def setPhoto(self, filename):
        if os.path.exists(filename):
            file = open(filename, "rb")
            self.photo = file.read()
            file.close()
        else:
            self.photo = base64.b64decode(DEFAULT_IMAGE.encode('ascii'))


def getSportsmanById(sportsman_id):
    if not sportsman_id:
        return Sportsman()
    query = f"""SELECT id, name, surname, birthday, gender, photo, year,
                (SELECT SUM(score) FROM results WHERE sportsman_id = id) as score                 
                FROM sportsmen WHERE id = {sportsman_id}"""
    result = DbHelper.get_one_from_db(query)
    if result:
        return Sportsman(*result)
    return Sportsman()


def getSportsmen(gender=None, category_ages=None):
    query = """SELECT id, name, surname, birthday, gender, photo, year,
                (SELECT SUM(score) FROM results WHERE sportsman_id = id) as score FROM sportsmen"""
    if gender is not None or category_ages:
        query += " WHERE "
        if gender is not None:
            query += f" gender={gender}"
            if category_ages:
                query += " AND "
        if category_ages:
            current_year = datetime.now().year
            query += f""" ({current_year} - year) BETWEEN {category_ages[0]} AND {category_ages[1]}"""
    query += " ORDER BY score DESC, surname ASC"
    return [Sportsman(*row) for row in DbHelper.get_all_from_db(query)]


def deleteSportsmen(sportsman_id):
    if sportsman_id:
        DbHelper.execute_on_db(f'DELETE FROM sportsmen WHERE id = {sportsman_id}')
