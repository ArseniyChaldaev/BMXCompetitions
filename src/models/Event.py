from datetime import datetime

from GlobalVars import POSITION
from utils import DbHelper

def getStartList(competition_id):
    query = f"""SELECT startlist.id, competition_id, startlist.gender, category_id, race_type, race_number, 
                        sportsman_id, sportsmen.surname, sportsmen.name, start_position, finish_position 
                        FROM startlist INNER JOIN sportsmen ON startlist.sportsman_id = sportsmen.id 
                        WHERE startlist.competition_id = {competition_id}"""
    result = DbHelper.get_all_from_db(query)
    dic = dict()
    for row in result:
        startlist_id = row[0]
        gender, category_id = row[2], row[3]
        if (gender, category_id) not in dic:
            dic[(gender, category_id)] = dict()
        race_type = row[4]
        if race_type not in dic[(gender, category_id)]:
            dic[(gender, category_id)][race_type] = dict()
        race_number = row[5]
        if race_number not in dic[(gender, category_id)][race_type]:
            dic[(gender, category_id)][race_type][race_number] = list()
        sportsman_id, full_name, start_position, finish_position = row[6], ' '.join([row[7], row[8]]), row[9], row[10]
        dic[(gender, category_id)][race_type][race_number].append([sportsman_id,
                                                                   full_name,
                                                                   start_position,
                                                                   finish_position,
                                                                   startlist_id])
    return dic


def createStartList(competition_id):
    current_year = datetime.now().year
    categories = DbHelper.get_all_from_db("SELECT id, min_age, max_age FROM categories")
    values_list = list()
    for category_id, min_age, max_age in categories:
        for gender_id in [1, 0]:
            sportsmen = DbHelper.get_all_from_db(f"""SELECT id, 
                    (SELECT SUM(score) FROM results WHERE sportsman_id = id) as score 
                    FROM sportsmen WHERE gender={gender_id} 
                    AND ({current_year} - year) BETWEEN {min_age} AND {max_age} 
                    ORDER BY score DESC, surname ASC""")
            if len(sportsmen) == 0:
                continue
            race_count = (len(sportsmen) - 1) // 8 + 1
            race_number, d = 1, 1
            for i, man in enumerate(sportsmen):
                values_list.append((competition_id, gender_id, category_id, 1,
                                    race_number, man[0], POSITION[i // race_count][0]))
                values_list.append((competition_id, gender_id, category_id, 2,
                                    race_number, man[0], POSITION[i // race_count][1]))
                values_list.append((competition_id, gender_id, category_id, 3,
                                    race_number, man[0], POSITION[i // race_count][2]))
                race_number += d
                if race_number > race_count:
                    race_number = race_count
                    d = -1
                    continue
                if race_number == 0:
                    race_number = 1
                    d = 1
    DbHelper.execute_many_on_db("""INSERT INTO startlist 
                            (competition_id, gender, category_id, race_type, race_number, sportsman_id, start_position) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)""", values_list)
    return getStartList(competition_id)


def createNextRoundStartList(competition_id, values_list):
    DbHelper.execute_many_on_db("""INSERT INTO startlist 
                            (competition_id, gender, category_id, race_type, race_number, sportsman_id, start_position) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?)""", values_list)
    return getStartList(competition_id)


def saveResult(values_list):
    try:
        DbHelper.execute_many_on_db("""INSERT INTO results
                                (competition_id, gender, category_id, sportsman_id, position, score) 
                                    VALUES (?, ?, ?, ?, ?, ?)""", values_list)
    except Exception as ex:
        print(ex)


def getResults(competition_id, gender, category_id):
    query = f"""SELECT results.sportsman_id, sportsmen.surname, sportsmen.name, 
                        position, score FROM results INNER JOIN sportsmen ON results.sportsman_id = sportsmen.id 
                            WHERE results.competition_id = {competition_id} AND results.gender = {gender}
                            AND results.category_id = {category_id}"""
    result = DbHelper.get_all_from_db(query)
    lst = []
    for row in result:
        sportsman_id, full_name, position, score = row[0], ' '.join([row[1], row[2]]), row[3], row[4]
        lst.append([sportsman_id, full_name, position, score])
    return lst


def updateStartList(positions):
    for position in positions:
        DbHelper.execute_on_db(f"UPDATE startlist SET finish_position=? WHERE id=?", position)


def getAllResults(year, gender, category_id):
    query = f"SELECT id, title, date FROM competitions WHERE year = {year} ORDER BY date"
    competitions = DbHelper.get_all_from_db(query)
    competitions = sorted(competitions, key=lambda x: f"{x[2][6:]}{x[2][3:5]}{x[2][0:3]}")
    competition_ids = {int(row[0]): i for i, row in enumerate(competitions)}
    header = ['Фамилия Имя'] + [row[1] for row in competitions] + ['Очки']
    query = f"""SELECT results.sportsman_id, sportsmen.surname, sportsmen.name,
                       competition_id, position, score
                        FROM results INNER JOIN sportsmen
                        ON results.sportsman_id = sportsmen.id INNER JOIN competitions
                        ON results.competition_id = competitions.id
                            WHERE results.gender = {gender} AND results.category_id = {category_id}"""
    result = DbHelper.get_all_from_db(query)
    dic = dict()
    for row in result:
        sportsman_id = row[0]
        competition_id = int(row[3])
        if competition_id not in competition_ids:
            continue
        if sportsman_id not in dic:
            dic[sportsman_id] = [' '.join([row[1], row[2]])] + [0] * (len(competitions) + 1)
        dic[sportsman_id][competition_ids[competition_id] + 1] = int(row[4])
        dic[sportsman_id][-1] += int(row[5])
    data = sorted(list(dic.values()), key=lambda x: -x[-1])
    return data, header
