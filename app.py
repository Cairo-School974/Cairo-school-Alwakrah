import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# المجلد الأساسي للشهادات
CERT_FOLDER = os.path.join(os.getcwd(), 'certificates')

# المجلد الأساسي لجداول الحصص (التحديث الجديد)
SCHEDULE_FOLDER = os.path.join(os.getcwd(), 'schedules')

# 1. الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# 2. صفحة الأنشطة
@app.route("/activities")
def activities():
    return render_template("activities.html")

# 3. صفحة اختيار جدول الحصص
@app.route("/schedule_select")
def schedule_select():
    return render_template("schedule_select.html")

# 3. مكرر/محدث: صفحة عرض جدول الحصص وسحب ملف الـ PDF تلقائياً
@app.route("/display_schedule", methods=["GET", "POST"])
def display_schedule():
    pdf_filename = None
    error_message = None

    if request.method == "POST":
        section = request.form.get("section") # القسم
        grade = request.form.get("grade")     # الفصل
        
        # بنبني اسم الملف بناءً على اسم الفصل (مثلاً صف 1-1.pdf)
        filename = f"{grade}.pdf"
        file_path = os.path.join(SCHEDULE_FOLDER, section, filename)

        if os.path.exists(file_path):
            pdf_filename = f"{section}/{filename}"
        else:
            error_message = f"عذراً، لا يوجد جدول متاح حالياً للفصل {grade} في القسم {section}."

    return render_template("display_schedule.html", pdf_filename=pdf_filename, error_message=error_message)

# 4. صفحة الشهادات (النسخة الكاملة للبحث والاستخراج)
@app.route("/certificate", methods=["GET", "POST"])
def certificate():
    pdf_filename = None
    error_message = None

    if request.method == "POST":
        student_id = request.form.get("national_id")
        cert_type = request.form.get("cert_type")
        
        filename = f"{student_id}.pdf"
        file_path = os.path.join(CERT_FOLDER, cert_type, filename)

        if os.path.exists(file_path):
            pdf_filename = f"{cert_type}/{filename}"
        else:
            error_message = "رقم الـ ID مدخل خطأ أو الشهادة غير متاحة حتى الآن. يرجى مراجعة إدارة المدرسة."

    return render_template("certificate.html", pdf_filename=pdf_filename, error_message=error_message)

# 5. مسار لعرض ملفات الـ PDF للشهادات
@app.route('/certificates/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(CERT_FOLDER, filename)

# 5. (مكرر/محدث) مسار لعرض ملفات الـ PDF لجداول الحصص
@app.route('/schedules/<path:filename>')
def serve_schedule(filename):
    return send_from_directory(SCHEDULE_FOLDER, filename)

# 6. صفحة اتصل بنا
@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)