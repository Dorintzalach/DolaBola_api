from flask import Flask, request, jsonify, Response, g
import json
from flask_cors import CORS
import pymysql.cursors


app = Flask(__name__)
CORS(app)


login = '648002e04ff1ab'
password = 'fbfa3b3ef2f9eb'
smtp_server = 'smtp.mailtrap.io'
port = '2525'
receiver = 'tzalach@post.bgu.ac.il'


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.before_request
def db_connect():
    g.conn = pymysql.connect(host='root.csrlcaaimlih.us-east-2.rds.amazonaws.com',
                          user='root',
                          password='Dola080990Bola220792',
                          db='DolaBola_DB',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    g.cursor = g.conn.cursor()

@app.after_request
def db_disconnect(response):
  g.cursor.close()
  g.conn.close()
  return response


def query_db(query, args=(), one=False):
  g.cursor.execute(query, args)
  rv = {}
  index = 0
  for row in g.cursor.fetchall():
      rv[index] = row
      index = index+1
  return rv

@app.route('/getAllBlogItems', methods=['POST'])
def getAllBlogItems():
    if request.method == "POST":
        try:
            result = query_db("SELECT * FROM blog_items")
            data = json.dumps(result)
            resp = Response(data, status=200, mimetype='application/json')
        except Exception as e:
            resp = Response(status=500, mimetype='application/json')
        return resp

@app.route('/updateBlogItemLikes', methods=['POST'])
def updateBlogItemLikes():
    if request.method == "POST":
        try:
            dict = request.get_json()
            likes = dict['likes_number']
            blog_item_id = dict['item_ID']
            params = (likes, blog_item_id)
            g.cursor.execute("UPDATE blog_items SET likes=%s where id=%s",params)
            g.conn.commit()
            resp = Response("Updated", status=200, mimetype='application/json')
        except Exception as e:
            resp = Response("something went wrong", status=500, mimetype='application/json')
        return resp

# update comments column in the wanted blog item(by blog item id)
@app.route('/updateBlogItemComments', methods=['POST'])
def updateBlogItemComments():
    if request.method == "POST":
        try:
            dict = request.get_json()
            blog_item_id = dict['item_ID']
            comment = dict['comment']
            params = (comment, blog_item_id)
            g.cursor.execute("UPDATE blog_items SET comments=%s where id=%s",params)
            g.conn.commit()
            resp = Response("Updated", status=200, mimetype='application/json')
        except Exception as e:
            resp = Response("something went wrong", status=500, mimetype='application/json')
        return resp

@app.route('/getRecentPosts', methods=['GET'])
def getRecentPosts():
    if request.method == "GET":
        try:
            result = query_db("select * from blog_items order by id desc limit 4")
            data = json.dumps(result)
            resp = Response(data, status=200, mimetype='application/json')
        except Exception as e:
                resp = Response(status=500, mimetype='application/json')
        return resp

@app.route('/getBlogItemById', methods=['GET'])
def getBlogItemById():
    if request.method == "GET":
        try:
            data = request.args
            blog_item_id = data['id']
            result = query_db("SELECT * FROM blog_items WHERE id=%s", args = blog_item_id)
            data = json.dumps(result)
            resp = Response(data, status=200, mimetype='application/json')
        except Exception as e:
            resp = Response("something went wrong", status=500, mimetype='application/json')
        return resp


# @app.route('/getGalleryImages', methods=['GET'])
# def getGalleryImages():
#     if request.method == "GET":
#         try:
#             cursor = mysql.connection.cursor()
#             cursor.execute('''SELECT * FROM images''')
#             res = cursor.fetchall()
#             resp = jsonify(res)
#             resp.status_code = 200
#             return resp
#         except Exception as e:
#             print(e)
#             resp.status_code = 500
#             return resp
#         finally:
#             mysql.connection.commit()
#             cursor.close()

# @app.route('/addBlogItem', methods=['PUT'])
# def addBlogItem():
#     if request.method == "PUT":
#         try:
#             data = request.get_json()
#             date = data['date']
#             title = data['title']
#             img = data['imagePath']
#             content = json.dumps(data['content'])
#             description = data['description']
#             params = (date, title, img, content, description)
#             cursor = mysql.connection.cursor()
#             cursor.execute('''INSERT INTO blog_items (date, title, img_path, content, description) VALUES(%s, %s, %s, %s, %s)''', params)
#             res = cursor.fetchall()
#             resp = jsonify(res)
#             resp.status_code = 200
#             return resp
#         except Exception as e:
#             print(e)
#             resp.status_code = 500
#             return resp
#         finally:
#             mysql.connection.commit()
#             cursor.close()


# @app.route('/addGalleryImage', methods=['PUT'])
# def addGalleryImage():
#     if request.method == "PUT":
#         try:
#             data = request.form
#             image_path = data['imagePath']
#             cursor = mysql.connection.cursor()
#             cursor.execute('''INSERT INTO images (image_url) VALUES(%s)''', [image_path])
#             res = cursor.fetchall()
#             resp = jsonify(res)
#             resp.status_code = 200
#             return resp
#         except Exception as e:
#             print(e)
#             resp.status_code = 500
#             return resp
#         finally:
#             mysql.connection.commit()
#             cursor.close()

# @app.route('/deleteGalleryImage', methods=['DELETE'])
# def deleteGalleryImage():
#     if request.method == "DELETE":
#         try:
#             data = request.form
#             image_id = data['imageID']
#             cursor = mysql.connection.cursor()
#             cursor.execute('''DELETE FROM images WHERE ID=%s''', [image_id])
#             res = cursor.fetchall()
#             resp = jsonify(res)
#             resp.status_code = 200
#             return resp
#         except Exception as e:
#             print(e)
#             resp.status_code = 500
#             return resp
#         finally:
#             mysql.connection.commit()
#             cursor.close()

# @app.route('/deleteBlogItem', methods=['DELETE'])
# def deleteBlogItem():
#     if request.method == "DELETE":
#         try:
#             data = request.form
#             blog_item_id = data['item_ID']
#             cursor = mysql.connection.cursor()
#             cursor.execute('''DELETE FROM blog_items WHERE id=%s''', [blog_item_id])
#             res = cursor.fetchall()
#             resp = jsonify(res)
#             resp.status_code = 200
#             return resp
#         except Exception as e:
#             print(e)
#             resp.status_code = 500
#             return resp
#         finally:
#             mysql.connection.commit()
#             cursor.close()

#
# @app.route('/sendEmail', methods=['POST'])
# def sendEmail():
#     if request.method == "POST":
#         try:
#             data = request.get_json()
#             sender = data['email']
#             message = data['messageContent']
#             sender_name = data['from']
#             # Type your message: use two newlines (\n) to separate the subject from the message body, and use 'f' to  automatically insert variables in the text
#             message = f"""\
#             Subject: Hi Mailtrap
#             To: {receiver}
#             From: {sender}
#             This is my first message with Python."""
#
#             try:
#                 # Send your message with credentials specified above
#                 with smtplib.SMTP(smtp_server, port) as server:
#                     server.login(login, password)
#                     server.sendmail(sender, receiver, message)
#             except Exception as e:
#                 # tell the script to report if your message was sent or which errors need to be fixed
#                 print('Failed to connect to the server. Bad connection settings?')
#             except smtplib.SMTPServerDisconnected:
#                 print('Failed to connect to the server. Wrong user/password?')
#             except smtplib.SMTPException as e:
#                 print('SMTP error occurred: ' + str(e))
#             else:
#                 print('Sent')
#             resp = Response("Updated", status=200, mimetype='application/json')
#         except Exception as e:
#             resp = Response("something went wrong", status=500, mimetype='application/json')
#         return resp


if __name__ == '__main__':
    app.run()