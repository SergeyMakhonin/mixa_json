from flask import Flask, request, render_template, make_response, session, redirect, url_for
from logging_and_configuration import log

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/main', methods=['GET'])
def main():
    # get teams from StorageApp
    guest_team = 'team1'
    local_team = 'team2'

    # make response with cookies
    response = make_response(render_template('main.html', title='Main', guest_team=guest_team, local_team=local_team))
    return response


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get user/pass from form
        session['username'] = request.form['username']
        session['password'] = request.form['password']

        # check user/pass pair
        # TODO check user via StorageApp
        # TODO check password via StorageApp for checked user

        # if check are OK redirect to Main, else abort(403)
        return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    # start reaping
    log('Starting to reap...')
    app.run(debug=False)
