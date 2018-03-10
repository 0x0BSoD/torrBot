import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def insert_to_bd(data):
    conn = sqlite3.connect('./base.bin')
    cur = conn.cursor()
    cur.execute('INSERT INTO `torrents`(`torr_id`,`name`,`data`, `finished`, `alerted`,`date`) VALUES (?,?,?,?,?,?)',
                data)
    conn.commit()
    conn.close()


def raw_to_bd(query):
    conn = sqlite3.connect('./base.bin')
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def get_by_torr_id(torr_id):
    conn = sqlite3.connect('./base.bin')
    cur = conn.cursor()
    cur.execute('SELECT `id`,* FROM `torrents` WHERE `torrents`.`torr_id`=?', (torr_id, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def update_state(torr_id):
    conn = sqlite3.connect('./base.bin')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('UPDATE `torrents` SET `finished`=1, `alerted`=1 WHERE `torrents`.`torr_id`=?', (torr_id, ))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result