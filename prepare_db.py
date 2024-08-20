import mysql.connector
from mysql.connector import errorcode
from pathlib import os
import socket
from dotenv import load_dotenv


load_dotenv()


def init_db():
    print("Connecting...")
    try:
        conn = mysql.connector.connect(
            host=".".join(socket.gethostbyname(socket.gethostname()).split(".")[:-1] + ["1"]), # NoQa
            user=str(os.getenv("MYSQL_USERNAME")),
            password=str(os.getenv("MYSQL_PW")),
            database='gameteca',
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('There`s something wrong with user or password')
        else:
            print(err)

    cursor = conn.cursor()

    TABLES = {}
    TABLES['Games'] = (
        '''
        CREATE TABLE IF NOT EXISTS `games` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(50) NOT NULL,
        `category` varchar(40) NOT NULL,
        `console` varchar(20) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
    )

    TABLES['Users'] = (
        '''
        CREATE TABLE IF NOT EXISTS `users` (
        `name` varchar(20) NOT NULL,
        `username` varchar(20) NOT NULL,
        `password` varchar(100) NOT NULL,
        PRIMARY KEY (`username`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
    )

    for tabela_nome in TABLES:
        tabela_sql = TABLES[tabela_nome]
        try:
            print('Creating table {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Already exists')
            else:
                print(err.msg)
        else:
            print('OK')

    conn.commit()

    cursor.close()
    conn.close()
