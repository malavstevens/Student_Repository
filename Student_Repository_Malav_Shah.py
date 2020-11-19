""" Creating a Data Repository for University """

import os
from collections import defaultdict
from prettytable import PrettyTable
from typing import Dict, DefaultDict, Tuple, List, Iterator, Set
import csv


class Repository:
    "Major, Student and Instructor repository"

    def __init__(self, path: str, tables: bool = True) -> None:
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()

        try:
            self._get_majors(os.path.join(path, 'majors.txt'))
            self._get_students(os.path.join(path, 'students.txt'))
            self._get_instructors(os.path.join(path, 'instructors.txt'))
            self._get_grades(os.path.join(path, 'grades.txt'))

        except (FileNotFoundError, ValueError) as e:
            print(e)

        else:
            if tables:
                print("\nMajors Table")
                self.majors_table()
                print("\nStudent Table ")
                self.student_table()
                print("\nInstructor Table ")
                self.instructor_table()

    def _get_majors(self, path: str):
        """Major details are read using file reading gen and added to dictionary"""
        for major, flag, course in file_reader(path, 3, sep='\t', header=True):
            if major not in self._majors:
                self._majors[major] = Major(major)
            self._majors[major].add_course(course, flag)

    def _get_students(self, path: str) -> None:
        """ Student detail are read using file reading gen and added to dictionary """
        for cwid, name, major in file_reader(path, 3, sep=';', header=True):
            if major not in self._majors:
                print(f"Student {cwid} '{name}' has unknown major '{major}'")
            else:
                self._students[cwid] = Student(cwid, name, self._majors[major])

    def _get_instructors(self, path: str) -> None:
        """ Instructor detail are read using file reading gen and added to dictionary """
        for cwid, name, dept in file_reader(path, 3, sep='|', header=True):
            self._instructors[cwid] = Instructor(cwid, name, dept)

    def _get_grades(self, path: str) -> None:
        """Grades are read using file reading gen and assigned to student and instructor """
        for std_cwid, course, grade, instructor_cwid in file_reader(path, 4, sep='|', header=True):
            if std_cwid in self._students:
                self._students[std_cwid].add_course(course, grade)
            else:
                print(f'Grades for student is {std_cwid}')

            if instructor_cwid in self._instructors:
                self._instructors[instructor_cwid].add_student(course)
            else:
                print(f'Grades for instructor is {instructor_cwid}')

    def majors_table(self) -> None:
        """ Majors table """
        table: PrettyTable = PrettyTable(field_names=Major.FIELD_NAMES)
        for major in self._majors.values():
            table.add_row(major.info())
        print(table)

    def student_table(self) -> None:
        """ Student table """
        table: PrettyTable = PrettyTable(field_names=Student.FIELD_NAMES)
        x: List[str] = list()
        for student in self._students.values():
            table.add_row(student.info())
            x.append(student.info())
        print(table)

    def instructor_table(self) -> None:
        """ Instructor table """
        table: PrettyTable = PrettyTable(field_names=Instructor.FIELD_NAMES)
        for instructor in self._instructors.values():
            for row in instructor.info():
                table.add_row(row)
        print(table)


class Major:
    """ Major Class """
    FIELD_NAMES: List[str] = ['Major', 'Required Courses', 'Electives']
    GRADES: Set[str] = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def __init__(self, major: str) -> None:
        self._major: str = major
        self._required: Set[str] = set()
        self._electives: Set[str] = set()

    def add_course(self, course: str, option: str) -> None:
        if option == 'R':
            self._required.add(course)
        elif option == 'E':
            self._electives.add(course)
        else:
            raise ValueError("Course Flag not Valid")

    def remaining(self, completed: Dict[str, str]) -> Tuple[str, List[str], List[str], List[str]]:
        """Adding remaining courses as well as electives"""
        passed: Set[str] = {course for course,
                            grade in completed.items() if grade in Major.GRADES}
        remaining: Set[str] = self._required - passed
        electives: Set[str] = self._electives

        if self._electives.intersection(passed):
            electives = []

        return self._major, list(passed), list(remaining), list(electives)

    def info(self) -> Tuple[str, List[str], List[str]]:
        """ Returning a row in table """
        return [self._major, sorted(self._required), sorted(self._electives)]


class Student:
    """Student Class """
    FIELD_NAMES: List[str] = ['CWID', 'Name', 'Major',
                              'Completed Courses', 'Remaining Required', 'Remaining Electives', 'GPA']

    def __init__(self, cwid: str, name: str, major: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def add_course(self, course: str, grade: str) -> None:
        """ Adding course with grade """
        self._courses[course] = grade

    def gpa(self) -> float:
        """Calculate the GPA using dictionary"""
        grades: Dict[str, float] = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75,
                                    'C+': 2.25, 'C': 2.0, "C-": 0.00, "D+": 0.00, "D": 0.00, "D-": 0.00, "F": 0.00}
        try:
            total: float = sum(
                [grades[grade] for grade in self._courses.values()]) / len(self._courses.values())
            return round(total, 2)
        except ZeroDivisionError as e:
            print(e)

    def info(self) -> Tuple[str, str, str, List[str], List[str], List[str]]:
        """ return a list of information needed for pretty table """
        major, passed, remaining, electives = self._major.remaining(
            self._courses)

        return [self._cwid, self._name, major, sorted(passed), sorted(remaining), sorted(electives), self.gpa()]


class Instructor:
    """ Instructor class """
    FIELD_NAMES: List[str] = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: str, name: str, dept: str) -> None:

        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_student(self, course: str) -> None:
        """ Number of students taking course with Instructor """
        self._courses[course] += 1

    def info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """ Yield the row """
        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]

# Write a generator function to read text files and return all of the values


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


def main():
    Repository('/Users/malavshah/HW09')


if __name__ == '__main__':
    main()
