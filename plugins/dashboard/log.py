from flask_jwt import jwt_required
from influxdb import InfluxDBClient

from global_config import influx_host, influx_port
from utils.check_authority import permission_required
from . import api

influx_client = InfluxDBClient(influx_host, influx_port)
influx_client.create_database('nuc-info-log')
influx_client.query('CREATE RETENTION POLICY "1_day" ON "nuc-info-log" DURATION 1d REPLICATION 1 DEFAULT')
influx_client.query('CREATE RETENTION POLICY "1_day" ON "_internal" DURATION 1d REPLICATION 1 DEFAULT')

@api.route('/log')
@jwt_required()
@permission_required(['admin'])
def dashboard_log():
    res = influx_client.query('SELECT * FROM "root" ORDER BY time DESC LIMIT 30', database='nuc-info-log')
    data = []
    for i in res:
        for j in i:
            data.append({
                'time': j['time'],
                'level': j['level'],
                'message': j['message']
            })
    return {'code': 0, 'data': data}
