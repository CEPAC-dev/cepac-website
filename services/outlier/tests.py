from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import pandas as pd
import io


class OutlierWorkflowTests(TestCase):
    """Integration tests for the outlier detection workflow."""

    def setUp(self):
        # build a small sample dataframe that contains two rate columns and some
        # intentional outliers.
        self.df = pd.DataFrame({
            'A_rate': [1, 2, 100, 4, 5],
            'B_rate': [10, 11, 12, 13, 14],
            'non_rate': [9, 8, 7, 6, 5],
        })

        csv_bytes = self.df.to_csv(index=False).encode('utf-8')
        self.upload_file = SimpleUploadedFile(
            'test.csv', csv_bytes, content_type='text/csv'
        )

    def _initial_post(self):
        """Upload file and return the response plus context values."""
        url = reverse('outLiers_Data:outlier_detection')
        resp = self.client.post(url, {'file': self.upload_file})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('file_session_id', resp.context)
        self.assertIn('rate_columns', resp.context)
        return resp

    def test_single_column_mode(self):
        resp = self._initial_post()
        session_id = resp.context['file_session_id']
        # choose A_rate which has a clear outlier (100)
        url = reverse('outLiers_Data:outlier_detection')
        resp2 = self.client.post(url, {
            'file_session_id': session_id,
            'processing_mode': 'single_column',
            'selected_items': ['A_rate'],
        })
        self.assertEqual(resp2.status_code, 200)
        results = resp2.context['results']
        self.assertIn('A_rate', results)
        self.assertGreater(results['A_rate']['total_outliers'], 0)

    def test_multiple_columns_mode(self):
        resp = self._initial_post()
        session_id = resp.context['file_session_id']
        url = reverse('outLiers_Data:outlier_detection')
        resp2 = self.client.post(url, {
            'file_session_id': session_id,
            'processing_mode': 'multiple_columns',
            'selected_items': ['A_rate', 'B_rate'],
        })
        self.assertEqual(resp2.status_code, 200)
        results = resp2.context['results']
        self.assertIn('A_rate', results)
        self.assertIn('B_rate', results)

    def test_single_row_mode(self):
        resp = self._initial_post()
        session_id = resp.context['file_session_id']
        # choose row index 3 (1-based in the UI) which contains the value 100
        url = reverse('outLiers_Data:outlier_detection')
        resp2 = self.client.post(url, {
            'file_session_id': session_id,
            'processing_mode': 'single_row',
            'selected_items': ['3'],
        })
        self.assertEqual(resp2.status_code, 200)
        results = resp2.context['results']
        self.assertIn('Row_3', results)
        self.assertGreater(results['Row_3']['outlier_count'], 0)

    def test_multiple_rows_mode(self):
        resp = self._initial_post()
        session_id = resp.context['file_session_id']
        url = reverse('outLiers_Data:outlier_detection')
        resp2 = self.client.post(url, {
            'file_session_id': session_id,
            'processing_mode': 'multiple_rows',
            'selected_items': ['1', '3'],
        })
        self.assertEqual(resp2.status_code, 200)
        results = resp2.context['results']
        self.assertIn('Row_1', results)
        self.assertIn('Row_3', results)

    def test_no_rate_columns(self):
        # build a file without any rate columns and ensure error message
        df2 = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        csv_bytes = df2.to_csv(index=False).encode('utf-8')
        file2 = SimpleUploadedFile('no_rate.csv', csv_bytes, content_type='text/csv')
        url = reverse('outLiers_Data:outlier_detection')
        resp = self.client.post(url, {'file': file2})
        self.assertContains(resp, "No 'Rate' columns found.")
