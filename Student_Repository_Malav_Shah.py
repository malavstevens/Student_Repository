"""Creating a Data Repo for University"""

from typing import Dict, DefaultDict, Tuple, List, Iterator
from prettytable import PrettyTable
from collections import defaultdict
import os
import csv
# holds all of  the students, instructors and grades for a single University


class Repository:
    """Student and Instructor repo (get students, get instructor & get grades)"""

    def __init__(self, path: str, tables: bool = True) -> None:
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()

        try:
            self._get_students(os.path.join(self._path, 'students.txt'))
            self._get_instructors(os.path.join(self._path, 'instructors.txt'))
            self._get_grades(os.path.join(self._path, 'grades.txt'))

        except (FileNotFoundError, ValueError) as e:
            print(e)

        else:
            if tables:
                print("\nStudent Table ")
                self.student_table()
                print("\nInstructor Table ")
                self.instructor_table()

    def _get_students(self, path) -> None:
        """ Read student details and added to dictionary """
        for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
            self._students[cwid] = Student(cwid, name, major)

    def _get_instructors(self, path) -> None:
        """ Read Instructor's details and added to dictionary """
        for cwid, name, dept in file_reader(path, 3, sep='\t', header=False):
            self._instructors[cwid] = Instructor(cwid, name, dept)

    def _get_grades(self, path) -> None:
        """ Read grades and assigned to student and instructor """
        for std_cwid, course, grade, instructor_cwid in file_reader(path, 4, sep='\t', header=False):
            if std_cwid in self._students:
                self._students[std_cwid].add_course(course, grade)
            else:
                print(f'Grades for student is {std_cwid}')

            if instructor_cwid in self._instructors:
                self._instructors[instructor_cwid].add_student(course)
            else:
                print(f'Grades for instructor is {instructor_cwid}')

    def student_table(self) -> None:
        """ Student table """
        table = PrettyTable(field_names=Student.FIELD_NAMES)
        for student in self._students.values():
            table.add_row(student.info())
        # print(table)

    def instructor_table(self) -> None:
        """ Instructor table """
        table = PrettyTable(field_names=Instructor.FIELD_NAMES)
        for instructor in self._instructors.values():
            for row in instructor.info():
                table.add_row(row)
        print(table)


class Student:
    """Student Class to store student data"""
    FIELD_NAMES = ['CWID', 'Name', 'Completed Courses']

    def __init__(self, cwid: str, name: str, major: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def add_course(self, course: str, grade: str) -> None:
        """ Adding course with grade """
        self._courses[course] = grade

    def info(self) -> Tuple[str, str, List[str]]:
        """ return a list of information needed for pretty table """
        return [self._cwid, self._name, sorted(self._courses.keys())]


class Instructor:
    """ Instructor class """
    FIELD_NAMES = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: str, name: str, dept: str) -> None:

        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_student(self, course: str) -> None:
        """ Number of students taking course with Instructor """
        self._courses[course] += 1

    def info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """ Yield row """
        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]


def main():
    Repository('/Users/malavshah/HW05_malav_shah/HW_09')


if __name__ == '__main__':
    main()


def file_reader(path: str, fields: int, sep: str = ',', header: bool = False) -> Iterator[Tuple[str]]:
    """ A generator function to read text files and return all of the values"""

    try:
        file_path = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("File is not present on the provided path")

    else:
        line_num: int = 0
        with file_path:
            reader = csv.reader(file_path, delimiter=sep)

            for line in reader:
                line_num += 1

                if len(line) != fields:
                    raise ValueError(
                        f'{path} - path has length of line: {len(line)} fields on line no: {line_num} expected {fields}')

                if header == False:
                    yield tuple(line)
                else:
                    header = False
