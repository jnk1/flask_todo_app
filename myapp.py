# coding: utf-8

from flask import Flask, redirect, render_template, request, url_for
import pymysql

app = Flask(__name__) # Flaskアプリケーションを作成

conn = pymysql.connect(host='localhost', user='root', password='', db='mydb',
        autocommit=True, # データ追加・変更時に自動的に保存(コミット)
        cursorclass=pymysql.cursors.DictCursor # 検索結果を辞書として受け取れるようにDictCursorを指定
        )
db = conn.cursor()

# トップページとなるルートパス("/")に対するアクションを指定
# "@app.route('/')"のようなデコレータを利用して、
# URLのパス名("/")とアクション(index関数)の対応づけを行う
@app.route('/')
def index():
    db.execute('SELECT * FROM todos')
    todos = db.fetchall() # SQLの実行結果は、db.fetchall()関数で取得
    # render_template()で"index.html"テンプレートを読み込みます。
    # 第二引数に"todos = todos"と指定することで、
    # テンプレート中の"todos"変数で、ToDo一覧を参照できるようにする。
    return render_template('index.html', todos = todos)

@app.route('/create', methods=('POST',))
def create():
    # "request.form['name']"で、
    # テキスト入力フォームから送信された追加ToDoの値を取得して、name変数に保存
    name = request.form['name']
    # SQL文中の"%s"のように指定された場所を第二引数の値(name)で置き換えることができる
    # 直接文字列を生成せずに"%s"を経由することでエスケープ処理を確実に行い、SQLを安全に実行できる
    db.execute('INSERT INTO todos(name) VALUES (%s)', (name,))
    # SQL実行後は、redirect_forでトップページにリダイレクト。
    # url_for('index')とurl_forを使うことで、
    # 直接URLではなくアクション名で指定できるため、より柔軟なコードになります。
    return redirect(url_for('index'))

# パス名で"/＜int:id＞/delete"のように指定すれば、
# deleteの引数でToDoのidを受け取れる
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db.execute('DELETE FROM todos WHERE id = %s', (id,))
    return redirect(url_for('index'))

# Flaskアプリケーションを実行。
# Flaskアプリケーションはデフォルトで5000番ポート
# デバッグモードで実行
app.run(debug=True)