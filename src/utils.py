


def get_data_home(data_home=None):
    """Get the home data directory.

    By default the data dir is set to a folder named 'data'
    in the user home folder.

    Alternatively, it can be set by the 'DATA_HOME' environment
    variable or programatically by giving an explit folder path. The
    '~' symbol is expanded to the user home folder.

    If the folder does not already exist, it is automatically created.
    """
    import os
    if data_home is None:
        data_home = os.environ.get('DATA_HOME',
                                   os.path.join('~/Desktop/personal_projects/qso_cv/', 'data'))
    data_home = os.path.expanduser(data_home)
    if not os.path.exists(data_home):
        os.makedirs(data_home)
    return data_home