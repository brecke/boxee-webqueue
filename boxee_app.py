from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from lib.boxee_api import BoxeeAPI

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return get_queue(request.form['username'], request.form['password'])
        else:
            error = 'Invalid username/password'
    else:
        show_login_form()
    
    # show login form with errors 
    return render_template('login.html', error=error)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error("Just stumbled upon a 404 error!")
    return render_template('page_not_found.html'), 404
    
@app.route('/delete/<id>', methods=['DELETE'])
def delete():
    # TODO
    # curl --url "http://app.boxee.tv/action/add" --data "<message type=\"dequeue\" referral=\"$item\"></message>" -H "Content-Type: text/xml" -u "$user":"$pass"
	pass
        
def valid_login(username, password):
    """docstring for valid_login"""
    if username and password:
        return True
    
    return False
	
def show_login_form():
    """"docstring for show_login_form"""
    return render_template('login.html')

def get_queue(username, password):
    """"docstring for get_queue"""
    app.logger.info("About to access boxee watch later queue for %s" %(username))
    api = BoxeeAPI(username, password)
    videos = api.get_videos()
    
    # debug printing
    print "Number of videos in queue: ", len(videos)
    return render_template('queue.html', videos=videos)

if __name__ == "__main__":
    app.run(debug=True)
    # To run beyond localhost
    # app.run(host='0.0.0.0')