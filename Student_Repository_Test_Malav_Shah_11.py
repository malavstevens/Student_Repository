"""" Test for Repository """

import unittest
import os
import sqlite3
from Student_Repository_Malav_Shah_11 import Repository, Student, Instructor, Major


class TestRepository(unittest.TestCase):
    """ Test for repository """

    def setUp(self) -> None:
        """This methods allow you to define instructions that will be executed before and after each test method"""
        self.test_path: str = "/Users/malavshah/HW11"
        self.repo: Repository = Repository(self.test_path, False)

    def test_majors(self):
        """ Testing majors table"""
        expected = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']],
                    ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]

        calculated = [majors.info()
                      for majors in self.repo._majors.values()]

        self.assertEqual(expected, calculated)

    def test_student_attributes(self) -> None:
        """ Testing for student attributes """

        expected = [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38],
                    ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], [
                        'SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 2.0],
                    ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'],
                        ['SSW 540'], ['CS 501', 'CS 546'], 4.0],
                    ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5]]

        calculated = [student.info()
                      for cwid, student in self.repo._students.items()]

        self.assertEqual(expected, calculated)

    def test_instructor_attributes(self) -> None:
        """ Testing for Instructor attributes """
        expected = [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
                    ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                    ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]

        calculated = [list(detail) for instructor in self.repo._instructors.values(
        ) for detail in instructor.info()]

        self.assertEqual(expected, calculated)

    def test_instructor_table_db(self) -> None:
        """ Testing instructors table """
        expected = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                    ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                    ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                    ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                    ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                    ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                    ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                    ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                    ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]

        calculated = []
        db = sqlite3.connect("/Users/malavshah/HW11/CS810.db")
        for row in db.execute("select students.Name, students.CWID, grades.Course, grades.Grade, instructors.Name from students,grades,instructors where students.CWID=StudentCWID and InstructorCWID=instructors.CWID order by students.Name"):
            calculated.append(row)
        self.assertEqual(expected, calculated)


if __name__ == "__main__":
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
