import sqlite3

class BancoDadosHelper():
    
    @staticmethod
    def get_connection():
        return sqlite3.connect('bd_busca_academica.db')