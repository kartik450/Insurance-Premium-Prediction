import mysql.connector as mc 
### first method connection
# try:
# config={'user':'root','password':'Jigar@975919','host':'localhost','port':3306}
conn=mc.connect(host ='localhost' , user = 'root' , password = '8003117245Kj?')
if(conn.is_connected()):
    print('jai ho mata Rani')
else:
    print('unable to connect')