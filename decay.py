#!/usr/bin/env python

import MySQLdb
import datetime
from flask import Flask, render_template, request, make_response, abort
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def addNew():
    outboundurl = request.form["outboundurl"]
    conn = MySQLdb.connect(host="localhost", user="", passwd="", db="decay")

    # Prepare url string
    if "//" not in outboundurl:
        outboundurl = "".join(["//", outboundurl])
    outboundurl = conn.escape_string(outboundurl)

    cur = conn.cursor()
    cur.execute("""INSERT INTO urlmap (decaytime, target) VALUES (ADDTIME(NOW(), '0:2:0'), %s)""", (outboundurl,))
    insert_id = conn.insert_id()
    conn.commit()

    return render_template("add.html", url=insert_id)

@app.route('/<int:urlkey>')
def forward(urlkey):
    conn = MySQLdb.connect(host="localhost", user="", passwd="", db="decay")

    # Get the matching URL, if any
    cur = conn.cursor()
    cur.execute("""SELECT target FROM urlmap WHERE id=%s AND decaytime > NOW() LIMIT 1""", (urlkey,))
    result = cur.fetchone()

    if result == None:
        abort(404)

    resp = make_response(render_template("forward.html", url=result), 307)
    resp.headers['Location'] = result[0]
    return resp

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
