import unittest
from Student_Repository_Malav_Shah_11 import Repository, Student, Instructor
import os
import sys
from prettytable import PrettyTable
import sqlite3


class Test_HW11(unittest.TestCase):
    """ Class  to perform error checking ad handelling """

    def test_class_instructor(self):

        stevens: Repository = Repository(
            r"/Users/malavshah/HW11")
        list1 = list()
        list2 = [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1], ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4], ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1], [
            '98762', 'Hawking, S', 'CS', 'CS 501', 1], ['98762', 'Hawking, S', 'CS', 'CS 546', 1], ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]
        for instructor in stevens._instruct.values():
            for row in instructor.details():

                list1.append(list(row))

        self.assertEqual(list1, list2)

    def test_class_student(self):

        stevens: Repository = Repository(
            r"/Users/malavshah/HW11")
        list1 = list()
        list2 = [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], '3.38'], ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], '2.00'], [
            '10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], '4.00'], ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], '3.50']]
        for student in stevens._students.values():
            list1.append(student.details())

        self.assertEqual(list1, list2)

    def test_file_not_found_error(self) -> None:

        with self.assertRaises(FileNotFoundError):
            Repository(
                r"/Users/malavshah/EmptyFolder")

    def test_class_major(self):

        stevens: Repository = Repository(
            r"/Users/malavshah/HW11")
        list1 = list()
        list2 = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']], [
            'CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]
        for major in stevens._maj.values():
            list1.append(major.details())
        self.assertEqual(list1, list2)

    def test_class_grade(self):
        db: sqlite3.Connection = sqlite3.connect(
            "/Users/malavshah/HW09/CS810")
        list_1 = list()
        list_2 = [('Jobs, S', '10103', 'A-', 'SSW 810', 'Rowland, J'), ('Jobs, S', '10103', 'B', 'CS 501', 'Hawking, S'), ('Bezos, J', '10115', 'A', 'SSW 810', 'Rowland, J'), ('Bezos, J', '10115', 'F', 'CS 546', 'Hawking, S'),  ('Musk, E', '10183',
                                                                                                                                                                                                                                     'A', 'SSW 555', 'Rowland, J'),  ('Musk, E', '10183', 'A', 'SSW 810', 'Rowland, J'),  ('Gates, B', '11714', 'B-', 'SSW 810', 'Rowland, J'), ('Gates, B', '11714', 'A', 'CS 546', 'Cohen, R'), ('Gates, B', '11714', 'A-', 'CS 570', 'Hawking, S')]
        for row in db.execute("SELECT (s.Name) as 'Student',(s.CWID) as 'CWID',(g.Grade) as 'Earned_grade',(g.Course) as 'In_Course',(i.Name) as 'Thought_by' from students as s inner join grades as g on s.CWID = g.StudentCWID inner join instructors i on g.InstructorCWID = i.CWID"):
            list_1.append(row)
        # print(list1)
        self.assertEqual(list_1, list_2)


if __name__ == '__main_s_':
    unittest.main(exit=False, verbosity=2)
