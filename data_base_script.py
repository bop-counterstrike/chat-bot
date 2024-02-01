import sqlite3

conn = sqlite3.connect('bd.sql')
cur = conn.cursor()
'''cur.executescript("""
    CREATE TABLE prices ( 
    type_ varchar(50) primary key,
    price int
    )""")'''
cur.execute('SELECT * FROM date_time')
print(cur.fetchall())
'''cur.execute("""SELECT wl.dt_date, wl.dt_time, cl.first_name, cl.last_name, cl.phone_n 
FROM work_list wl, clients cl
WHERE wl.cl_number = cl.phone_n""")
print(cur.fetchall())'''
'''cur.executescript("""
    INSERT INTO prices(type_, price) VALUES ('Комби-маникюр', 450);
    INSERT INTO prices(type_, price) VALUES ('Маникюр + однотонное покрытие', 900);
    INSERT INTO prices(type_, price) VALUES ('Маникюр + покрытие + дизайн', 1000);
    INSERT INTO prices(type_, price) VALUES ('Снятие', 200);
    INSERT INTO prices(type_, price) VALUES ('Укрепление ногтей', 200);
    INSERT INTO prices(type_, price) VALUES ('Ремонт одного ногтя', 50);
    INSERT INTO prices(type_, price) VALUES ('Френч', 1200);
""")'''
'''cur.executescript("""PRAGMA foreign_keys=on;
    CREATE TABLE clients ( 
    phone_n char(10) primary key,
    first_name varchar(50), 
    last_name varchar(50)
    );
    
    CREATE TABLE date_time (
    date_ date,
    time_ time,
    CONSTRAINT dt_pk PRIMARY KEY (date_, time_)
    );
    
    CREATE TABLE work_list (
    wl_id integer primary key autoincrement,
    cl_number char(10),
    dt_date date,
    dt_time time,
    FOREIGN KEY (cl_number) REFERENCES clients (phone_n),
    FOREIGN KEY (dt_date, dt_time) REFERENCES date_time (date_, time_)
    )
""")'''
conn.commit()
cur.close()
conn.close()
