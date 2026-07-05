
"""
student manager basic - aliakbartnt
"""
# import
import os
import sys
import json

# ====== main dict ======
students = {}  # {lower_id: {'id': orig, 'name': name, 'grades': {lower_cid: grade}}}
courses = {}   # {lower_cid: {'id': orig, 'name': name}}

student_counter = 1
course_counter = 1
id_mode = 'manual'  # 'manual' or 'auto'

# ====== function helper ======
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
        print("بازگشت به منوی اصلی...")
        return None
    return inp

# ====== list ======
def list_students():
    if not students:
        print("❌ هیچ دانشجویی ثبت نشده است.")
        return False
    print("\n--- لیست دانشجویان ---")
    for data in students.values():
        print(f"  {data['id']}: {data['name']}")
    print("-------------------------\n")
    return True

def list_courses():
    if not courses:
        print("❌ هیچ درسی ثبت نشده است.")
        return False
    print("\n--- لیست دروس ---")
    for data in courses.values():
        print(f"  {data['id']}: {data['name']}")
    print("------------------------\n")
    return True

# ====== main ======
def add_student():
    global id_mode
    if id_mode == 'manual':
        sid = safe_input("شناسه دانشجو را وارد کنید (یا 'exit' برای لغو): ")
        if sid is None:
            return
        if not sid:
            print("❌ شناسه نمی‌تواند خالی باشد.")
            return
        if student_exists(sid):
            print(f"❌ دانشجویی با شناسه '{sid}' از قبل وجود دارد.")
            return
    else:
        sid = None
    
    name = safe_input("نام دانشجو را وارد کنید (یا 'exit' برای لغو): ")
    if name is None:
        return
    if not name:
        print("❌ نام نمی‌تواند خالی باشد.")
        return
    
    if id_mode == 'auto':
        sid = generate_student_id()
        print(f"✅ شناسه دانشجو تولید شد: {sid}")
    
    students[sid.lower()] = {'id': sid, 'name': name, 'grades': {}}
    print(f"✅ دانشجو با شناسه '{sid}' و نام '{name}' اضافه شد.")

def add_course():
    global id_mode
    if id_mode == 'manual':
        cid = safe_input("شناسه درس را وارد کنید (یا 'exit' برای لغو): ")
        if cid is None:
            return
        if not cid:
            print("❌ شناسه نمی‌تواند خالی باشد.")
            return
        if course_exists(cid):
            print(f"❌ درسی با شناسه '{cid}' از قبل وجود دارد.")
            return
    else:
        cid = None
    
    name = safe_input("نام درس را وارد کنید (یا 'exit' برای لغو): ")
    if name is None:
        return
    if not name:
        print("❌ نام نمی‌تواند خالی باشد.")
        return
    
    if id_mode == 'auto':
        cid = generate_course_id()
        print(f"✅ شناسه درس تولید شد: {cid}")
    
    courses[cid.lower()] = {'id': cid, 'name': name}
    print(f"✅ درس با شناسه '{cid}' و نام '{name}' اضافه شد.")

def set_grade():
    if not list_students():
        print("❌ امکان ثبت نمره وجود ندارد زیرا هیچ دانشجویی وجود ندارد.")
        return
    sid = safe_input("شناسه دانشجو را از لیست بالا وارد کنید (یا 'exit' برای لغو): ")
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(f"❌ دانشجویی با شناسه '{sid}' یافت نشد.")
        return
    print(f"✅ دانشجوی انتخاب‌شده: {st['name']}")
    
    if not list_courses():
        print("❌ امکان ثبت نمره وجود ندارد زیرا هیچ درسی وجود ندارد.")
        return
    cid = safe_input("شناسه درس را از لیست بالا وارد کنید (یا 'exit' برای لغو): ")
    if cid is None:
        return
    cs = get_course(cid)
    if not cs:
        print(f"❌ درسی با شناسه '{cid}' یافت نشد.")
        return
    print(f"✅ درس انتخاب‌شده: {cs['name']}")
    
    gr = safe_input("نمره را وارد کنید (عدد) (یا 'exit' برای لغو): ")
    if gr is None:
        return
    try:
        grade = float(gr)
    except:
        print("❌ نمره باید یک عدد باشد.")
        return
    
    st['grades'][cid.lower()] = grade
    print(f"✅ نمره {grade} برای دانشجو '{st['name']}' در درس '{cs['name']}' ثبت شد.")

def edit_student():
    if not list_students():
        return
    sid = safe_input("شناسه دانشجو را برای ویرایش وارد کنید (یا 'exit' برای لغو): ")
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(f"❌ دانشجویی با شناسه '{sid}' یافت نشد.")
        return
    print(f"✅ دانشجوی انتخاب‌شده: {st['name']}")
    
    new_name = safe_input("نام جدید را وارد کنید (یا 'exit' برای لغو): ")
    if new_name is None:
        return
    if not new_name:
        print("❌ نام نمی‌تواند خالی باشد.")
        return
    st['name'] = new_name
    print(f"✅ نام دانشجو با شناسه '{st['id']}' به '{new_name}' تغییر یافت.")

