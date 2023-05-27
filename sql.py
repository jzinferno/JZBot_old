#!/usr/bin/env python3

from tabulate import tabulate
import sys, sqlite3, readline

def writecmd(database, command):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    try:
        cursor.execute(command)
        result = cursor.fetchall()
        if result != []:
            print(result)
        else:
            connect.commit()
    except:
        print('Syntax error!')
    connect.close()

def show_table(database, tablename):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    try:
        cursor.execute('SELECT name FROM pragma_table_info(\'{}\')'.format(tablename))
        headers = [column[0] for column in cursor.fetchall()]
        cursor.execute('SELECT * FROM {}'.format(tablename))
        print(tabulate(cursor.fetchall(), headers, tablefmt='simple_grid'))
    except:
        print('Error read table')
    connect.close()

def tables(database):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    try:
        cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
        print(tabulate(cursor.fetchall(), tablefmt='simple_grid'))
    except:
        print('Error read tables list')
    connect.close()

def main():
    while True:
        command = input('{} > '.format(sys.argv[1])).split()
        if len(command) < 1:
            pass
        elif command[0] == 'clear':
            print('\33[3J\33[H\33[2J')
        elif command[0] == 'exit':
            break
        elif command[0] == 'tables':
            tables(sys.argv[1])
        elif command[0] == 'show' and len(command) == 2:
            show_table(sys.argv[1], command[1])
        else:
            writecmd(sys.argv[1], ' '.join(command))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            main()
        except:
            print('')
    else:
        print('Usage {} <name.db>'.format(sys.argv[0]))
