from flask import Flask, render_template, flash, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor
import yaml
import os

app = Flask(__name__)
Bootstrap (app)
CKEditor(app)

#Configure DB
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM blogs")
    if resultValue > 0:
        blogs = cur.fetchall()
        cur.close()
        return render_template('index.html', active='home', blogs=blogs)
    cur.close()
    return render_template("index.html", active='home', blogs=None)

@app.route('/about')
def about():
    return render_template("about.html", active='about')


@app.route('/blogs/<int:id>/')
def blogs(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM blogs WHERE UBR = {}".format(id))
    if resultValue > 0:
        blogs = cur.fetchone()
        return render_template('blogs.html', active='blogs', blogs=blogs)
    return 'Blog not found'

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        print(userDetails)
        if userDetails['Password'] != userDetails['ConfirmPassword']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register.html', active='register')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(FirstName, LastName, Username, Email, Password) "\
        "VALUES(%s,%s,%s,%s,%s)",(userDetails['FirstName'], userDetails['LastName'],
        userDetails['Username'], userDetails['Email'], generate_password_hash(userDetails['Password'])))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    return render_template("register.html", active='register')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form 
        username = userDetails['Username']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM users WHERE Username = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if check_password_hash(user['Password'], userDetails['Password']):
                session['login'] = True
                session['first_name'] = user['FirstName']
                session['last_name'] = user ['LastName']
                flash('Welcome ' + session['first_name'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login.html', active='login')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html', active='login')
        cur.close()
        return redirect('/')
    return render_template('login.html', active='login')

@app.route('/write-blog', methods=['GET', 'POST'])
def writeblog():
    if request.method == 'POST':
        blogpost = request.form
        title = blogpost['BlogTitle']
        body = blogpost['ckeditor']
        author = session['first_name'] + ' ' + session['last_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blogs(title, body, author) VALUES(%s, %s, %s)", (title, body, author))
        mysql.connection.commit()
        cur.close()
        flash("Successfully posted new blog", 'success')
        return redirect('/')
    return render_template('write-blog.html', active='writeblog')


@app.route('/my-blogs/')
def myblogs():
    author = session['first_name'] + ' ' + session['last_name']
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM blogs WHERE author = %s",[author])
    if result_value > 0:
        my_blogs = cur.fetchall()
        return render_template('my-blogs.html', active='myblogs', my_blogs=my_blogs)
    else:
        return render_template('my-blogs.html', active='myblogs', my_blogs=None)


@app.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
def editblog(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        Title = request.form['blogTitle']
        Body = request.form['blogBody']
        cur.execute("UPDATE blogs SET Title = %s, Body = %s where UBR = %s",(Title, Body, id))
        mysql.connection.commit()
        cur.close()
        flash('Blog updated successfully', 'success')
        return redirect('/blogs/{}'.format(id))
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM blogs WHERE UBR = {}".format(id))
    if result_value > 0:
        blog = cur.fetchone()
        blog_form = {}
        blog_form['blogTitle'] = blog['Title']
        blog_form['blogBody'] = blog['Body']
    return render_template('edit-blog.html', active='editblog', blog_form=blog_form)


@app.route('/delete-blog/<int:id>/')
def deleteblog(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM blogs WHERE UBR = {}".format(id))
    mysql.connection.commit()
    flash("Your blog post has been deleted", 'success')
    return redirect('/my-blogs')
    


@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    # The port number above is defalut 5000 but
    # changed it as part of the course to point out it can be changed manually
