from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/blog')
def blog():
    posts = [{'title': 'Post 1', 'content': 'This is the content of post 1. Lorem ipsum dolor sit amet.'},
            {'title': 'Post 2', 'content': 'This is the content of post 2. Lorem ipsum dolor sit amet.'}
            ]
    return render_template('blog.html', sunny=True, author='Serdar', posts=posts)


if __name__ == '__main__':
    app.run()

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
