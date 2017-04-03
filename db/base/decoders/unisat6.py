#!/usr/bin/env python
from datetime import datetime


def decode_bytes(byte_array_temp):
    numberOfBitsToShiftBy = 0
    telemetryPointRaw = 0
    for byte in byte_array_temp:
        shiftedByte = byte << numberOfBitsToShiftBy
        telemetryPointRaw += shiftedByte
        numberOfBitsToShiftBy += 8
    return telemetryPointRaw


def find_sync_index(data):
    sync_bytes = bytearray([0x55, 0x53, 0x36])  # U S 6 0r 0x55 0x53 0x36
    packet_start_index = bytearray(data).find(sync_bytes)
    return packet_start_index


def decode_payload(payload, observation_datetime, data_id):
    payload = bytearray.fromhex(payload)
    # Find the sync bytes, reframe the packet to start after sync
    sync_offset = find_sync_index(payload)
    if sync_offset == -1:
        raise ValueError('No sync bytes found')
    else:
        payload = payload[sync_offset:len(payload)]

    telemetry = []

    packet_index = decode_bytes(payload[3:3 + 2])
    gnd_index_ack = decode_bytes(payload[5:5 + 2])
    packet_type = decode_bytes(payload[7:7 + 1])
    payload_size = decode_bytes(payload[8:8 + 1])
    reboot_cnt = decode_bytes(payload[9:9 + 2])
    if (packet_type == 1):
        uptime = decode_bytes(payload[11:11 + 4])  # in ms
        unix_time = decode_bytes(payload[15:15 + 4])  # in s
        temp_mcu = decode_bytes(payload[19:19 + 1])  # in C
        temp_fpga = decode_bytes(payload[20:20 + 1])  # in C
        magneto_x = decode_bytes(payload[21:21 + 2])  # in ?
        magneto_y = decode_bytes(payload[23:23 + 2])  # in ?
        magneto_z = decode_bytes(payload[25:25 + 2])  # in ?
        gyro_x = decode_bytes(payload[27:27 + 2])  # in ?
        gyro_y = decode_bytes(payload[29:29 + 2])  # in ?
        gyro_z = decode_bytes(payload[31:31 + 2])  # in ?
        i_cpu = decode_bytes(payload[33:33 + 2])  # in ?
        temp_radio = decode_bytes(payload[35:35 + 1])  # in C
        payload_reserved_0 = decode_bytes(payload[36:36 + 2])
        temp_bottom = decode_bytes(payload[38:38 + 1]) * 0.2  # in ?C
        temp_upper = decode_bytes(payload[39:39 + 1]) * 0.2  # in ?C
        payload_reserved_1 = decode_bytes(payload[40:40 + 1])
        eps_vbat = decode_bytes(payload[41:41 + 2])  # in mV
        i_eps_sun = decode_bytes(payload[43:43 + 2])  # in mA
        i_eps_out = decode_bytes(payload[45:45 + 2])  # in mA
        v_eps_panel1 = decode_bytes(payload[47:47 + 2])  # in mV
        v_eps_panel2 = decode_bytes(payload[49:49 + 2])  # in mV
        v_eps_panel3 = decode_bytes(payload[51:51 + 2])  # in mV
        i_eps_panel1 = decode_bytes(payload[53:53 + 2])  # in mA
        i_eps_panel2 = decode_bytes(payload[55:55 + 2])  # in mA
        i_eps_panel3 = decode_bytes(payload[57:57 + 2])  # in mA
        temp_eps_bat = decode_bytes(payload[59:59 + 2])  # in C
        payload_reserved_2 = decode_bytes(payload[61:61 + 1])
        sat_error_flag = decode_bytes(payload[62:62 + 2])
        sat_operation_status = decode_bytes(payload[64:64 + 1])
        sat_crc = decode_bytes(payload[65:65 + 1])

        data = {
            'satellite_datetime': datetime.fromtimestamp(
                int(unix_time)).strftime('%Y-%m-%d %H:%M:%S'),
            'observation_datetime': observation_datetime,
            'data_id': data_id,
            'demod_data': {
                'packet_index': packet_index,
                'gnd_index_ack': gnd_index_ack,
                'packet_type': packet_type,
                'payload_size': payload_size,
                'reboot_cnt': reboot_cnt,
                'uptime': uptime,
                'temp mcu': temp_mcu,
                'temp_fpga': temp_fpga,
                'magneto_x': magneto_x,
                'magneto_y': magneto_y,
                'magneto_z': magneto_z,
                'gyro_x': gyro_x,
                'gyro_y': gyro_y,
                'gyro_z': gyro_z,
                'i_cpu': i_cpu,
                'temp_radio': temp_radio,
                'payload_reserved_0': payload_reserved_0,
                'temp_bottom': temp_bottom,
                'temp_upper': temp_upper,
                'payload_reserved_1': payload_reserved_1,
                'eps_vbat': eps_vbat,
                'i_eps_sun': i_eps_sun,
                'i_eps_out': i_eps_out,
                'v_eps_panel1': v_eps_panel1,
                'v_eps_panel2': v_eps_panel2,
                'v_eps_panel3': v_eps_panel3,
                'i_eps_panel1': i_eps_panel1,
                'i_eps_panel2': i_eps_panel2,
                'i_eps_panel3': i_eps_panel3,
                'temp_eps_bat': temp_eps_bat,
                'payload_reserved_2': payload_reserved_2,
                'sat_error_flag': sat_error_flag,
                'sat_operation_status': sat_operation_status,
                'sat_crc': sat_crc
            }
        }

        telemetry.append(data)
        return telemetry
