
"""
# Removes rows containing missing values given a the list of columns you wish to remove nan values from
Input: columns and dataset
Output: notnull values from the columns selected
"""

def notNulls(columns, dataset):
    for col in columns:
        dataset = dataset[pd.notnull(dataset[col])]  
    return dataset


"""
# This function renames categories within a column given a list of new categories and the renaming condition. It also creates a new column with the renamed categories
Input: a list with the new categories, the dataset, a reference column (from where you want to apply changes), the name of the new column
Output: new column with categories renamed
"""


def categoryAggr(category_list, dataset, ref_column, new_column):
    for cat in category_list:
        dataset.loc[dataset[ref_column].str.startswith(f"{cat}"),f"{new_column}"] = f"{cat}"
        print(f"{cat} done")
    return dataset