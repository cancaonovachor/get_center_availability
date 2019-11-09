import os
import centers.nishinomiya_center as nishinomiya
from flask import Flask, request

app = Flask(__name__)

@app.route('/nishinomiya')
def get_center_nishinomiya():
    if request.args and 'reservMon' in request.args:
        reservMon = request.args.get('reservMon')
    else:
        return "必須項目をリクエストクエリに含めてください"

    if request.args and 'reservDay' in request.args:
        reservDay = request.args.get('reservDay')
    else:
        return "必須項目をリクエストクエリに含めてください"

    return nishinomiya.get_nishinomiya_center_availability(reservMon, reservDay)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))