#!/usr/bin/env python
from datetime import datetime, timedelta

EPOCH_DATE = datetime.strptime('20000101T000000Z', '%Y%m%dT%H%M%SZ')


def decode_payload(payload, observation_datetime, data_id):
    dt = payload[:32]
    datasets = payload[32:]

    # calculate initial datetime
    seconds = int(dt[24:] + dt[16:24] + dt[8:16] + dt[:8], 2)

    telemetry = []

    while datasets:
        dataset = datasets[:57]
        datasets = datasets[57:]

        dataset_datetime = EPOCH_DATE + timedelta(seconds=seconds)
        seconds += 60
        satellite_datetime = datetime.strftime(dataset_datetime, '%Y%m%dT%H%M%SZ')

        # mode
        status = dataset[0]

        # battery voltage
        u = float(int(dataset[1:9], 2))
        bat_v = round((u + 60) / 20, 2)

        # battery current
        u = float(int(dataset[9:17], 2))
        bat_c = round((u - 127) / 127, 2)

        # 3v3 current
        u = float(int(dataset[17:25], 2))
        v3_c = round(u / 40, 2)

        # 5v current
        u = float(int(dataset[25:33], 2))
        v5_c = round(u / 40, 2)

        # temperature comms
        u = float(int(dataset[33:41], 2))
        comms_t = round((u - 60) / 4, 2)

        # temperature eps
        u = float(int(dataset[41:49], 2))
        eps_t = round((u - 60) / 4, 2)

        # temperature battery
        u = float(int(dataset[49:], 2))
        batt_t = round((u - 60) / 4, 2)

        data = {
            'satellite_datetime': satellite_datetime,
            'observation_datetime': observation_datetime,
            'data_id': data_id,
            'damod_data': {
                'status': status,
                'bat_v': bat_v,
                'bat_c': bat_c,
                'v3_c': v3_c,
                'v5_c': v5_c,
                'comms_t': comms_t,
                'eps_t': eps_t,
                'batt_t': batt_t
            }
        }

        telemetry.append(data)
        return telemetry
