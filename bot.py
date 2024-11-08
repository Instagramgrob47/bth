import sqlite3
import telebot
from sqlite3 import Error
from telebot import types
import re

# إعداد قاعدة البيانات
def open_db(name):
    try:
        db = sqlite3.connect(f"{name}.sqlite")
        db.execute('PRAGMA journal_mode=WAL')
        return db
    except Error as e:
        print(e)

def close_db(db):
    if db:
        db.close()

# دالة لإزالة الأحرف غير العربية
def filter_arabic(text):
    return re.sub(r'[^\u0600-\u06FF ]+', '', text)

# دالة للبحث في قاعدة بيانات m واسترجاع المعلومات المطلوبة
def search_family(db, name):
    first_name, father_name, grand_name = name.split(' ')
    query = f"""
    SELECT RC_NO, FAM_NO, SEQ_NO, P_FIRST, P_FATHER, P_GRAND, P_RELATION, P_BIRTH,
           SS_BR_NO, SS_LG_NO, SS_PG_NO, SS_ID_NO, P_CASE, P_JOB, P_ISUDT, SOC,
           P_SALARY, P_WORK, P_MOTHER, GR_MOTHER, T_JOB, MARK, SS_BR_NM
    FROM person
    WHERE P_FIRST LIKE '{first_name}%' AND P_FATHER LIKE '{father_name}%' AND P_GRAND LIKE '{grand_name}%'
    """
    results = []
    for i in db.execute(query):
        try:
            clean_name = f"{filter_arabic(i[3].strip())} {filter_arabic(i[4].strip())} {filter_arabic(i[5].strip())}"
            results.append({
                'رقم الوكيل': i[0],
                'رقم العائلة': i[1],
                'الرقم التسلسلي': i[2],
                'الاسم': clean_name,
                'التسلسل العائلي': i[6],
                'تاريخ الميلاد': str(i[7])[:4],
                'رقم السجل المدني': i[8],
                'رقم السجل العام': i[9],
                'رقم الصفحة': i[10],
                'رقم الهوية': i[11],
                'الحالة': i[12],
                'الوظيفة': i[13],
                'تاريخ الإصدار': i[14],
                'الضمان الاجتماعي': i[15],
                'الراتب': i[16],
                'مكان العمل': i[17],
                'اسم الأم': filter_arabic(i[18]),
                'اسم الجدة': filter_arabic(i[19]),
                'نوع الوظيفة': i[20],
                'العلامة': i[21],
                'اسم الفرع': i[22]
            })
        except Exception as e:
            print(e)
    return results

# دالة للبحث في قاعدة بيانات f واسترجاع المعلومات المطلوبة
def search_head_family(db, name):
    first_name, father_name, grand_name = name.split(' ')
    query = f"""
    SELECT RC_NO, FAM_NO, F_DIST, F_AREA, F_STREET, F_HOUSE, FH_FIRST, FH_FATHER, FH_GRAND,
           F_NO_PER, F_NO_INF, FD_AG_NO, FL_AG_NO, ISSUE_DT, TIK_IND, F_CASE, F_JOB,
           PRV_RCNO, CUR_RC_TIK, PRV_FDAGNO, F_NO_JOB, T_SALARY, EGAR, SAKIN, KATHA, NAHIA
    FROM FAMILY
    WHERE FH_FIRST LIKE '{first_name}%' AND FH_FATHER LIKE '{father_name}%' AND FH_GRAND LIKE '{grand_name}%'
    """
    results = []
    for i in db.execute(query):
        try:
            clean_name = f"{filter_arabic(i[6].strip())} {filter_arabic(i[7].strip())} {filter_arabic(i[8].strip())}"
            results.append({
                'رقم الوكيل': i[0],
                'رقم العائلة': i[1],
                'المنطقة': i[2],
                'الحي': i[3],
                'الشارع': i[4],
                'المنزل': i[5],
                'الاسم': clean_name,
                'عدد الأشخاص': i[9],
                'عدد الأطفال': i[10],
                'رقم الوكيل الغذائي الأول': i[11],
                'رقم الوكيل الغذائي الأخير': i[12],
                'تاريخ الإصدار': i[13],
                'مؤشر التذاكر': i[14],
                'حالة الأسرة': i[15],
                'وظيفة الأسرة': i[16],
                'رقم الوكيل السابق': i[17],
                'رقم التذكرة الحالية': i[18],
                'رقم الوكيل الغذائي السابق': i[19],
                'عدد العاطلين': i[20],
                'إجمالي الراتب': i[21],
                'الإيجار': i[22],
                'مكان السكن': i[23],
                'القطاع': i[24],
                'الناحية': i[25]
            })
        except Exception as e:
            print(e)
    return results

