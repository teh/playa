import os
import flask
import jinja2
import json
import argparse

app = flask.Flask(__name__)
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./templates'),
    variable_start_string='[[',
    variable_end_string=']]',
)

def is_music(f):
    return f.lower().endswith('mp3')


@app.route('/m/<path:path>')
def m(path):
    return flask.Response(
        open('/' + path).read(),
        200,
        headers={
            'Accept-Ranges':'bytes',
        },
        mimetype='audio/mpeg',
    )

@app.route('/music')
def all_music():
    songs = []
    for dir, dirs, files in os.walk(app.config.music_path):
        for filename in files:
            path = os.path.join(dir, filename)
            if not is_music(path):
                continue
            songs.append({
                'title': unicode(os.path.basename(path), errors='ignore'),
                'path': unicode(path, errors='ignore'),
            })
                        
    data = {
        'songs': sorted(songs, key=lambda x: x['path']),
    }
    return flask.Response(
        json.dumps(data),
        mimetype='application/json',
    )

@app.route('/')
def serve():
    return env.get_template('serve.html').render()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export music collection.')
    parser.add_argument(
        'music_path', metavar='MUSIC_PATH', type=str,
        help='root of your music collection'
    )

    args = parser.parse_args()

    app.config.music_path = args.music_path
    app.run(host='0.0.0.0', port=8000, threaded=True)
