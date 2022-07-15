from flask import Flask, request, jsonify
from scrape_nfds import scrape_nfds
import sys
application = Flask(__name__)


@application.route("/")
def hello():
    return "Hello goorm!"


@application.route('/line-fire', methods=['POST'])
def lineDetail():
    """
    강남전체 | 영등포전체
    강남, 광진 | 관악, 마포, 영등포 | 중부 | 혜북경기, 혜북서울
    """
    req = request.get_json()
    line = req['action']['detailParams']['LineFire']['value']
    region_cat = 'g' if line == '혜북경기' else 's'
    fire_msg = scrape_nfds(line, region_cat)
        
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": fire_msg
                    }
                }
            ]
        }
    }

    return jsonify(res)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, threaded=True)
