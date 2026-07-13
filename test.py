"""
test.py - unit tests for student manager
aliakbartnt - 2026
run: py test.py
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from unittest.mock import patch
from io import StringIO
#path find
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main


class TestApp(unittest.TestCase):
    """testing everything"""

    def setUp(self):
        """reset before test"""
        main.students.clear()
        main.courses.clear()
        main.student_counter = 1
        main.course_counter = 1
        main.id_mode = 'manual'

    def tearDown(self):
        """clean up after"""
        main.students.clear()
        main.courses.clear()

    # ---- helper funcs ----

    def test_ids(self):
        """check id generation"""

        s1 = main.generate_student_id()
        s2 = main.generate_student_id()
        self.assertEqual(s1, "S1")
        self.assertEqual(s2, "S2")
        
        c1 = main.generate_course_id()
        c2 = main.generate_course_id()

        self.assertEqual(c1, "C1")
        self.assertEqual(c2, "C2")

    def test_avg(self):
        """test average calculation"""

        data1 = {'grades': {'c1': 18.5, 'c2': 17.0}}
        self.assertEqual(main.calc_average(data1), 17.75)
        
        data2 = {'grades': {}}
        self.assertEqual(main.calc_average(data2), 0.0)

    def test_find_student(self):
        """find student by id"""


        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        
        # check case sensitive
        st = main.get_student('S1')
        self.assertIsNotNone(st)
        self.assertEqual(st['name'], 'Ali')
        
        # check case insensitive
        st2 = main.get_student('s1')
        self.assertIsNotNone(st2)
        
        # check non-existing
        st3 = main.get_student('S2')
        self.assertIsNone(st3)

    def test_exists(self):
        """check if student exists"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        self.assertTrue(main.student_exists('S1'))
        self.assertTrue(main.student_exists('s1'))  # case insensitive
        self.assertFalse(main.student_exists('S2'))

    # ---- main ops ----

    @patch('builtins.input', side_effect=['S1', 'Ali'])
    def test_add_student(self, mock_input):
        """add student manually"""



        main.add_student()
        self.assertEqual(len(main.students), 1)
        self.assertEqual(main.students['s1']['name'], 'Ali')

    @patch('builtins.input', side_effect=['S1'])
    def test_dup_student(self, mock_input):
        """duplicate student id"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        main.add_student()
        self.assertEqual(len(main.students), 1)

    @patch('builtins.input', side_effect=['C1', 'Math'])
    def test_add_course(self, mock_input):
        """add course"""
        main.add_course()

        self.assertEqual(len(main.courses), 1)
        self.assertEqual(main.courses['c1']['name'], 'Math')

    @patch('builtins.input', side_effect=['S1', 'C1', '18.5'])
    
    def test_grade(self, mock_input):
        """set grade for student"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        main.courses['c1'] = {'id': 'C1', 'name': 'Math'}
        main.set_grade()
        self.assertIn('c1', main.students['s1']['grades'])
        self.assertEqual(main.students['s1']['grades']['c1'], 18.5)

    @patch('builtins.input', side_effect=['S1', 'Ali Reza'])
    def test_edit_student(self, mock_input):
        """edit student name"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        main.edit_student()
        self.assertEqual(main.students['s1']['name'], 'Ali Reza')

    @patch('builtins.input', side_effect=['C1', 'Mathematics'])
    def test_edit_course(self, mock_input):
        """edit course name"""
        main.courses['c1'] = {'id': 'C1', 'name': 'Math'}
        main.edit_course()
        self.assertEqual(main.courses['c1']['name'], 'Mathematics')

    @patch('builtins.input', side_effect=['S1', 'y'])
    def test_del_student(self, mock_input):
        """delete student"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        main.delete_student()
        self.assertEqual(len(main.students), 0)

    @patch('builtins.input', side_effect=['C1', 'y'])
    def test_del_course(self, mock_input):
        """delete course"""
        main.courses['c1'] = {'id': 'C1', 'name': 'Math'}
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {'c1': 18.5}}
        main.delete_course()
        self.assertEqual(len(main.courses), 0)
        self.assertNotIn('c1', main.students['s1']['grades'])

    # ---- search and sort ----

    @patch('builtins.input', side_effect=['Ali'])
    def test_search(self, mock_input):
        """search student by name"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali Ahmadi', 'grades': {'c1': 18.5}}
        
        with patch('sys.stdout', new_callable=StringIO) as out:
            main.search_student_by_name()
            output = out.getvalue()
            self.assertTrue('Ali' in output or 'علی' in output)

    @patch('builtins.input', side_effect=['d'])
    def test_sort(self, mock_input):
        """sort students by average"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {'c1': 20, 'c2': 18}}
        main.students['s2'] = {'id': 'S2', 'name': 'Sara', 'grades': {'c1': 15}}
        main.students['s3'] = {'id': 'S3', 'name': 'Reza', 'grades': {}}
        
        with patch('sys.stdout', new_callable=StringIO) as out:
            main.sort_students_by_average()
            output = out.getvalue()
            # just check if something printed
            self.assertTrue(len(output) > 0)

    # ---- delete all ----

    @patch('builtins.input', side_effect=['y', 'y'])
    def test_nuke(self, mock_input):
        """delete all data"""
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        main.courses['c1'] = {'id': 'C1', 'name': 'Math'}
        main.delete_all_data()
        self.assertEqual(len(main.students), 0)
        self.assertEqual(len(main.courses), 0)

    # ---- storage ----

    def test_save_load(self):
        """save and load data"""
        orig_storage = main.STORAGE_DIR
        orig_data = main.DATA_FILE
        
        try:
            tmp = tempfile.mkdtemp()
            test_storage = os.path.join(tmp, 'Storage')
            test_file = os.path.join(test_storage, 'data.json')
            
            main.STORAGE_DIR = test_storage
            main.DATA_FILE = test_file
            os.makedirs(test_storage, exist_ok=True)
            
            # add some data
            main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
            main.courses['c1'] = {'id': 'C1', 'name': 'Math'}
            
            main.save_to_file()
            self.assertTrue(os.path.exists(test_file))
            
            # clear and load
            main.students.clear()
            main.courses.clear()
            main.load_from_file()
            
            self.assertEqual(len(main.students), 1)
            self.assertEqual(main.students['s1']['name'], 'Ali')
            
        finally:
            main.STORAGE_DIR = orig_storage
            main.DATA_FILE = orig_data
            if os.path.exists(tmp):
                shutil.rmtree(tmp)


class TestWorkflow(unittest.TestCase):
    """full workflow test"""

    def setUp(self):
        main.students.clear()
        main.courses.clear()
        main.student_counter = 1
        main.course_counter = 1

    def test_complete(self):
        """complete scenario"""
        # add student
        main.students['s1'] = {'id': 'S1', 'name': 'Ali', 'grades': {}}
        main.courses['c1'] = {'id': 'C1', 'name': 'Math'}
        
        # grade
        main.students['s1']['grades']['c1'] = 18.5
        self.assertEqual(main.students['s1']['grades']['c1'], 18.5)
        
        # avg
        avg = main.calc_average(main.students['s1'])
        self.assertEqual(avg, 18.5)
        
        # edit
        main.students['s1']['name'] = 'Ali Reza'
        self.assertEqual(main.students['s1']['name'], 'Ali Reza')
        
        # delete
        del main.students['s1']
        self.assertEqual(len(main.students), 0)


if __name__ == '__main__':
    unittest.main()