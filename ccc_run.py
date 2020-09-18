from ccc_pkg import app, db
from ccc_pkg.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# Set Debug=False before live production
if __name__ == '__main__':
    app.run(debug=True)