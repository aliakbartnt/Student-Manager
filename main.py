
"""
student manager basic - aliakbartnt
"""

import os
import sys
import json
import yaml

# ====== language select ======
def choose_lang():
    while True:
        lang = input("Select language / انتخاب زبان (en/fa): ").strip().lower()
        if lang in ('en', 'fa'):
            return lang
        print("لطفاً en یا fa رو انتخاب کن.")

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
            print(f"خطا تو خوندن فایل پیام: {e}")
            sys.exit(1)
    
    def get(self, key, **kwargs):
        msg = self.messages.get(key, key)
        if kwargs:
            msg = msg.format(**kwargs)
        if self.lang == 'fa':
            msg = '\u202B' + msg + '\u202C'
        return msg

MSG = MsgLoader(LANG)

# ====== Main dict ======
students = {}  # {lower_id: {'id': orig, 'name': name, 'grades': {lower_cid: grade}}}
courses = {}   # {lower_cid: {'id': orig, 'name': name}}

student_counter = 1
course_counter = 1
id_mode = 'manual'  # 'manual' or 'auto'

# ====== Function helper ======
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
            cname_show = cs['name'] if cs else "نامشخص"
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
                cname_show = cs['name'] if cs else "نامشخص"
                print(MSG.get('show_all_grade_line', course_id=cid_show, course_name=cname_show, grade=grade))
        else:
            print(MSG.get('show_all_no_grades'))
    print(MSG.get('show_all_footer'))

def show_menu():
    print(MSG.get('menu'))

# ====== Main func ======
def main():
    global id_mode
    print(MSG.get('welcome'))
    
    # Id Gen Choice mode 
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
            if choice == '0':
                print(MSG.get('exit_program'))
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
            else:
                print(MSG.get('invalid_choice'))
            
            if choice != '0':
                show_menu()
        except KeyboardInterrupt:
            print(MSG.get('interrupted'))
            break

if __name__ == '__main__':
    main()