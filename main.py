"""
student manager - aliakbartnt
copyright 
!!! dont touch my copyright my app license is MIT And you must cite the source. !!!

"""
import time
import os
import sys
import json
import yaml
import re
import shutil
from datetime import datetime

# ====== language select ======
def choose_lang():
    while True:
        lang = input("Select language / انتخاب زبان (en/fa): ").strip().lower()
        if lang in ('en', 'fa'):
            return lang
        print("Select Language en /fa")

LANG = choose_lang()

# ====== load language class ======
class MsgLoader:
    def __init__(self, lang):
        self.lang = lang
        self.messages = self._get_msgs()
    
    def _get_msgs(self):
        base = os.path.dirname(os.path.abspath(__file__))
        fname = 'message_en.yml' if self.lang == 'en' else 'message_fa.yml'
        path = os.path.join(base, 'messages', fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"error for reading lang file: {e}")
            sys.exit(1)
    
    def get(self, key, **kwargs):
        msg = self.messages.get(key, key)
        if kwargs:
            msg = msg.format(**kwargs)
        if self.lang == 'fa':
            msg = '\u202B' + msg + '\u202C'
        return msg

MSG = MsgLoader(LANG)

# ====== personal info ======
APP_VERSION = "2.0"
DEVELOPER = "Aliakbartnt"
START_TIME = time.time()

def show_current_time():
    now = datetime.now()
    if LANG == 'en':
        return now.strftime("%A, %B %d, %Y - %H:%M:%S")
    else:
        return now.strftime("%A, %B %d, %Y - %H:%M:%S")

# ====== Main dict ======
students = {}  # {lower_id: {'id': orig, 'name': name, 'grades': {lower_cid: grade}}}
courses = {}   # {lower_cid: {'id': orig, 'name': name}}
# variable
student_counter = 1
course_counter = 1
id_mode = 'manual'  # 'manual' or 'auto'

# ====== Storage paths ======
STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Storage')
DATA_FILE = os.path.join(STORAGE_DIR, 'data.json')
BACKUP_DIR = os.path.join(STORAGE_DIR, 'backups')

# ====== Function helper ======
def extract_number_from_id(id_str):
    """extracting last ID S1, C2, ..."""
    match = re.search(r'\d+', id_str)
    if match:
        return int(match.group())
    return 0

def calculate_max_counter(data_dict):
    """Find last ID"""
    max_num = 0
    for data in data_dict.values():
        num = extract_number_from_id(data['id'])
        if num > max_num:
            max_num = num
    return max_num + 1  # last ID + 1

def generate_student_id():
    global student_counter
    new_id = f"S{student_counter}"
    student_counter += 1
    return new_id

def generate_course_id():
    global course_counter
    new_id = f"C{course_counter}"
    course_counter += 1
    return new_id

def get_student(sid):
    return students.get(sid.lower())

def get_course(cid):
    return courses.get(cid.lower())

def student_exists(sid):
    return sid.lower() in students

def course_exists(cid):
    return cid.lower() in courses

def safe_input(prompt):
    inp = input(prompt).strip()
    if inp.lower() == 'exit':
        print(MSG.get('return_to_menu'))
        return None
    return inp

def calc_average(student_data):
    """Calnculator avg student"""
    grades = student_data.get('grades', {}).values()
    if not grades:
        return 0.0
    return sum(grades) / len(grades)

# ====== Backup functions ======
def ensure_backup_dir():
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating backup folder: {e}")

def create_backup():
    """Create a backup of data.json with timestamp"""
    ensure_backup_dir()
    if not os.path.exists(DATA_FILE):
        print(MSG.get('backup_no_data'))
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.json"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        shutil.copy2(DATA_FILE, backup_path)
        print(MSG.get('backup_success', path=backup_path))
        return True
    except Exception as e:
        print(MSG.get('backup_error', error=str(e)))
        return False

# ====== Save & Load functions ======
def ensure_storage_dir():
    try:
        os.makedirs(STORAGE_DIR, exist_ok=True)
    except Exception as e:
        print(f"❌ Error for folder create Storage: {e}")

