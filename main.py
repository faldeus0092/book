from distutils.log import debug
from website import create_app

app = create_app()

# run if the file executed
if __name__ == '__main__':
    app.run(debug=True)