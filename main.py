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


@login_required
@app.route('/post')
def post():

    return render_template('post.html')
	
@login_required	
@app.route('/read_more<string:post_name>')
def read_more(post_name):
	posts = []
	comments = []
	post_by_name = 0
	comments_by_id = []
	
	for account in stormpath_manager.application.accounts:
		if account.custom_data.get('posts'):
			posts.extend(account.custom_data['posts'])
	for post in posts:
		if post['title'] == post_name:
			post_by_name = post
	
	for account in stormpath_manager.application.accounts:
		if account.custom_data.get('comments'):
			comments.extend(account.custom_data['comments'])
			
	print comments
	
	for comment in comments:
		print comment['comment_id']
		print post_by_name['comment_id']
		if comment['comment_id'] == post_by_name['comment_id']:
			print comment
			comments_by_id.append(comment)
			
	print comments_by_id		
	return render_template('read_more.html', post_name = post_name, post = post_by_name, comments = comments_by_id)

# @login_required
@app.route('/edit<string:title>')
def edit(title):
    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])
    posts = sorted(posts, key=lambda k: k['date'], reverse=True)
    for post in posts:
        if post['title'] == title:
            new_post = post

    return render_template('edit.html',post=new_post)

@app.route('/submit', methods=['POST'])
def submit():
    if not user.custom_data.get('posts'):
        user.custom_data['posts'] = []

    user.custom_data['posts'].append({
        'date': datetime.utcnow().isoformat(),
        'title': request.form['title'],
        'location': request.form['location'],
        'crowd': request.form['crowd'],
        'activity': request.form['activity'],
        'expense': request.form['expense'],
        'blog': request.form['blog'],
        'user_email': str(user),
		'comment_id': "1234random"
        'vote': 0
    })
    user.save()
    print(user.custom_data['posts'])

    return redirect(url_for('sites', page=1,user=str(user)))

@app.route('/update<string:title>', methods=['POST'])
def update(title):
    if not user.custom_data.get('posts'):
        user.custom_data['posts'] = []

    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])
    posts = sorted(posts, key=lambda k: k['date'], reverse=True)

    del user.custom_data['posts'][:]

    for post in user.custom_data['posts']:
        i = 0
        if post['title'] == title and post['user_email'] == user:
            print(user.custom_data['posts'])
            del user.custom_data['posts'][i]

    user.custom_data['posts'].append({
        'date': datetime.utcnow().isoformat(),
        'title': request.form['title'],
        'location': request.form['location'],
        'crowd': request.form['crowd'],
        'activity': request.form['activity'],
        'expense': request.form['expense'],
        'blog': request.form['blog'],
        'user_email': str(user)
        'vote': 0
        
    })
    #print(user.custom_data['posts'])
    user.save()

    return redirect(url_for('sites', page=1))
	
@app.route('/comment<string:comment_id>', methods=['POST'])
@login_required
def comment(comment_id):
	if not user.custom_data.get('comments'):
		user.custom_data['comments'] = []
		
	comment = {
		'date': datetime.utcnow().isoformat(),
		'title': request.form['title'],
		'comment_text': request.form['comment'],
		'comment_id': comment_id
	}
	
	user.custom_data['comments'].append(comment)
	user.save()
	'''
	posts = []
	post_by_name = 0
	for account in stormpath_manager.application.accounts:
		if account.custom_data.get('posts'):
			posts.extend(account.custom_data['posts'])
	for post in posts:
		if post['comment_id'] == comment_id:
			post_by_id = post
	'''		
	return redirect(url_for('sites', page = 1))



@app.route('/votes<string:title>', methods = ['POST'])
def votes(title):
    if not user.custom_data.get('posts'):
        user.custom_data['posts'] = []

    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])
    posts = sorted(posts, key=lambda k: k['date'], reverse=True)

    for post in user.custom_data['posts']:
        i = 0
        print(post['title'])
        print(title)
        if post['title'] == title:
            print("inside")
            post['vote'] += 1
            new_post = post
            print(new_post)

    return redirect(url_for('sites', page=1, new_post=new_post))
    # return render_template(url_for('post.html'))

@app.route('/delete<string:title>')
def delete(title):
    if not user.custom_data.get('posts'):
        user.custom_data['posts'] = []

    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])
    posts = sorted(posts, key=lambda k: k['date'], reverse=True)

    print(user.custom_data['posts'])
    del user.custom_data['posts'][:]

    for post in user.custom_data['posts']:
        i = 0
        if post['title'] == title and post['user_email'] == user:
            print(user.custom_data['posts'])
            del user.custom_data['posts'][i]

    user.save()

    return render_template('delete.html', title=title)

    # if not user.custom_data.get('posts'):
    #     user.custom_data['posts'] = []
    #
    # posts = []
    # for account in stormpath_manager.application.accounts:
    #     if account.custom_data.get('posts'):
    #         posts.extend(account.custom_data['posts'])
    # posts = sorted(posts, key=lambda k: k['date'], reverse=True)
    #
    # print(user.custom_data['posts'])
    # del user.custom_data['posts'][:]
    #
    # for post in user.custom_data['posts']:
    #     i = 0
    #     if post['title'] == title and post['user_email'] == user:
    #         print(user.custom_data['posts'])
    #         del user.custom_data['posts'][i]
    #
    # print(user.custom_data['posts'])
    # user.save()
    #
    # return redirect(url_for('sites', page=1))

@login_required
@app.route('/sites<int:page>')
def sites(page):
    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])
    posts = sorted(posts, key=lambda k: k['date'], reverse=True)
    #calculate the max amount of pages for the amount of posts
    total_pgs=math.ceil(len(posts)/3.0)
    #ensures that only 3 posts are shown per page        
    posts = posts[((page-1)*3):(((page-1)*3)+3)]
    return render_template('sites.html', posts=posts, page=page, max=total_pgs, user1=str(user))

@app.route('/home')
def home():
    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])
    posts = sorted(posts, key=lambda k: k['date'], reverse=True)
    #ensures that only 3 posts are shown on the homepage        
    if len(posts) > 3:
        posts = posts[:3]        
    return render_template('index.html', posts = posts )

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
