from flask import Flask,render_template

app = Flask(__name__)

@app.route('/timetable')
def timetable():
    rows_one = [('UAL455','B739','San Francisco Intl (SFO)','00:13 PST','01:13 PST'),
              ('UAL455', 'B739', 'San Francisco Intl (SFO)', '00:13 PST', '01:13 PST')]
    rows_two = [('WJA1118', 'B738','Toronto Pearson Intl (YYZ)','22:44 EST','00:48 PST'),
                ('ROU1853',' A319','Toronto Pearson Intl (YYZ)','22:57 EST','00:50 PST')]
    rows_three = [('ROU1854',' 01:48 PST','08:19 EST','100'),
                  ('HAL17','01:57 PST','06:26 HST','97')]
    return render_template('timetable.html',rows_one = rows_one,rows_two = rows_two,rows_three=rows_three)

@app.route('/')
def flightflow():
    return render_template('flightflow.html')

if __name__ == '__main__':
    app.run()