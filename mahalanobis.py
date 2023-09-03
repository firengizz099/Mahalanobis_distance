import pandas as pd
import numpy as np
from scipy.spatial.distance import mahalanobis

def fill_na_mahalanobis(df):
    # Get covariance matrix for entire DataFrame
    cov = np.cov(df, rowvar=False)
    inv_cov = np.linalg.inv(cov)

    # Iterate through each row in DataFrame
    for index, row in df.iterrows():
        # Check if there are any NaN values in the row
        if pd.isna(row).sum() > 0:
            # Calculate Mahalanobis distance for each row to all other rows
            dist = np.apply_along_axis(lambda x: mahalanobis(row.fillna(0), x.fillna(0), inv_cov), 1, df.fillna(0))

            # Get indices of nearest neighbors without NaN values
            nn_idx = np.argsort(dist)[1:]
            nn_notnull = df.iloc[nn_idx].dropna()

            # Calculate mean of nearest neighbors and fill NaN values with this value
            if len(nn_notnull) > 0:
                row.fillna(nn_notnull.mean(), inplace=True)

    return df
#Description of the Code

# import pandas as pd
# import numpy as np
# from scipy.spatial.distance import mahalanobis

# This imports the necessary libraries for the code: Pandas for working with data in a DataFrame, NumPy for scientific computing, and Mahalanobis distance from the SciPy library for calculating distances between rows.

# def fill_na_mahalanobis(df):
# This creates a function called fill_na_mahalanobis that takes a DataFrame as its input and will return the modified DataFrame with all NaN values filled.

# cov = np.cov(df, rowvar=False)
# inv_cov = np.linalg.inv(cov)
# This calculates the covariance matrix of the DataFrame and its inverse. The rowvar=False parameter specifies that the input DataFrame is a collection of column vectors.

# for index, row in df.iterrows():
# This iterates through each row in the DataFrame, where index is the index of the row and row is the row itself.

# if pd.isna(row).sum() > 0:
# This checks whether the row contains any NaN values using pd.isna(), which returns a boolean mask indicating whether each value is NaN, and sum() to count the number of True values. If there are any NaN values in the row, then the code inside the if statement will execute.

# dist = np.apply_along_axis(lambda x: mahalanobis(row.fillna(0), x.fillna(0), inv_cov), 1, df.fillna(0))
# This calculates the Mahalanobis distance between the current row and all other rows in the DataFrame using np.apply_along_axis(). This function applies a given function to 1-D slices along the given axis of the input array, which in this case is the rows of the DataFrame. The function calculates the Mahalanobis distance between each row and the current row using the mahalanobis() function from SciPy. The fillna() function replaces all NaN values with 0.

# nn_idx = np.argsort(dist)[1:]
# nn_notnull = df.iloc[nn_idx].dropna()

# This gets the indices of the nearest neighbors that do not have any NaN values using np.argsort(), which returns the indices that would sort the array. Since the distance from the row to itself is 0, the nearest neighbor will be the row itself, so we start with the second-nearest neighbor ([1:]). The iloc[] function selects rows from the DataFrame using the specified integer index, and dropna() removes any rows that contain NaN values.


# if len(nn_notnull) > 0:
#     row.fillna(nn_notnull.mean(), inplace=True)
# This checks if there are any nearest neighbors without NaN values, and if so, fills the NaN values in the current row with the mean value of those nearest neighbors using fillna() with the inplace=True parameter to modify the row in-place.

# return df