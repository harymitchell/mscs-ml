"""
To run: python -m unittest -v test.test_datasets
"""

import unittest
from dataset_service import dataset_service
from settings import TEST_MONGO_HOST, TEST_MONGO_PORT, TEST_MONGO_USERNAME, TEST_MONGO_PASSWORD, TEST_MONGO_DBNAME
from data import TEST_DATASET, LARGE_DATASET_ID
import pandas

class TestDatasetsMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatasetsMethods, self).__init__(*args, **kwargs)
        self.mongo_uri = "mongodb://{username}:{password}@{host}:{port}/{database}".format(
                username=TEST_MONGO_USERNAME, password=TEST_MONGO_PASSWORD, host=TEST_MONGO_HOST, port=TEST_MONGO_PORT, database=TEST_MONGO_DBNAME)
        self.dataset_service = dataset_service(self.mongo_uri, TEST_MONGO_DBNAME, "unit_test_worker_id")
        
    def setUp(self):
        self.created_datasets = []

    def test_create(self):
        dataset = self.dataset_service.insertDataset(TEST_DATASET)
        self.created_datasets.append(dataset)
        self.assertTrue(dataset is not None, 'dataset created')
        # Retrieve dataset by its _id
        self.assertEqual(self.dataset_service.getDatasetByID(dataset)['_id'], dataset, 'Retrieved dataset consistent')
        d = self.dataset_service.getDatasetByID(dataset)
        np_arr = self.dataset_service.dataToNumpy(d['data'])
        self.assertEqual(np_arr.dtype, 'float64')
        self.assertEqual(np_arr[0][0], 6.0)
        # print (np_arr[0])
        # print (np_arr[0].dtype)
        # print (np_arr[0][0].dtype)
        self.dataset_service.removeDataset({'name': 'Test Pima'})
        
    def test_large_dataset(self):
        """Test a dataset that uses gridfs
            python -m unittest -v test.test_datasets.TestDatasetsMethods.test_large_dataset"""
        d = self.dataset_service.getDatasetByID(LARGE_DATASET_ID)
        self.assertTrue(d is not None, 'large dataset retrieved')
        self.assertEqual(d['name'], 'mnist')
        self.assertTrue(isinstance(d['data'], pandas.DataFrame))
        
    def tearDown(self):
        for d in self.created_datasets:
            self.dataset_service.removeDataset({'name': 'Test Pima'})
            
        for grid_out in self.dataset_service.fs.find():
            if grid_out.filename != 'mnist':
                self.dataset_service.fs.delete(grid_out._id)
 