def save_to_file():
    try:
        data = {
            'students': students,
            'courses': courses,
            'student_counter': student_counter,
            'course_counter': course_counter,
            'version': APP_VERSION,
            'last_saved': time.time(),
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Error to save: {e}")
        fallback = os.path.join(os.getcwd(), 'data_backup.json')
        try:
            with open(fallback, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ data for backup save to {fallback} .")
        except:
            pass

def load_from_file():
    global students, courses, student_counter, course_counter
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print("⚠️ Data file is empty. Starting with empty data.")
                    return
                data = json.loads(content)
            
            students = data.get('students', {})
            courses = data.get('courses', {})
            
            # ====== Version Check ======
            file_version = data.get('version', 'unknown')
            if file_version != APP_VERSION:
                print("\n" + "=" * 60)
                print(MSG.get('version_mismatch_warning'))
                print(MSG.get('version_mismatch_detail', 
                             file_ver=file_version, 
                             app_ver=APP_VERSION))
                print("=" * 60 + "\n")
                
                while True:
                    confirm = input(MSG.get('version_mismatch_confirm')).strip().lower()
                    if confirm in ('y', 'yes'):
                        print(MSG.get('version_mismatch_continue'))
                        break
                    elif confirm in ('n', 'no'):
                        print(MSG.get('version_mismatch_abort'))
                        print("Exiting program. Please backup manually or update.")
                        sys.exit(0)
                    else:
                        print(MSG.get('version_mismatch_invalid'))
            
            # ====== Fix: Calculate counters from existing IDs ======
            saved_student_counter = data.get('student_counter', 1)
            saved_course_counter = data.get('course_counter', 1)
            
            real_student_counter = calculate_max_counter(students)
            real_course_counter = calculate_max_counter(courses)
            
            student_counter = max(saved_student_counter, real_student_counter)
            course_counter = max(saved_course_counter, real_course_counter)
            
            print("✅ Load data successful.")
            print(f"ℹ️ Student counter: {student_counter}, Course counter: {course_counter}")
            
        except json.JSONDecodeError:
            print("⚠️ Data file is corrupted. Starting with empty data.")
            students = {}
            courses = {}
            student_counter = 1
            course_counter = 1
        except Exception as e:
            print(f"⚠️ Error to loading: {e}")
            students = {}
            courses = {}
            student_counter = 1
            course_counter = 1
    else:
        print("ℹ️ No data file found. Starting with empty data.")

# ====== list ======
def list_students():
    if not students:
        print(MSG.get('no_students_registered'))
        return False
    print(MSG.get('list_students_title'))
    for data in students.values():
        print(MSG.get('list_students_line', id=data['id'], name=data['name']))
    print(MSG.get('list_students_footer'))
    return True

def list_courses():
    if not courses:
        print(MSG.get('no_courses'))
        return False
    print(MSG.get('list_courses_title'))
    for data in courses.values():
        print(MSG.get('list_courses_line', id=data['id'], name=data['name']))
    print(MSG.get('list_courses_footer'))
    return True

# ====== Summary Report ======
def show_summary():
    print("\n" + "=" * 50)
    print(MSG.get('summary_title'))
    print("=" * 50)
    
    if not students and not courses:
        print(MSG.get('summary_no_data'))
        print("=" * 50 + "\n")
        return
    
    print(MSG.get('summary_students_count', count=len(students)))
    print(MSG.get('summary_courses_count', count=len(courses)))
    print()
    
    # information students
    for st in students.values():
        print(MSG.get('summary_student_header', name=st['name'], id=st['id']))
        if st['grades']:
            for cid_low, grade in st['grades'].items():
                cs = courses.get(cid_low)
                cname_show = cs['name'] if cs else "Unknown"
                print(MSG.get('summary_student_grade_line', course=cname_show, grade=grade))
            avg = calc_average(st)
            print(MSG.get('summary_student_avg', avg=avg))
        else:
            print(MSG.get('summary_student_no_grades'))
        print()
    
    # information courses
    for cs in courses.values():
        count = 0
        for st in students.values():
            if cs['id'].lower() in st['grades']:
                count += 1
        print(MSG.get('summary_course_detail', name=cs['name'], id=cs['id'], count=count))
    
    print("=" * 50 + "\n")

# ====== Main ======
def add_student():
    global id_mode
    if id_mode == 'manual':
        sid = safe_input(MSG.get('student_id_prompt'))
        if sid is None:
            return
        if not sid:
            print(MSG.get('student_id_empty'))
            return
        if student_exists(sid):
            print(MSG.get('student_id_exists', id=sid))
            return
    else:
        sid = None
    
    name = safe_input(MSG.get('student_name_prompt'))
    if name is None:
        return
    if not name:
        print(MSG.get('name_empty'))
        return
    
    if id_mode == 'auto':
        sid = generate_student_id()
        print(MSG.get('student_id_generated', id=sid))
    
    students[sid.lower()] = {'id': sid, 'name': name, 'grades': {}}
    save_to_file()
    print(MSG.get('student_added', id=sid, name=name))

def add_course():
    global id_mode
    if id_mode == 'manual':
        cid = safe_input(MSG.get('course_id_prompt'))
        if cid is None:
            return
        if not cid:
            print(MSG.get('course_id_empty'))
            return
        if course_exists(cid):
            print(MSG.get('course_id_exists', id=cid))
            return
    else:
        cid = None
    
    name = safe_input(MSG.get('course_name_prompt'))
    if name is None:
        return
    if not name:
        print(MSG.get('name_empty'))
        return
    
    if id_mode == 'auto':
        cid = generate_course_id()
        print(MSG.get('course_id_generated', id=cid))
    
    courses[cid.lower()] = {'id': cid, 'name': name}
    save_to_file()
    print(MSG.get('course_added', id=cid, name=name))

def set_grade():
    if not list_students():
        print(MSG.get('no_students'))
        return
    sid = safe_input(MSG.get('student_id_list_prompt'))
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(MSG.get('student_not_found', id=sid))
        return
    print(MSG.get('selected_student', name=st['name']))
    
    if not list_courses():
        print(MSG.get('no_courses'))
        return
    cid = safe_input(MSG.get('course_id_list_prompt'))
    if cid is None:
        return
    cs = get_course(cid)
    if not cs:
        print(MSG.get('course_not_found', id=cid))
        return
    print(MSG.get('selected_course', name=cs['name']))
    
    gr = safe_input(MSG.get('grade_prompt'))
    if gr is None:
        return
    try:
        grade = float(gr)
    except:
        print(MSG.get('grade_invalid'))
        return
    
    st['grades'][cid.lower()] = grade
    save_to_file()
    print(MSG.get('grade_recorded', grade=grade, student=st['name'], course=cs['name']))

def edit_student():
    if not list_students():
        return
    sid = safe_input(MSG.get('edit_student_id_prompt'))
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(MSG.get('student_not_found', id=sid))
        return
    print(MSG.get('selected_student', name=st['name']))
    
    new_name = safe_input(MSG.get('edit_student_name_prompt'))
    if new_name is None:
        return
    if not new_name:
        print(MSG.get('name_empty'))
        return
    st['name'] = new_name
    save_to_file()
    print(MSG.get('student_renamed', id=st['id'], name=new_name))

def edit_course():
    if not list_courses():
        return
    cid = safe_input(MSG.get('edit_course_id_prompt'))
    if cid is None:
        return
    cs = get_course(cid)
    if not cs:
        print(MSG.get('course_not_found', id=cid))
        return
    print(MSG.get('selected_course', name=cs['name']))
    
    new_name = safe_input(MSG.get('edit_course_name_prompt'))
    if new_name is None:
        return
    if not new_name:
        print(MSG.get('name_empty'))
        return
    cs['name'] = new_name
    save_to_file()
    print(MSG.get('course_renamed', id=cs['id'], name=new_name))

def delete_student():
    if not list_students():
        return
    sid = safe_input(MSG.get('delete_student_id_prompt'))
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(MSG.get('student_not_found', id=sid))
        return
    print(MSG.get('selected_student', name=st['name']))
    
    confirm = safe_input(MSG.get('delete_student_confirm', name=st['name']))
    if confirm is None:
        return
    if confirm.lower() == 'y':
        del students[sid.lower()]
        save_to_file()
        print(MSG.get('student_deleted', id=st['id']))
    else:
        print(MSG.get('delete_cancelled'))

def delete_course():
    if not list_courses():
        return
    cid = safe_input(MSG.get('delete_course_id_prompt'))
    if cid is None:
        return
    cs = get_course(cid)
    if not cs:
        print(MSG.get('course_not_found', id=cid))
        return
    print(MSG.get('selected_course', name=cs['name']))
    
    confirm = safe_input(MSG.get('delete_course_confirm', name=cs['name']))
    if confirm is None:
        return
    if confirm.lower() == 'y':
        lower = cid.lower()
        del courses[lower]
        for st in students.values():
            if lower in st['grades']:
                del st['grades'][lower]
        save_to_file()
        print(MSG.get('course_deleted', id=cs['id']))
    else:
        print(MSG.get('delete_cancelled'))

def show_student():
    if not list_students():
        return
    sid = safe_input(MSG.get('show_student_id_prompt'))
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(MSG.get('student_not_found', id=sid))
        return
    print(MSG.get('selected_student', name=st['name']))
    
    print(MSG.get('show_student_info_title'))
    print(MSG.get('show_student_id', id=st['id']))
    print(MSG.get('show_student_name', name=st['name']))
    if st['grades']:
        print(MSG.get('show_student_grades_title'))
        for cid_low, grade in st['grades'].items():
            cs = courses.get(cid_low)
            cid_show = cs['id'] if cs else cid_low
            cname_show = cs['name'] if cs else "Unknown"
            print(MSG.get('show_student_grade_line', course_id=cid_show, course_name=cname_show, grade=grade))
    else:
        print(MSG.get('show_student_no_grades'))
    print()

def show_all():
    if not students:
        print(MSG.get('no_students_registered'))
        return
    print(MSG.get('show_all_title'))
    for st in students.values():
        print(MSG.get('show_all_student_line', id=st['id'], name=st['name']))
        if st['grades']:
            print(MSG.get('show_all_grades_title'))
            for cid_low, grade in st['grades'].items():
                cs = courses.get(cid_low)
                cid_show = cs['id'] if cs else cid_low
                cname_show = cs['name'] if cs else "Unknown"
                print(MSG.get('show_all_grade_line', course_id=cid_show, course_name=cname_show, grade=grade))
        else:
            print(MSG.get('show_all_no_grades'))
    print(MSG.get('show_all_footer'))

# ====== Search by name ======
def search_student_by_name():
    if not students:
        print(MSG.get('no_students_registered'))
        return
    
    term = safe_input(MSG.get('search_name_prompt'))
    if term is None:
        return
    if not term:
        print(MSG.get('search_name_empty'))
        return
    
    term_lower = term.lower()
    found = []
    for data in students.values():
        if term_lower in data['name'].lower():
            found.append(data)
    
    if not found:
        print(MSG.get('search_no_result', name=term))
        return
    
    print(MSG.get('search_result_title', count=len(found)))
    for data in found:
        avg = calc_average(data)
        print(MSG.get('search_result_line', id=data['id'], name=data['name'], avg=avg))
    print()

# ====== Sort by average ======
def sort_students_by_average():
    if not students:
        print(MSG.get('no_students_registered'))
        return
    
    order = safe_input(MSG.get('sort_order_prompt'))
    if order is None:
        return
    if order.lower() not in ('d', 'desc', 'a', 'asc'):
        print(MSG.get('sort_order_invalid'))
        return
    
    student_list = []
    for data in students.values():
        avg = calc_average(data)
        student_list.append((data, avg))
    
    if order.lower() in ('d', 'desc'):
        student_list.sort(key=lambda x: x[1], reverse=True)
        sort_label = MSG.get('sort_descending')
    else:
        student_list.sort(key=lambda x: x[1])
        sort_label = MSG.get('sort_ascending')
    
    print(MSG.get('sort_result_title', order=sort_label))
    for data, avg in student_list:
        print(MSG.get('sort_result_line', id=data['id'], name=data['name'], avg=avg))
    print()

# ====== Delete all data ======
def delete_all_data():
    confirm1 = safe_input(MSG.get('delete_all_prompt'))
    if confirm1 is None:
        return
    if confirm1.lower() != 'y':
        print(MSG.get('delete_all_cancelled'))
        return
    
    confirm2 = safe_input(MSG.get('delete_all_confirm'))
    if confirm2 is None:
        return
    if confirm2.lower() != 'y':
        print(MSG.get('delete_all_cancelled'))
        return
    
    global students, courses, student_counter, course_counter
    students.clear()
    courses.clear()
    student_counter = 1
    course_counter = 1
    save_to_file()
    print(MSG.get('delete_all_success'))

# ====== menu ======
def show_menu():
    print(MSG.get('menu'))

# ====== Main func ======
def main():
    global id_mode
    
    # show my information
    print("\n" + "=" * 50)
    print(MSG.get('welcome'))
    print(f"📅 {show_current_time()}")
    print(f"👤 Developer: {DEVELOPER}")
    print(f"📌 Version: {APP_VERSION}")
    time.sleep(5)
    print("=" * 50 + "\n")
    
    # choice summery or manage
    while True:
        mode_choice = input(MSG.get('mode_prompt')).strip().lower()
        if mode_choice in ('m', 'manage'):
            print(MSG.get('mode_manage'))
            break
        elif mode_choice in ('s', 'summary'):
            print(MSG.get('mode_summary'))
            ensure_storage_dir()
            load_from_file()
            show_summary()
            time.sleep(5)
            print(MSG.get('exit_program'))
            time.sleep(1)
            sys.exit(0)
        else:
            print(MSG.get('mode_invalid'))
    
    # data load
    ensure_storage_dir()
    load_from_file()
    
    # choise id mode
    while True:
        ch = input(MSG.get('id_mode_prompt')).strip().lower()
        if ch in ('m', 'manual'):
            id_mode = 'manual'
            print(MSG.get('id_mode_manual'))
            break
        elif ch in ('a', 'auto'):
            id_mode = 'auto'
            print(MSG.get('id_mode_auto'))
            break
        else:
            print(MSG.get('id_mode_invalid'))
    
    show_menu()
    
    while True:
        try:
            choice = input(MSG.get('menu_choice_prompt')).strip()
            
            # ====== Exit with backup option ======
            if choice == '0':
                print("\n" + "=" * 50)
                backup_choice = input(MSG.get('exit_backup_prompt')).strip().lower()
                if backup_choice in ('y', 'yes'):
                    print(MSG.get('exit_backup_creating'))
                    create_backup()
                    time.sleep(1)
                elif backup_choice in ('n', 'no'):
                    print(MSG.get('exit_backup_skip'))
                else:
                    print(MSG.get('exit_backup_invalid'))
                    # if choice dont exist exit
                
                print(MSG.get('exit_program'))
                time.sleep(1)
                break
            elif choice == '1':
                add_student()
            elif choice == '2':
                add_course()
            elif choice == '3':
                set_grade()
            elif choice == '4':
                edit_student()
            elif choice == '5':
                edit_course()
            elif choice == '6':
                delete_student()
            elif choice == '7':
                delete_course()
            elif choice == '8':
                show_student()
            elif choice == '9':
                show_all()
            elif choice == '10':
                search_student_by_name()
            elif choice == '11':
                sort_students_by_average()
            elif choice == '12':
                delete_all_data()
            else:
                print(MSG.get('invalid_choice'))
            
            if choice != '0':
                time.sleep(3)  # time after show menu
                show_menu()
        except KeyboardInterrupt:
            print(MSG.get('interrupted'))
            break

if __name__ == '__main__':
    main()