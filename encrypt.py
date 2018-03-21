#!/bin/python

import subprocess as sub
import mysql.connector
import aes
import getpass


class theApp():

    def __init__(self):

        # self.crypt_pass = 'password'
        self.crypt_pass = getpass.getpass("crypt password: ")

        with open("config") as fop:
            cont = fop.readlines()
            cont = [x.strip() for x in cont]
            self.sql_user = cont[0]
            self.sql_pass = cont[1]
            self.sql_host = cont[2]
            self.sql_db = cont[3]
        fop.close()

        self.sql_config = {
            'user': self.sql_user,
            'password': self.sql_pass,
            'host': self.sql_host,
            'database': self.sql_db,
            'raise_on_warnings': True,
        }

    def connect_db(self):
        self.con = mysql.connector.connect(**self.sql_config)
        self.cur = self.con.cursor()

    def disconnect_db(self):
        self.con.close()
        self.cur.close()

    def fetch_data(self):
        self.query = ("SELECT id, site, passw, date FROM passd ORDER BY id")
        self.cur.execute(self.query)
        for (id, site, passw, date) in self.cur:
            print(id, site, self.decrypt(self.crypt_pass, passw), date)

    def insert_new(self, url, password):
        self.insert = ("INSERT INTO passd\
        " "(site, passw)\
        " "VALUES (%(site)s, %(passw)s)")
        self.data = {
            'site': url,
            'passw': self.encrypt(self.crypt_pass, password),
        }
        self.cur.execute(self.insert, self.data)

    def encrypt(self, password, message):
        crypt = aes.AESCipher(password).encrypt(message)
        return crypt

    def decrypt(self, password, message):
        decrypt = aes.AESCipher(password).decrypt(message)
        return decrypt


start = theApp()
start.connect_db()
# start.insert_new('test.com', 'anotherpass')

start.fetch_data()
start.disconnect_db()
