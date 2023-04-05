
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    username = "root",
    password = "root",
)


cousor = mydb.cursor()
cousor.execute('create database  if not exists netdisk')
cousor.execute('use netdisk ')
cousor.execute('create table user(username varchar(128) primary key, password varchar(256)) ')
cousor.execute('create table folder(username text, foldername text, folderpath text) ')
cousor.execute('create table file(username text, filename text, filepath text) ')
cousor.execute('create table share(username text, filename text, filepath text) ')
cousor.execute('create table sharefile(username text, filename text, filepath text) ')
cousor.execute('create table sharefolder(username text, foldername text, folderpath text) ')


mydb.commit()
cousor.close()

