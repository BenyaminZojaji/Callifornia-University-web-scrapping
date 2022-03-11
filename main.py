import csv
import logging
from selenium import webdriver

logger = logging.getLogger('__main__')

class UCOP:
    Course_Page_Url = 'https://myeap.eap.ucop.edu/Galileo/service/coursecatalog/Coursecatalog.aspx?direct=yes&programid=83&_ga=2.159220154.1488026999.1519671986-1740273094.1501095366'
    University = 'University of California Office of the President'
    Abbreviation = 'UCOP'
    University_Homepage = 'https://www.ucop.edu/'
    
    # Below fields didn't find in the website
    Professor = None
    Objective = None
    Prerequisite = None
    Required_Skills = None
    Outcome = None
    References = None
    Scores = None
    Projects = None
    Professor_Homepage = None
    
    def __init__(self):
        self.output_file = csv.writer(open(f'data/{self.__class__.__name__}.csv', 'w', encoding='utf-8', newline=''))
        self.output_file.writerow(
            ['University', 'Abbreviation', 'Department', 'Course title', 'Unit', 'Professor', 'Objective',
             'Prerequisite', 'Required Skills', 'Outcome', 'References', 'Scores', 'Description', 'Projects',
             'University Homepage', 'Course Homepage', 'Professor Homepage']
        )
        self.driver = webdriver.Firefox()
        self.course_count = 0

    def get_course_data(self, course):
        course.click()
        self.driver.implicitly_wait(5)
        self.driver.switch_to.window(self.driver.window_handles[1])
        Department_Name = self.driver.find_element_by_xpath('/html/body/form/div/span/div/table/tbody/tr[12]/td[2]')
        Course_Title = self.driver.find_element_by_xpath('/html/body/form/div/span/div/table/tbody/tr[6]/td[2]')
        Unit_Count = self.driver.find_element_by_xpath('/html/body/form/div/span/div/table/tbody/tr[8]/td[2]')
        Description = self.driver.find_element_by_xpath('/html/body/form/div/span/div/table/tbody/tr[9]/td[2]')
        
        return Department_Name.text.strip(), Course_Title.text.strip(), Unit_Count.text.strip().split(' ')[0], Description.text.strip()

    def save_course_data(self, university, abbreviation, department_name, course_title, unit_count, professor,
                         objective, prerequisite, required_skills, outcome, references, scores, description, projects,
                         university_homepage, course_homepage, professor_homepage):
        try:
            self.output_file.writerow([university, abbreviation, department_name, course_title, unit_count, professor,
                                       objective, prerequisite, required_skills, outcome, references, scores,
                                       description, projects, university_homepage, course_homepage, professor_homepage])

            self.course_count += 1
        except Exception as e:
            logger.error(
                f"{abbreviation} - {department_name} - {course_title}: An error occurred while saving course data: {e}"
            )

    def handler(self):
        self.driver.get(self.Course_Page_Url)
        courses = []
        i=2
        while True:
            try:
                tmp = self.driver.find_element_by_xpath(f'/html/body/form/div/table/tbody/tr/td/div/table/tbody/tr[3]/td/span[2]/table/tbody/tr[{i}]/td[7]/span/a')
                courses.append(tmp)
                self.course_count += 1
                i += 1
            except:
                break
        for course in courses:
            Course_Homepage = course.get_attribute('href')
            Department_Name, Course_Title, Unit_Count, Description = self.get_course_data(course)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

            self.save_course_data(
                    self.University, self.Abbreviation, Department_Name, Course_Title, Unit_Count,
                    self.Professor, self.Objective, self.Prerequisite, self.Required_Skills, self.Outcome, self.References, self.Scores,
                    Description, self.Projects, self.University_Homepage, Course_Homepage, self.Professor_Homepage
                )

            logger.info(f"{self.Abbreviation}: {course.text} department's data was crawled successfully.")

        logger.info(f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")
            

if __name__=='__main__':
    ucop = UCOP()
    ucop.handler()