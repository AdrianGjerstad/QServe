# QServeRunCommands Parser

import sys

def parse(data):
    lines = data.split('\n')

    file_data = {}
    trigger_data = {}

    for i in range(len(lines)):
        if lines[i].endswith('\r'):
            lines[i] = lines[i][0:len(lines[i])-1]
        
        if lines[i] == '':
          continue

        lines[i] = tuple(lines[i].split(' - '))

    for i in range(len(lines)):
        if len(list(lines[i])) != 2:
          continue

        r, v = lines[i]

        if len(r) == 3:
            try:
                int(r) # Will trigger except clause if error occurs
                if v[0] != '/':
                    if v == '<DEFAULT>':
                        file_data[r] = None
                        continue
                    sys.stderr.write('.qrc rule value at line %i must have an absolute path or <DEFAULT>.\n' % (
                        i+1
                    ))
                    return (None, None, True)

                file_data[r] = v
            except:
                sys.stderr.write('.qrc rule at line %i must follow the following format (RegExp):\n' % (i+1))
                sys.stderr.write('\tt?[0-9]{3}\n')
                return (None, None, True)
        elif len(r) == 4:
            try:
                r = r[1:]
                int(r) # Will trigger except clause if error occurs

                if v[0] != '/':
                    sys.stderr.write('.qrc rule value at line %i must have an absolute path.\n' % (
                        i+1
                    ))
                    return (None, None, True)

                trigger_data[v] = r
            except:
                sys.stderr.write('.qrc rule at line %i must follow the following format (RegExp):\n' % (i+1))
                sys.stderr.write('\tt?[0-9]{3}\n')
                return (None, None, True)
        else:
            sys.stderr.write('.qrc rule at line %i must follow the following format (RegExp):\n' % (i+1))
            sys.stderr.write('\tt?[0-9]{3}\n')
            return (None, None, True)

    return (file_data, trigger_data, False)

# Example .qrc:
# 404 - /404.html
# 403 - /403.html
# t403 - /private/mysecret
# t403 - /doesnothavetobeinadirectory
# 503 - <DEFAULT>

# NOTE: There is not much point in having that last line!
