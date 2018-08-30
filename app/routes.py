import datetime
from flask import render_template, request
from app import app
from app.utils import get_data, put_data, make_weeklycount


@app.route('/')
def addactivity():
    """
    Return the training template with today's date.
    """
    today = datetime.date.today().isoformat()
    return render_template('addactivity.html', today=today, title='Add activity')


@app.route('/result', methods=['POST', 'GET'])
def addedresult():
    """
    Return the results from the training template and update airtable
    """
    if request.method == 'POST':
        result = request.form
        put_data(result)
        return render_template("resultadded.html", result=result, title='Activity added')


@app.route('/stats/<int:num_weeks>')
def stats(num_weeks):
    """
    Return the graph with the number of training sessions per sport
    """
    if num_weeks <= 0:
        num_weeks = 1
    data = make_weeklycount(get_data(num_weeks))
    return render_template('stats.html', num_weeks=num_weeks, data=data, title='Stats')


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


