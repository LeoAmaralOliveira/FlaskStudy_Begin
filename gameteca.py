from flask import Flask, render_template


class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


app = Flask(__name__)


@app.route('/home')
def hello_world():
    game_list = [
        Game('Tetris', 'Puzzle', 'Atari'),
        Game('God Of War', 'Rack n Slash', 'PS3'),
        Game('Skyrim', 'RPG', 'PC'),
        Game('Crash Bandicoot', 'Adventure', 'PS1'),
        Game('Valorant', 'FPS', 'PC'),
        Game('Mortal Kombat', 'Fight', 'PS2')
    ]

    return render_template('list.html', title='GameTeca', games=game_list)


app.run(host='0.0.0.0', port=8000)
