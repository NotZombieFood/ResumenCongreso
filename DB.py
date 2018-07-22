import MySQLdb
db = MySQLdb.connect("52.171.56.64","root","Perritofeliz@1","Semestrei" )
cursor = db.cursor()

def updateCount(title,good_summary):
    if(good_summary):
        sql = "UPDATE entries SET vote_yes = vote_yes + 1 WHERE title = %d" % (title)
    else:
        sql = "UPDATE entries SET vote_no = vote_no + 1 WHERE title = %d" % (title)
    try:
        cursor.execute(sql)
        db.commit()
        response = 1
    except:
        response = 0
        db.rollback()
    return response