# دالة للبحث في قاعدة بيانات w واسترجاع المعلومات المطلوبة
def search_welfare(db, rc_no):
    query = """
    SELECT RC_NO, RC_NAME, RC_PRVCD, RC_PROVINC, RC_CTRCD, RC_CTRNM, RC_CTCD, RC_COUNTY,
           RC_DIST, RC_AREA, RC_STREET, RC_HOUSE, RC_TEL, RC_CHIEF, CH_DISTRKT, CH_AREA,
           CH_STREET, CH_HOUSE, CH_TEL, SUPPMON, ISSUDAT, PRVISSU
    FROM RC
    WHERE RC_NO = ?
    """
    results = []
    for i in db.execute(query, (rc_no,)):
        try:
            results.append({
                'رقم الوكيل': i[0],
                'اسم': filter_arabic(i[1]),
                'رقم المحافظة': i[2],
                'المحافظة': i[3],
                'رمز المركز': i[4],
                'اسم المركز': i[5],
                'رمز المدينة': i[6],
                'المقاطعة': i[7],
                'المنطقة': i[8],
                'الحي': i[9],
                'الشارع': i[10],
                'المنزل': i[11],
                'الهاتف': i[12],
                'الرئيس': i[13],
                'المنطقة الإدارية': i[14],
                'الحي الإداري': i[15],
                'الشارع الإداري': i[16],
                'المنزل الإداري': i[17],
                'الهاتف الإداري': i[18],
                'مساعدة مالية': i[19],
                'تاريخ الإصدار': i[20],
                'تاريخ الإصدار السابق': i[21]
            })
        except Exception as e:
            print(e)
    return results
# دالة التعامل مع البحث برقم العائلة
def handle_search_family_by_number(message):
    fam_no = message.text.strip()
    db = open_db("m")
    results = search_family_by_number(db, fam_no)  # دالة جديدة سنقوم بإنشائها
    send_results(message, results, fam_no)  # أرسل النتائج مع رقم العائلة
    close_db(db)

# دالة للبحث في قاعدة بيانات m باستخدام رقم العائلة
def search_family_by_number(db, fam_no):
    query = f"""
    SELECT RC_NO, FAM_NO, SEQ_NO, P_FIRST, P_FATHER, P_GRAND, P_RELATION, P_BIRTH,
           SS_BR_NO, SS_LG_NO, SS_PG_NO, SS_ID_NO, P_CASE, P_JOB, P_ISUDT, SOC,
           P_SALARY, P_WORK, P_MOTHER, GR_MOTHER, T_JOB, MARK, SS_BR_NM
    FROM person
    WHERE FAM_NO = ?
    """
    results = []
    for i in db.execute(query, (fam_no,)):  # استخدام الرقم العائلي كمعامل
        try:
            clean_name = f"{filter_arabic(i[3].strip())} {filter_arabic(i[4].strip())} {filter_arabic(i[5].strip())}"
            results.append({
                'رقم الوكيل': i[0],
                'رقم العائلة': i[1],
                'الرقم التسلسلي': i[2],
                'الاسم': clean_name,
                'التسلسل العائلي': i[6],
                'تاريخ الميلاد': str(i[7])[:4],
                'رقم السجل المدني': i[8],
                'رقم السجل العام': i[9],
                'رقم الصفحة': i[10],
                'رقم الهوية': i[11],
                'الحالة': i[12],
                'الوظيفة': i[13],
                'تاريخ الإصدار': i[14],
                'الضمان الاجتماعي': i[15],
                'الراتب': i[16],
                'مكان العمل': i[17],
                'اسم الأم': filter_arabic(i[18]),
                'اسم الجدة': filter_arabic(i[19]),
                'نوع الوظيفة': i[20],
                'العلامة': i[21],
                'اسم الفرع': i[22]
            })
        except Exception as e:
            print(e)
    return results
