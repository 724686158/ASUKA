# from django.shortcuts import render

# Create your views here.
import logging
import os

LOG = logging.getLogger(__name__)


def self_diagnose():
    """This function is used to check whether furion is running ok."""
    def _process_one(name):
        data = {
            "status": "OK",
            "name": name,
            "message": ""
        }
        try:
            globals()['_check_{}'.format(name)]()
            return data
        except Exception as e:
            LOG.error("Diagnose check error: {}".format(e))
            data['message'] = e.message
        data['status'] = "ERROR"
        return data

    def _cal_global_status(dt):
        assert isinstance(dt, list)
        for x in dt:
            assert isinstance(x, dict)
            if x.get('status') == 'ERROR':
                return 'ERROR'
        return 'OK'

    details = []
    for name in ['db']:
        details.append(_process_one(name))
    return {
        "details": details,
        "status": _cal_global_status(details)
    }


def dump_data():
    result = 'success'
    try:
        os.system('python dumpdata coil coil_data.json')
    except:
        result = 'fail'
    return {'dump coil data': result}


def load_data():
    result = 'success'
    try:
        os.system('python dumpdata coil_data.json')
    except:
        result = 'fail'
    return {'load coil data': result}


