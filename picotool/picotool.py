import subprocess
import re


INFO_GROUP_MAP = {
    'Program Information': 'program',
    'Fixed Pin Information': 'pins',
    'Build Information': 'build',
    'Device Information': 'device',
}

DEVICE_REGEX = r'bus (\d*), address (\d*):'


def _process_info_groups(groups, output):
    for group in groups:
        lines = group.split('\n')
        if len(lines) == 0:
            continue

        long_name = lines.pop(0)
        if long_name not in INFO_GROUP_MAP:
            raise Exception('Unknown group name "%s"' % long_name)

        name = INFO_GROUP_MAP[long_name]

        fields = {}
        for line in lines:
            parts = line.split(':', 1)
            key = parts.pop(0).strip()
            if len(key) == 0:
                continue

            # normalize keys
            key = key.lower()
            key = key.replace(' ', '_')

            if len(parts) == 0:
                values = ''
            else:
                values = parts[0].strip().split(',')

                # convert single values to string
                if len(values) == 1:
                    values = values[0]

            if len(values):
                fields[key] = values

        if len(fields):
            output[name] = fields


def _read_line(process):
    line = ''
    while True:
        c = process.stdout.read(1)
        line += c.decode('utf-8')

        if c == b'\r' or c == b'\n' or process.poll() is not None:
            return line


def _get_percent(line):
    space = line.rfind(' ')

    return int(line[space+1:-2])


def info(filename=None, bus=None, address=None):
    args = ['picotool', 'info', '-a']

    if filename:
        args.append(filename)

    if bus:
        args.extend(['--bus', str(bus)])
    else:
        bus = 0

    if address:
        args.extend(['--address', str(address)])
    else:
        address = 0

    result = subprocess.run(args, stdout=subprocess.PIPE)
    stdout = result.stdout.decode('utf-8')

    if result.returncode != 0:
        raise Exception('picotool returned %d (%s)' % (result.returncode, stdout[:-1]))

    is_multiple = stdout.startswith('Multiple')

    output = {}

    if is_multiple:
        devices = stdout.split('\nDevice at ')

        # remove "Multiple RP2040..."
        devices = devices[1:]

        for device in devices:
            groups = device.split('----------------------------\n')
            bus, address = re.match(DEVICE_REGEX, groups[0]).groups()

            device_output = {}
            _process_info_groups(groups[1].split('\n\n'), device_output)

            output['%s:%s' % (bus, address)] = device_output
    else:
        infos = stdout.split('\n\n')
        key = '%d:%d' % (bus, address)

        if filename:
            infos.pop(0)

            key = filename

        device_output = {}
        _process_info_groups(infos, device_output)
        output[key] = device_output

    return output


def load(filename, bus=None, address=None, verify=False, execute=False, offset=None, callback=None):
    args = ['picotool', 'load']

    if verify:
        args.append('--verify')

    if execute:
        args.append('--execute')

    args.append(filename)

    if offset:
        args.extend(['--offset', str(offset)])

    if bus:
        args.extend(['--bus', str(bus)])

    if address:
        args.extend(['--address', str(address)])

    process = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)

    while True:
        line = _read_line(process)
        is_verify = ('Verifying' in line) and verify

        try:
            percent = _get_percent(line)
            if callback:
                if callback.__code__.co_argcount == 2:
                    callback(percent, is_verify)
                else:
                    callback(percent)
        except:
            pass

        if process.poll() is not None:
            break

    if process.returncode != 0:
        raise Exception('picotool returned %d ' % process.returncode)

    return True


def save(filename, bus=None, address=None, all_flash=False, mem_range=None, callback=None):
    args = ['picotool', 'save']

    if all_flash:
        args.append('--all')

    if mem_range:
        args.extend(['--range', str(mem_range[0]), str(mem_range[1])])

    args.append(filename)

    if bus:
        args.extend(['--bus', str(bus)])

    if address:
        args.extend(['--address', str(address)])

    process = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)

    while True:
        line = _read_line(process)
        try:
            percent = _get_percent(line)
            if callback:
                callback(percent)
        except:
            pass

        if process.poll() is not None:
            break

    if process.returncode != 0:
        raise Exception('picotool returned %d ' % process.returncode)

    return True


def verify(filename, bus=None, address=None, mem_range=None, offset=None, callback=None):
    args = ['picotool', 'verify']

    if bus:
        args.extend(['--bus', str(bus)])

    if address:
        args.extend(['--address', str(address)])

    args.append(filename)

    if mem_range:
        args.extend(['--range', str(mem_range[0]), str(mem_range[1])])

    if offset:
        args.extend(['--offset', str(offset)])

    process = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)

    while True:
        line = _read_line(process)
        try:
            percent = _get_percent(line)
            if callback:
                callback(percent)
        except:
            pass

        if process.poll() is not None:
            break

    if process.returncode != 0:
        raise Exception('picotool returned %d ' % process.returncode)

    return True


def reboot(bus=None, address=None):
    args = ['picotool', 'reboot']

    if bus:
        args.extend(['--bus', str(bus)])

    if address:
        args.extend(['--address', str(address)])

    result = subprocess.run(args, stdout=subprocess.PIPE)
    stdout = result.stdout.decode('utf-8')

    if result.returncode != 0:
        raise Exception('picotool returned %d (%s)' % (result.returncode, stdout[:-1]))

    return True
