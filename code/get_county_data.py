def get_county_data(file_name, num_rows=None):
    """ Retrieves a single data-file from the King County Assessors webstie.

    Retrieves the single data-file from the King County Assessors webstie
    defined by file_name using the Pandas read_csv() function

    Args:
        file_name: The name of the file to download.
        num_rows: The number of rows to return.

    Returns:
        A Pandas dataframe containing all columns of the data retreived from
        the King County Assessor's webstie and number of rows equal to
        num_rows (defaults to all).

    Raises:
        ValueError: If passed file_name is not a string.
        ValueError: If passed num_rows is not a positive integer.
        OSError: If a connection to the URL is unable to be established.
    """

    # Import packages DELETE THIS LATER
    import time
    import pandas as pd

    # Initialize dataframe
    data_raw = pd.DataFrame()

    # Check inputs
    if not isinstance(file_name, str):
        raise ValueError('Passed file_name must be of type string')

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
            print(i)
            time.sleep(1)
            try:
                data_raw = pd.read_csv(url,
                                       nrows=num_rows,
                                       low_memory=False)
            except OSError:
                pass
        if data_raw.empty:
            raise OSError('King County Assessor\'s page could not be ' +
                          'reached. Please check ' +
                          'https://info.kingcounty.gov/assessor/' +
                          'DataDownload/default.aspx')

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