def edit_course():
    if not list_courses():
        return
    cid = safe_input("شناسه درس را برای ویرایش وارد کنید (یا 'exit' برای لغو): ")
    if cid is None:
        return
    cs = get_course(cid)
    if not cs:
        print(f"❌ درسی با شناسه '{cid}' یافت نشد.")
        return
    print(f"✅ درس انتخاب‌شده: {cs['name']}")
    
    new_name = safe_input("نام جدید درس را وارد کنید (یا 'exit' برای لغو): ")
    if new_name is None:
        return
    if not new_name:
        print("❌ نام نمی‌تواند خالی باشد.")
        return
    cs['name'] = new_name
    print(f"✅ نام درس با شناسه '{cs['id']}' به '{new_name}' تغییر یافت.")

def delete_student():
    if not list_students():
        return
    sid = safe_input("شناسه دانشجو را برای حذف وارد کنید (یا 'exit' برای لغو): ")
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(f"❌ دانشجویی با شناسه '{sid}' یافت نشد.")
        return
    print(f"✅ دانشجوی انتخاب‌شده: {st['name']}")
    
    confirm = safe_input(f"آیا از حذف دانشجو '{st['name']}' مطمئن هستید؟ (y/n) (یا 'exit' برای لغو): ")
    if confirm is None:
        return
    if confirm.lower() == 'y':
        del students[sid.lower()]
        print(f"✅ دانشجو با شناسه '{st['id']}' حذف شد.")
    else:
        print("❌ عملیات لغو شد.")

def delete_course():
    if not list_courses():
        return
    cid = safe_input("شناسه درس را برای حذف وارد کنید (یا 'exit' برای لغو): ")
    if cid is None:
        return
    cs = get_course(cid)
    if not cs:
        print(f"❌ درسی با شناسه '{cid}' یافت نشد.")
        return
    print(f"✅ درس انتخاب‌شده: {cs['name']}")
    
    confirm = safe_input(f"آیا از حذف درس '{cs['name']}' و تمام نمرات مربوطه مطمئن هستید؟ (y/n) (یا 'exit' برای لغو): ")
    if confirm is None:
        return
    if confirm.lower() == 'y':
        lower = cid.lower()
        del courses[lower]
        for st in students.values():
            if lower in st['grades']:
                del st['grades'][lower]
        print(f"✅ درس با شناسه '{cs['id']}' و تمام نمرات مربوطه حذف شد.")
    else:
        print("❌ عملیات لغو شد.")

def show_student():
    if not list_students():
        return
    sid = safe_input("شناسه دانشجو را وارد کنید (یا 'exit' برای لغو): ")
    if sid is None:
        return
    st = get_student(sid)
    if not st:
        print(f"❌ دانشجویی با شناسه '{sid}' یافت نشد.")
        return
    print(f"✅ دانشجوی انتخاب‌شده: {st['name']}")
    
    print("\n📋 اطلاعات دانشجو:")
    print(f"شناسه: {st['id']}")
    print(f"نام: {st['name']}")
    if st['grades']:
        print("نمرات:")
        for cid_low, grade in st['grades'].items():
            cs = courses.get(cid_low)
            cid_show = cs['id'] if cs else cid_low
            cname_show = cs['name'] if cs else "نامشخص"
            print(f"  {cid_show} ({cname_show}): {grade}")
    else:
        print("⚠️ هیچ نمره‌ای ثبت نشده است.")
    print()

def show_all():
    if not students:
        print("❌ هیچ دانشجویی ثبت نشده است.")
        return
    print("\n--- همه دانشجویان ---")
    for st in students.values():
        print(f"شناسه: {st['id']}, نام: {st['name']}")
        if st['grades']:
            print("  نمرات:")
            for cid_low, grade in st['grades'].items():
                cs = courses.get(cid_low)
                cid_show = cs['id'] if cs else cid_low
                cname_show = cs['name'] if cs else "نامشخص"
                print(f"    {cid_show} ({cname_show}): {grade}")
        else:
            print("  (هیچ نمره‌ای ثبت نشده)")
    print("---------------------\n")

def show_menu():
    print("""
===== منو =====
۱. افزودن دانشجو
۲. افزودن درس
۳. ثبت نمره
۴. ویرایش دانشجو
۵. ویرایش درس
۶. حذف دانشجو
۷. حذف درس
۸. نمایش دانشجو
۹. نمایش همه دانشجویان
۰. خروج
===============
""")

# ====== Main func ======
def main():
    global id_mode
    print("به سیستم مدیریت نمرات دانشجویان خوش آمدید.")
    
    # Choice mode 
    while True:
        ch = input("آیا می‌خواهید شناسه‌ها را دستی وارد کنید یا خودکار تولید شوند؟ (m/a): ").strip().lower()
        if ch in ('m', 'manual'):
            id_mode = 'manual'
            print("✅ حالت شناسه به حالت دستی تنظیم شد.")
            break
        elif ch in ('a', 'auto'):
            id_mode = 'auto'
            print("✅ حالت شناسه به حالت خودکار تنظیم شد.")
            break
        else:
            print("❌ ورودی نامعتبر. لطفاً 'm' برای دستی یا 'a' برای خودکار وارد کنید.")
    
    show_menu()
    
    while True:
        try:
            choice = input("\nشماره مورد نظر را وارد کنید: ").strip()
            if choice == '0':
                print("خروج از برنامه. خدانگهدار!")
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
                print("❌ انتخاب نامعتبر. لطفاً عددی بین ۰ تا ۹ وارد کنید.")
            
            if choice != '0':
                show_menu()
        except KeyboardInterrupt:
            print("\nعملیات متوقف شد. در حال خروج...")
            break

if __name__ == '__main__':
    main()