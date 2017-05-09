from datetime import datetime, timedelta
from flask import Flask, make_response
from io import BytesIO
from framework.base_user import db_session, Statistics
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure, SubplotParams
from configs.config_reader import get_config

config = get_config()

app = Flask(__name__)


def get_data(name):
    data = []
    for st in db_session.query(Statistics).filter(Statistics.day.like(datetime.today().strftime('%Y-%m-%d')))\
            .filter(Statistics.user_name.like(name)):
        data.append((st.user_name, st.issue_id, st.issue_subject, st.time_issue, st.day))

    return data


@app.route("/")
def index():
    return '<a href="Helgi S">Helgi S</a><br><a href="Anna K">Anna K</a>'


@app.route("/<string:name>")
def user_statistic(name):
    figure1 = Figure(
        figsize=(8, 8),
        dpi=100,
        facecolor='lavender',
        edgecolor='lavenderblush',
        linewidth=19.0,
        frameon=True,
        subplotpars=SubplotParams(left=0.2, bottom=0.2, right=0.8, top=0.8, wspace=0.1, hspace=0.1)
    )

    subplot3 = figure1.add_subplot(221, aspect='equal')
    label = ['Рабочий день']
    issue_time = [36000]
    db_data = get_data(name)
    if not db_data:
        return 'No data'
    for data in db_data:
        user_name, issue_id, issue_subject, time_issue, day = data

        issue_time.append(
            timedelta(hours=time_issue.hour, minutes=time_issue.minute, seconds=time_issue.second).total_seconds())
        label.append('{} ({})'.format(issue_id, issue_subject))

    subplot3.pie(issue_time, labels=label, shadow=True)

    subplot3.set_title('{} ({})'.format(user_name, day))

    canvas = FigureCanvas(figure1)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response


if __name__ == "__main__":
    app.run()
    # print(get_data())