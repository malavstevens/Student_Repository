"""" Test for Repository """

import unittest
import os
from HW09_Malav_Shah import Repository, Student, Instructor


class TestRepository(unittest.TestCase):
    """ Test for repository """

    def setUp(self) -> None:
        """This methods allow you to define instructions that will be executed before and after each test method"""
        self.test_path: str = "/Users/malavshah/HW_09"
        self.repo: Repository = Repository(self.test_path, False)

    def test_student_attributes(self) -> None:
        """ Testing for student attributes """
        expected = {'10103':  ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10115':  ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10172':  ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']],
                    '10175':  ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']],
                    '10183':  ['10183', 'Chapman, O', ['SSW 689']],
                    '11399':  ['11399', 'Cordova, I', ['SSW 540']],
                    '11461':  ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']],
                    '11658':  ['11658', 'Kelly, P', ['SSW 540']],
                    '11714':  ['11714', 'Morton, A', ['SYS 611', 'SYS 645']],
                    '11788':  ['11788', 'Fuller, E', ['SSW 540']]}

        actual = {cwid: student.info()
                  for cwid, student in self.repo._students.items()}
        self.assertEqual(expected, actual)

    def test_instructor_attributes(self) -> None:
        """ Testing for Instructor attributes """
        expected = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I',  'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}

        actual = {tuple(detail) for instructor in self.repo._instructors.values(
        ) for detail in instructor.info()}
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    """ Run test cases """
    unittest.main(exit=False, verbosity=2)
