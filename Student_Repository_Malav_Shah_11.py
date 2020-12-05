""" Creating a Data Repository for University """

import os
import sqlite3
import collections
from collections import defaultdict
from prettytable import PrettyTable
from typing import Dict, DefaultDict, Tuple, List, Iterator


class Repository:
    def __init__(self, dir_path: str) -> None:
        self._dir_path: str = dir_path
        self._stud: Dict[str, str] = dict()
        self._instruct: Dict[str, str] = dict()
        self._maj: Dict[str, str] = dict()
        os.chdir(self._dir_path)
        self.file_list = os.listdir()
        cwd: str = os.getcwd()

        try:
            self.majors(os.path.join(cwd, 'majors.txt'))
            self.students(os.path.join(cwd, 'students.txt'))
            self.instructor(os.path.join(cwd, 'instructors.txt'))
            self.grades(os.path.join(cwd, 'grades.txt'))

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def majors(self, path) -> None:
        for mjor, flag, course in self.file_reading(path, 3, header=True, sep='\t'):
            if mjor not in self._maj:
                self._maj[mjor] = Major(mjor)
            self._maj[mjor].add_major(course, flag)

    def instructor(self, path) -> None:
        """ Instructor detail """
        for cwid, name, deptarment in self.file_reading(path, 3, header=True, sep='\t'):
            self._instruct[cwid] = Instructor(cwid, name, deptarment)

    def students(self, path) -> None:
        """ Student detail """
        for cwid, name, major in self.file_reading(path, 3, header=True, sep='\t'):
            self._stud[cwid] = Student(
                cwid, name, major, self._maj[major].get_req(), self._maj[major].get_elec())

    def grades(self, path) -> None:
        """Grades details to map with student and instructor"""
        for std_cwid, course, grade, instructor_cwid in self.file_reading(path, 4, header=True, sep='\t'):
            if instructor_cwid in self._instruct:
                self._instruct[instructor_cwid].add_student_to_course(course)
            else:
                print(
                    f'The Grade file Contains a instructor {instructor_cwid} who is not in instructor file')
            if std_cwid in self._stud:
                self._stud[std_cwid].add_coursework(course, grade)
            else:
                print(
                    f'The Grade file contains a student {std_cwid} who is not in student file')

    def file_reading(self, path: str, fields: int, header, sep: str = ',') -> Iterator[List[str]]:
        if not isinstance(path, str):
            raise ValueError("Path is Not a string")
        if not isinstance(fields, int):
            raise ValueError("Fields is Not a Integer")
        try:
            fp: IO = open(path, 'r')
            base = os.path.basename(path)
        except FileNotFoundError:
            print("No file in such directory")
        else:
            with fp:
                if header:
                    next(fp)
                for n, line in enumerate(fp, 1):
                    line = line.strip()
                    if line.count(sep) == fields-1:
                        yield tuple(line.split(sep))
                    else:
                        raise ValueError(
                            f"{base} has {line.count(sep) + 1} fields on line {n} but expected {fields} ")

    def stud_table(self) -> None:
        """to display Student table """
        student_tab = PrettyTable()
        student_tab.field_names = [
            'CWID', 'Name', 'Majors', 'Completed Courses', 'Remaininig Courses', 'Remaining Elective', 'GPA']
        for student in self._stud.values():
            student_tab.add_row(student.details())
        print("\n")
        print("Student Summary")
        print(student_tab)

    def instruct_table(self) -> None:
        """ to display Instructor table """
        instructor_tab = PrettyTable()
        instructor_tab.field_names = [
            'CWID', 'Name', 'Deptarment', 'Course', 'Students']
        for instructor in self._instruct.values():
            for row in instructor.details():
                instructor_tab.add_row(row)
        print("\n")
        print("Instructor Summary")
        print(instructor_tab)

    def major_tab(self) -> None:
        m_tab = PrettyTable()
        m_tab.field_names = ['Major', 'Required courses', 'Elective']
        for mj in self._maj.values():
            m_tab.add_row(mj.details())
        print("Major Summary")
        print(m_tab)

    def student_grade_table_db(self, db_path):
        ptgrades: PrettyTable = PrettyTable()
        ptgrades.field_names = ['Name', 'CWID',
                                'Course', 'Grade', 'Instructor']
        db: sqlite3.Connection = sqlite3.connect(db_path)
        for row in db.execute("SELECT (s.Name) as 'Student',(s.CWID) as 'CWID',(g.Course) as 'In_Course',(g.Grade) as 'Earned_grade',(i.Name) as 'Thought_by' from students as s inner join grades as g on s.CWID = g.StudentCWID inner join instructors i on g.InstructorCWID = i.CWID ORDER BY s.Name"):
            ptgrades.add_row(row)
        print("\n")
        print("Grades Summary")
        print(ptgrades)


