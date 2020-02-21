from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # Create Parser
    parser = ConfigParser()
    # Read file
    parser.read(filename)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in file {1}'.format(section, filename))
    return db
