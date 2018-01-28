import math
import sys
import sqlite3 as sqli
from socket import *

def is_prime(val):
    for i in range(2, int(math.sqrt(val) + 1)):
        if (val % i) == 0:
            return False
    return True

def nth_prime(n, i=0, val=2):
    while i < n:
        if is_prime(val):
            i += 1
            if i == n:
                return val
        val += 1

def db_get_prime(n, con):
    try:
        cur = con.cursor()
        #lookup n in db
        db_res = cur.execute('SELECT val FROM primes WHERE n=?', (n,)).fetchall()

        if len(db_res) != 0: #prime is in db, return value
            prime = db_res[0][0]
            print(prime)
            return prime
        else: #compute prime
            #get nearest
            db_res = cur.execute("""SELECT n, val FROM primes WHERE
                                     n=(SELECT max(n) FROM primes)
                                  """).fetchall()
            if len(db_res) != 0:
                _n, _val = db_res[0]
            else:
                _n = 1
                _val = 2
            #compute prime
            prime = nth_prime(int(n), _n - 1, _val)
            print(prime)
            #insert value into table
            insert = (n, prime)
            cur.execute('INSERT INTO primes (n, val) VALUES (?, ?)', (n, prime))
            return prime
    except sqli.Error as e:
        print('db_get_prime: An error occurred using sqlite ->', e)
        return 0

def db_init(db_file):
    #connect to db file
    try:
        con = sqli.connect(db_file) #make db file
        cur = con.cursor()

        #check if table exists
        create = True
        tables = cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = tables.fetchall()
        for t in tables:
            if t[0] == 'primes':
                create = False

        #create table if it doesn't exist
        if create:
            #create table
            cur.execute("""
                CREATE TABLE primes(
                  n INTEGER PRIMARY KEY,
                  val INTEGER
                )
            """)
            con.commit() #save
    except sqli.Error as e:
        print('db_init: An error occurred using sqlite ->', e)
        return False

    return con

def main():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', 12000))

    con = False
    if len(sys.argv) == 2:
        con = db_init(sys.argv[1])

    print("Server On")
    while True:
        message, address = serverSocket.recvfrom(1024)

        print("Message from", address, ":", message)

        # n =  re.sub("[^0-9]", "", str(message))
        n = str(message)[2:-1]
        prime = -1

        if con:
            prime = db_get_prime(n, con)
        else:
            prime = nth_prime(int(n))

        response = str(prime)
        serverSocket.sendto(str.encode(response), address)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer Off")
