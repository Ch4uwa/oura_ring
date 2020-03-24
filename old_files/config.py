from configparser import ConfigParser


def config(filename=None, section=None):
    # Create Parser
    parser = ConfigParser()
    # Read file
    parser.read(filename)

    values = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            values[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in file {1}'.format(section, filename))
    return values
