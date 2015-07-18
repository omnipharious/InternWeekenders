from datetime import datetime
import math

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.ext.stormpath import (
    StormpathError,
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey.properties'
app.config['STORMPATH_APPLICATION'] = 'InternWeekenders'

stormpath_manager = StormpathManager(app)

@app.route('/')
def main():
    return redirect(url_for('home'))


#@app.route('/add', methods=['POST'])
#@login_required
#def add_post():
 #   if not user.custom_data.get('posts'):
  #      user.custom_data['posts'] = []

   # user.custom_data['posts'].append({
    #    'date': datetime.utcnow().isoformat(),
     #   'title': request.form['title'],
      #  'text': request.form['text'],
   # })
    #user.save()

   # flash('New post successfully added.')
   # return redirect(url_for('show_posts'))


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/sites<int:page>')
def sites(page):
    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])
    #calculate the max amount of pages for the amount of posts
    total_pgs=math.ceil(len(posts)/3.0)
    #ensures that only 3 posts are shown per page        
    posts = posts[((page-1)*3):(((page-1)*3)+3)]
    return render_template('sites.html', posts=posts, page=page, max=total_pgs)

@app.route('/home')
def home():
    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])

    #ensures that only 3 posts are shown on the homepage        
    if len(posts) > 3:
        posts = posts[:3]        
    return render_template('index.html', posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        try:
            _user = User.from_login(
                request.form['email'],
                request.form['password'],
            )
            login_user(_user, remember=True)
            flash('You were logged in.')

            return redirect(url_for('home'))
        except StormpathError, err:
            error = err.message

    return render_template('login.html', error=error)


@app.route('/logout')
def signout():
    logout_user()
    flash('You were logged out.')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
