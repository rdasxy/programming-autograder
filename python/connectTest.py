import pymysql
def getConnection():
    params = {'host':'KC-csrv-mysql', "user":"SCEAutoGrdr",
             "passwd":"XNHyJ9V4HTaC","db":"SCE-AutoGrdr", "use_unicode": True}
    return pymysql.connect(**params)

connect = getConnection()
cursor = connect.cursor()
cursor.execute("SELECT * FROM Roll")
with open('connectTest.txt', 'w') as fout:
        answer = cursor.fetchone()
        fout.write(str(answer)+'\n')
connect.close()