class Major:
    def __init__(self, major: str) -> None:
        self._major = major
        self.required_course = list()
        self.elective_course = list()

    def add_major(self, course, fl) -> None:
        if fl == 'R':
            self.required_course.append(course)
        elif fl == 'E':
            self.elective_course.append(course)
        else:
            print(f"the data flag {fl} is not in use")

    def get_req(self) -> List[str]:
        return list(self.required_course)

    def get_elec(self) -> List[str]:
        return list(self.elective_course)

    def details(self) -> Tuple[str, str, List[str]]:
        """ return vale to display in table """
        return [self._major, sorted(self.required_course), sorted(self.elective_course)]


class Student:
    """store student data"""

    def __init__(self, cwid: str, name: str, major: str, required: str, electives: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()
        self._remaining_req: List[str] = required
        self._remaining_elec: List[str] = electives
        self._grade: Dict[str, float] = {
            'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 'C': 2.0}
        self._smry_st:  Dict[str, str] = dict()

    def add_coursework(self, course: str, grade: str) -> None:
        """ grads and course are added """
        self._smry_st[course] = grade
        if grade in self._grade.keys():
            self._courses[course] = grade
        else:
            return self._courses

    def calculate_GPA(self, gd: Dict[str, int]) -> float or str:
        sum: float = 0.00
        count: int = 0
        isEmpty = not gd
        if isEmpty == True:
            return 0.00

        for k, v in gd.items():
            if v == '':
                count = -1
                continue
            if v in self._grade:
                sum = sum+self._grade[v]
                count += 1
            else:
                count += 1
        if count == -1:
            return "NA"
        elif count == 0:
            return 0.00
        return format((sum/count), '.2f')

    def cal_remaining_course(self, required_cors, completed_cors) -> List[str]:
        remaining_course_left: list()
        remaining_course_left = required_cors-completed_cors
        return remaining_course_left

    def cal_elective(self, elected_corse, completed_cors) -> List[str]:
        for n in elected_corse:
            for m in list(completed_cors):
                if n == m:
                    return []
        return elected_corse

    def details(self) -> Tuple[str, str, List[str], List[str], List[str], int]:
        """ return vale to display in table """
        return [self._cwid, self._name, self._major, sorted(self._courses.keys()), sorted(self.cal_remaining_course(self._remaining_req, self._courses.keys())), sorted(self.cal_elective(self._remaining_elec, self._courses.keys())), self.calculate_GPA(self._smry_st)]


class Instructor:
    """ store Instructor data """

    def __init__(self, cwid: str, name: str, deptarment: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._deptarment: str = deptarment
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_student_to_course(self, course: str) -> None:
        """ map the course with student """
        self._courses[course] += 1

    def details(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """ Yield  to display in table """
        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._deptarment, course, count]


def main():
    studenrRepo = Repository(
        'E:/SSW-810-Special Topics/SSW-810-Yash/Assignment/11')
    studenrRepo.major_tab()
    studenrRepo.stud_table()
    studenrRepo.instruct_table()
    studenrRepo.student_grade_table_db(
        'E:/SSW-810-Special Topics/SSW-810-Yash/Assignment/11/810_assginemt11')


if __name__ == '__main__':
    main()
