import unittest
from webscraper import get_table_rows, create_lists, get_csv


class OutputTest(unittest.TestCase):

    """
        These tests check the functions written in the webscraper.py file
        We import get_table_rows, create_lists, and get_csv at the top of this test file
    """

    def setUp(self):

        # We will be scraping the URL below that contains a table with the ranking, name, and city of U.S universities
        self.url = "https://www.4icu.org/us/"

    def test_table_rows_exist(self):

        # Call function
        test = get_table_rows(self.url)

        # Check that the GET request returns a response
        self.assertIsNotNone(test)

    def test_create_lists(self):

        # Call functions
        test = get_table_rows(self.url)
        rank, name, city = create_lists(test)

        # Checks that the returned lists are not empty
        self.assertGreater(len(rank), 1)
        self.assertGreater(len(name), 1)
        self.assertGreater(len(city), 1)

        # Since every University has a ranking and city, the length of all lists should be the equal
        self.assertEqual(len(rank), len(name))
        self.assertEqual(len(rank), len(city))

    def test_pandas_df(self):
        """"
            Testing the accuracy of the returned pandas data frame object
        """

        # Call functions
        test = get_table_rows(self.url)
        rank, name, city = create_lists(test)
        df  = get_csv(rank, name, city)

        # Check City of University
        city_harvard = df.loc[df['Name'] == 'Harvard University']['City'].item()
        city_usc = df.loc[df['Name'] == 'University of Southern California']['City'].item()
        self.assertEqual(city_harvard, 'Cambridge')
        self.assertEqual(city_usc, 'Los Angeles')

        # Check University of a Ranking
        ranking_3 = df.loc[df['Rank'] == '3']['Name'].item()
        ranking_46 = df.loc[df['Rank'] == '46']['Name'].item()
        self.assertEqual(ranking_3, 'Stanford University')
        self.assertEqual(ranking_46, 'University of California, Santa Barbara')


if __name__ == '__main__':
    unittest.main()
