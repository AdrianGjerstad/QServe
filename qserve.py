
from http.server import HTTPServer, BaseHTTPRequestHandler # Pretty obvious

import sys # argv
from datetime import datetime # timestamps

import qrc
import os.path
from os import path

# Check python interpreter (Requirement: python3)
if sys.version_info[0] < 3:
    sys.stderr.write('FATAL ERROR: Python3 required to run QServe!\n')
    sys.stderr.write('Current version: %i.%i.%i\n' % (
        sys.version_info[0],
        sys.version_info[1],
        sys.version_info[2]
    ))
    sys.stderr.write('\nExit Code: 127\n\n')
    sys.stderr.flush()
    sys.exit(127)

# Constants
QSERVE_DEFAULT_PORT = 8080
QSERVE_DEFAULT_IP   = '0.0.0.0'

# Parse options
QServe_Flags = {
    'verbose': False,
    'log_enable': False
}

QServe_Port = QSERVE_DEFAULT_PORT
QServe_IP   = QSERVE_DEFAULT_IP

def flag_set(name):
    return QServe_Flags[name]

def QServe_Arg_Crawl(argc, argv_):
    argv = argv_.copy()

    global QServe_Port
    global QServe_IP

    flag_skip = 0

    for i in range(1, argc):
        if flag_skip != 0:
            flag_skip -= 1
            continue

        if argv[i][0] == '-':
            argv[i] = argv[i][1:]
            if argv[i][0] == '-':
                argv[i] = argv[i][1:]
                if argv[i][0] == '-':
                    raise ValueError('Too many \'-\' characters in option: --%s' % (argv[i]))

                               # Parse double '-' options
                name = argv[i] # (name=fulloptionname)

                if name == 'verbose':
                    QServe_Flags['verbose'] = True
                elif name == 'ip':
                    QServe_IP = argv[i+1]
                    flag_skip = 1
                elif name == 'port':
                    QServe_Port = int(argv[i+1])
                    flag_skip = 1
                elif name == 'log':
                    QServe_Flags['log_enable'] = True
                else:
                    raise ValueError('Unknown option: --%s' % (name))

                continue
            elif len(argv[i]) > 1:
                raise ValueError('Unknown option: -%s' % (argv[i]))

                           # Parse single '-' options
            char = argv[i] # (char=optionchar)

            if char == 'v':
                QServe_Flags['verbose'] = True
            elif char == 'l':
                QServe_Flags['log_enable'] = True
            else:
                raise ValueError('Unknown option: -%s' % (char))

            continue

                       # Parse arguments without '-' characters
        argn = argv[i] # (argn=argumentvalue)

        if False:
            pass
        else:
            sys.stderr.write('WARNING: Argument with no use: ' + argn + '\n')

class QServeServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        if self.server.code_triggers.get(self.path) == '403':
            data = self.server.code_overrides.get('403', '<DEFAULT>')
            if data == '<DEFAULT>':
                data = '403 Forbidden'
            else:
                data = open(data[1:], 'r').read()
            self.send_response(403)
        else:
            try:
                data = open(self.path[1:]).read()
                self.send_response(200)
            except:
                if self.server.code_triggers.get(self.path) is '404':
                    data = self.server.code_overrides.get('404', '<DEFAULT>')
                    if data == '<DEFAULT>':
                        data = '404 Not Found'
                else:
                    data = '404 Not Found'
                self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(data, 'utf-8'))

    def log_message(self, format, *args):
        sys.stderr.write("[%s:%s] %s %s\n" % (
            self.client_address[0],
            self.client_address[1],
            self.log_date_time_string(),
            format%args
        ))

        severity = 'info'

        if args[1][0] == '4':
            severity = 'error'

        self.server.log('%s:%s %s' % (
            self.client_address[0],
            self.client_address[1],
            format%args
        ), severity)

class QServeServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        if flag_set('log_enable'):
            self.log_ = open('qserve_%s.log' % (self.file_date_time_string().replace(" ", "_")), 'x')
            self.log_.write('---- %s ----\n' % (self.log_.name))
            self.log('QServeServer started hosting on %s:%i' % (
                server_address[0],
                server_address[1]
            ))

        self.code_overrides = {}
        self.code_triggers = {}

    def set_code_overrides(self, co):
        self.code_overrides = co

    def set_code_triggers(self, ct):
        self.code_triggers = ct

    def close(self):
        if flag_set('log_enable'):
            self.log('QServeServer stopped hosting on %s:%i' % (
                self.server_address[0],
                self.server_address[1]
            ))

            self.log_.close()

    def log(self, value, severity='info'):
        if flag_set('log_enable'):
            self.log_.write('[%s] [%s] - %s\n' % (
                self.file_date_time_string(),
                severity,
                value
            ))

            self.log_.flush()

    def file_date_time_string(self):
        now = datetime.now()

        return now.strftime("%Y-%m-%d %H:%M:%S")

def main(argc, argv):
    # Crawl the options given
    QServe_Arg_Crawl(argc, argv)

    file_odata = {}
    file_otriggers = {}

    if path.exists('.qrc'):
        file_odata, file_otriggers, error = qrc.parse(open('.qrc', 'r').read())
        if error:
            return 1

    if flag_set('verbose'):
        sys.stderr.write('To quit safely, press CTRL+C. (CMD+C on Mac)\n')

    sys.stderr.write('Serving HTTP on port %i with ip %s ...\n' % (
        QServe_Port,
        QServe_IP
    ))

    QHTTP_DAEMON_SERVER = QServeServer((QServe_IP, QServe_Port), QServeServerHandler)
    QHTTP_DAEMON_SERVER.set_code_overrides(file_odata)
    QHTTP_DAEMON_SERVER.set_code_triggers(file_otriggers)

    try:
        QHTTP_DAEMON_SERVER.serve_forever()
    except KeyboardInterrupt:
        # CTRL+C/CMD+C Pressed
        sys.stderr.write('\b\bStopping serving HTTP on port %i with ip %s ...\n' % (
            QServe_Port,
            QServe_IP
        ))

        QHTTP_DAEMON_SERVER.close()

        return 0

    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
else:
    raise RuntimeError('qserve.py cannot be executed from another file.')
