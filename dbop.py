import sqlite3
# pid=3
# predictionss=1500
# with sqlite3.connect('database.db') as conn:
#     try:
#         cur = conn.cursor()
#         cur.execute('''INSERT INTO futuresales (productId,stock) VALUES (?, ?)''', (pid, predictionss))
#         conn.commit()
#         msg="added successfully"
#         print("Successful")
#     except:
#         msg="error occured"
#         cur = conn.cursor()
#         cur.execute("""UPDATE futuresales SET stock = ?  WHERE productId= ? """, (predictionss,pid))
#         print("Update Done")
#         conn.commit()
#         conn.rollback()
# conn.close()


# with sqlite3.connect('database.db') as conn:
#     try:
#         cur = conn.cursor()
#         cur.execute('''SELECT * FROM futuresales2''')
#         conn.commit()
#         ans=cur.fetchall()
#         print(ans)
#         msg="added successfully"
#         print("Successful")

#     except:
#         msg="error occured"
#         print(msg)
# conn.close()

with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    cur.execute('''DELETE FROM ordersss WHERE productId=2''')
    conn.commit()
    # ans=cur.fetchall()
    # print(ans)
    msg="added successfully"
    print("Successful")
conn.close()