# إرسال المعلومات بطريقة مرتبة
def send_results(message, results, family_number=None):
    if results:
        for res in results:
            response = "\n".join([f"{key}: {value}" for key, value in res.items()])

            # إعداد الزر لعرض جميع أفراد العائلة
            if family_number is not None:
                markup = types.InlineKeyboardMarkup()
                show_family_button = types.InlineKeyboardButton(text="عرض جميع أفراد العائلة", callback_data=f"show_family_{family_number}")
                markup.add(show_family_button)
                bot.send_message(message.chat.id, response, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, response)  # بدون زر
    else:
        bot.send_message(message.chat.id, "لم يتم العثور على نتائج.")

# إعداد البوت
token = os.getenv("BOT_TOKEN")# استبدل هذا برمز التوكن الخاص بك
bot = telebot.TeleBot(token, num_threads=20, skip_pending=True)

# قائمة الأزرار
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="بحث افراد الاسرة", callback_data="search_all_families")
    button2 = types.InlineKeyboardButton(text="بحث باسم رب الاسرة", callback_data="search_head_of_family")
    button3 = types.InlineKeyboardButton(text="ابحث عن منطقة الوكيل", callback_data="search_welfare")
    button4 = types.InlineKeyboardButton(text="بحث برقم العائلة", callback_data="search_family_number")  # الزر الجديد
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, "بوت داتا بيس محافظة الموصل يمكنك البحث عن شخص ومعرفة رب الاسرة ومن ثم البحث عن رقم وكالة المواد الغذائية ورقم المنطقة ", reply_markup=markup)

# التعامل مع اختيار البحث
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "search_all_families":
        bot.send_message(call.message.chat.id, "أرسل الاسم الثلاثي للبحث.")
        bot.register_next_step_handler(call.message, handle_search_family)
    elif call.data == "search_head_of_family":
        bot.send_message(call.message.chat.id, "أرسل الاسم الثلاثي للبحث.")
        bot.register_next_step_handler(call.message, handle_search_head_family)
    elif call.data == "search_welfare":
        bot.send_message(call.message.chat.id, "أرسل رقم الوكيل للبحث.")
        bot.register_next_step_handler(call.message, handle_search_welfare)
    elif call.data == "search_family_number":  # الشرط الجديد
        bot.send_message(call.message.chat.id, "أرسل رقم العائلة للبحث.")
        bot.register_next_step_handler(call.message, handle_search_family_by_number)

# دالة التعامل مع البحث عن أفراد الأسرة
def handle_search_family(message):
    name = filter_arabic(message.text)
    db = open_db("m")
    results = search_family(db, name)
    send_results(message, results)
    close_db(db)

# دالة التعامل مع البحث عن رب الأسرة
def handle_search_head_family(message):
    name = filter_arabic(message.text)
    db = open_db("f")
    results = search_head_family(db, name)
    send_results(message, results)
    close_db(db)

# دالة التعامل مع البحث عن الوكالة
def handle_search_welfare(message):
    rc_no = message.text.strip()
    db = open_db("w")
    results = search_welfare(db, rc_no)
    send_results(message, results)
    close_db(db)

# بدء تشغيل البوت
if __name__ == "__main__":
    bot.polling(none_stop=True)
