def get_county_data(file_name, num_rows=None):
    """ Retrieves a single data-file from the King County Assessors webstie.

    Retrieves the single data-file from the King County Assessors webstie
    defined by file_name using the Pandas read_csv() function

    Args:
        file_name: The name of the file to download.
                   Spaces will be properly formatted
        num_rows: The number of rows to return.

    Returns:
        A Pandas dataframe containing all columns of the data retreived from
        the King County Assessor's webstie and number of rows equal to
        num_rows (defaults to all).

    Raises:
        ValueError: If passed file_name is not a string.
        ValueError: If passed file_name is not valid.
        ValueError: If passed num_rows is not a positive integer.
        OSError: If a connection to the URL is unable to be established.
    """

    # Import packages DELETE THIS LATER
    import time
    import pandas as pd

    # Initialize dataframe
    data_raw = pd.DataFrame()

    # Check inputs
    valid_names = ['Accessory', 'Apartment%20Complex', 'Change%20History',
                   'Change%20History%20Detail', 'Commercial%20Building',
                   'Condo%20Complex%20and%20Units',
                   'District%20Levy%20Reference',
                   'Environmental%20Restriction',
                   'Home%20Improvement%20Applications',
                   'Home%20Improvement%20Exemptions', 'Legal', 'Lookup',
                   'Notes', 'Parcel', 'Permit', 'Real%20Property%20Account',
                   'Real%20Property%20Appraisal%20History',
                   'Real%20Property%20Sales', 'Residential%20Building',
                   'Review%20History', 'Tax%20Data', 'Unit%20Breakdown',
                   'Vacant%20Lot', 'Value%20History']

    if not isinstance(file_name, str):
        raise ValueError('Passed file_name must be of type string')

    file_name = file_name.replace(' ', '%20')

    if file_name not in valid_names:
        raise ValueError('The file name you\'ve entered is not valid. ' +
                         'Please check ' +
                         'https://info.kingcounty.gov/assessor/' +
                         'DataDownload/default.aspx for correct file name')

    if num_rows is not None:
        if not isinstance(num_rows, int) & (num_rows > 0):
            raise ValueError('Number or rows to return must be a positive' +
                             f'integer not {num_rows}')

    # Define base URL
    url = f'https://aqua.kingcounty.gov/extranet/assessor/{file_name}.zip'

    # Read in the data
    try:
        data_raw = pd.read_csv(url,
                               nrows=num_rows,
                               low_memory=False)

    except OSError:
        # try three more times with delay
        for i in range(3):
            time.sleep(1)
            try:
                data_raw = pd.read_csv(url,
                                       nrows=num_rows,
                                       low_memory=False)
            except OSError:
                pass
        if data_raw.empty:
            raise OSError('King County Assessor\'s page could not be ' +
                          'reached. Please check that ' +
                          'https://info.kingcounty.gov/assessor/' +
                          'DataDownload/default.aspx is available')

    except UnicodeDecodeError:
        # change encoding to latin-1 in read_csv
        data_raw = pd.read_csv(url,
                               nrows=num_rows,
                               encoding='latin-1',
                               low_memory=False)

    # Check result and return
    if data_raw.shape[0] == 0:
        raise RuntimeError('No data was returned. Please try again later.')

    return data_raw
