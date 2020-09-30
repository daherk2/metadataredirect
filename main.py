
from flask import Flask, request, send_from_directory
import uuid
import sqlite3

app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

def connecta():
    conn = None
    try:
        conn = sqlite3.connect("/home/metared/metadataredirect/db.sqlite")
    except Exception as e:
        print(e)
    return conn

def add_item(conn, link):
    sql = ''' INSERT INTO data_metadata(id,titulo,descricao,url) VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, link)
    conn.commit()
    conn.close()

def get_item(conn, idv):
    cur = conn.cursor()
    cur.execute("SELECT titulo,descricao,url FROM data_metadata WHERE id='"+str(idv)+"';")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/media/<path:path>')
def hoster(path):
    return send_from_directory('/home/metared/metadataredirect/media', path)

@app.route('/', methods=["GET", "POST"])
def main_app():
    if request.method == "POST":
        idv = str(uuid.uuid1()).replace("-", "")
        f = request.files['file']
        f.save("/home/metared/metadataredirect/media/"+str(idv) + ".png")
        temp = (
                str(idv),
                str(request.form.get('title')),
                str(request.form.get('desc')),
                str(request.form.get('url'))
                )
        conn = connecta()
        add_item(conn, temp)
        return open("/home/metared/metadataredirect/result.html").read().replace("XXXXX", str("?id=" + idv))
    else:
        idv = request.args.get('id')
        if idv != None:
            conn = connecta()
            rows = get_item(conn, str(idv))

            titulo = str(rows[0][0])
            desc = str(rows[0][1])
            url = str(rows[0][2])

            data = str(open("template.html", "r").read())
            data = data.replace("AAAAA", titulo)
            data = data.replace("BBBBB", desc)
            data = data.replace("CCCCC", str("http://metared.pythonanywhere.com/media/" + idv + ".png"))
            data = data.replace("DDDDD", url)
            data = data.replace("EEEEE", desc)
            data = data.replace("FFFFF", titulo)

            return data
        else:
            return str(open("/home/metared/metadataredirect/main.html", "r").read())

#if __name__ == "__main__":
#    app.run()