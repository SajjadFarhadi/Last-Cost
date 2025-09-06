from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import os
from pyngrok import ngrok

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret'

# --- Translations ---
translations = {
    'en': {
        'app_title': 'Product Cost Calculator',
        'language': 'Language',
        'lang_fa': 'Persian',
        'lang_en': 'English',
        'lang_tr': 'Turkish',
        'logout': 'Logout',
        'enter_params': 'Choose Desirable Parameters',
        'part_name': 'Part Name',
        'material': 'Material',
        'customer': 'Customer',
        'calculate': 'Calculate',
        'select': 'Select',
        'login': 'Login',
        'username': 'Username',
        'password': 'Password',
        'calc_result': 'Calculation Result',
        'total_cost': 'Total Cost',
        'data_table': 'Data Table',
        'no_matching_data': 'No matching data found!',
        'invalid_credentials': 'Invalid credentials',
        'cost': 'Cost',
        'company_name': 'BAHAYAR',
        'app_subtitle': 'Web application of calculating the final cost of products (BAHAYAR)',
        'services': 'Services',
        'services_text': 'We provide innovative solutions for mechanical parts cost calculation, including accurate material and customer-based pricing analysis.',
        'about': 'About',
        'about_text': 'Our company is committed to delivering reliable, user-friendly, and modern software tools that help businesses optimize costs efficiently.',
        'contact': 'Contact',
        'contact_text': 'Email: fidar.fanavar.hermes@gmail.com | Phone: +98 914 419 9484',
        'enter_system': 'Enter System',
        'video_not_supported': 'Your browser does not support the video tag.',
        'buyer_welcome': 'Welcome to Your Last Cost Calculator',
        'buyer_company_name': 'Azar Hydraulic Gharb (AHG)',
        'buyer_description': 'Azar Hydraulic Gharb (AHG) is the largest manufacturer of hydraulic fittings in the northwest of the country, producing over 400 types of hydraulic fittings.',
        'buyer_intro_text': 'As our valued buyer, this tool is customized for your needs. Select parameters to calculate precise costs for your parts.',
        'start_calculating': 'Start Calculating',
        'exclusive_image1_caption': 'High-quality hydraulic fittings production line',
        'exclusive_image2_caption': 'Advanced manufacturing facility',
        'exclusive_image3_caption': 'Diverse range of hydraulic products',
        'products_stat': 'Products',
        'years_stat': 'Years in Business',
        'buyer_contact_text': 'Phone: +98 914 361 1140 | Address: Iran, Tabriz, Automotive Technology Industrial Park, Third Street'
    },
    'fa': {
        'app_title': 'محاسبه گر هزینه محصولات',
        'language': 'زبان',
        'lang_fa': 'فارسی',
        'lang_en': 'انگلیسی',
        'lang_tr': 'ترکی',
        'logout': 'خروج',
        'enter_params': 'پارامترهای مورد نظر را انتخاب کنید',
        'part_name': 'نام قطعه',
        'material': 'مواد',
        'customer': 'مشتری',
        'calculate': 'محاسبه',
        'select': 'انتخاب',
        'login': 'ورود',
        'username': 'نام کاربری',
        'password': 'رمز عبور',
        'calc_result': 'نتیجه محاسبه',
        'total_cost': 'هزینه کل',
        'data_table': 'جدول داده',
        'no_matching_data': 'هیچ داده منطبقی یافت نشد!',
        'invalid_credentials': 'اعتبارنامه نامعتبر',
        'cost': 'هزینه',
        'company_name': 'بهایار',
        'app_subtitle': 'نرم‌افزار تحت وب برای محاسبه هزینه نهایی محصولات (بهایار)',
        'services': 'خدمات',
        'services_text': 'ما راه‌حل‌های نوآورانه‌ای برای محاسبه هزینه قطعات مکانیکی ارائه می‌دهیم، شامل تحلیل دقیق قیمت‌گذاری براساس مواد و مشتری.',
        'about': 'درباره ما',
        'about_text': 'شرکت ما متعهد به ارائه ابزارهای نرم‌افزاری قابل اعتماد، کاربرپسند و مدرن برای کمک به بهینه‌سازی هزینه‌هاست.',
        'contact': 'تماس',
        'contact_text': 'ایمیل: fidar.fanavar.hermes@gmail.com | +تلفن: 98 914 419 9484',
        'enter_system': 'ورود به سیستم',
        'video_not_supported': 'مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.',
        'buyer_welcome': 'به محاسبه‌گر هزینه محصولات خود خوش آمدید',
        'buyer_company_name': 'آذر هیدرولیک غرب (AHG)',
        'buyer_description': 'آذر هیدرولیک غرب (AHG) بزرگترین تولید کننده اتصالات هیدرولیک در شمال غرب کشور است که بیش از 400 نوع اتصالات هیدرولیک تولید می کند.',
        'buyer_intro_text': 'به عنوان خریدار ارزشمند ما، این ابزار برای نیازهای شما سفارشی شده است. پارامترها را انتخاب کنید تا هزینه دقیق قطعات خود را محاسبه کنید.',
        'start_calculating': 'شروع محاسبه',
        'exclusive_image1_caption': 'خط تولید اتصالات هیدرولیک با کیفیت بالا',
        'exclusive_image2_caption': 'تاسیسات تولیدی پیشرفته',
        'exclusive_image3_caption': 'طیف متنوعی از محصولات هیدرولیک',
        'products_stat': 'محصولات',
        'years_stat': 'سال فعالیت',
        'buyer_contact_text': '| تلفن:98 914 361 1140+| آدرس:ایران، تبریز، شهرک صنعتی فناوری خودرو، خیابان سوم'
    },
    'tr': {
        'app_title': 'Ürünler Maliyet Hesaplayıcı',
        'language': 'Dil',
        'lang_fa': 'Farsça',
        'lang_en': 'İngilizce',
        'lang_tr': 'Türkçe',
        'logout': 'Çıkış Yap',
        'enter_params': 'İstediğiniz parametreleri seçin',
        'part_name': 'Parça Adı',
        'material': 'Malzeme',
        'customer': 'Müşteri',
        'calculate': 'Hesapla',
        'select': 'Seç',
        'login': 'Giriş',
        'username': 'Kullanıcı Adı',
        'password': 'Şifre',
        'calc_result': 'Hesaplama Sonucu',
        'total_cost': 'Toplam Maliyet',
        'data_table': 'Veri Tablosu',
        'no_matching_data': 'Eşleşen veri bulunamadı!',
        'invalid_credentials': 'Geçersiz kimlik bilgileri',
        'cost': 'Maliyet',
        'company_name': 'BAHAYAR',
        'app_subtitle': 'Ürünlerin nihai maliyetini hesaplamak için web uygulaması (BAHAYAR)',
        'services': 'Hizmetler',
        'services_text': 'Mekanik parça maliyeti hesaplamasında yenilikçi çözümler sunuyoruz.',
        'about': 'Hakkımızda',
        'about_text': 'Şirketimiz güvenilir, kullanıcı dostu ve modern yazılım araçları sunmayı taahhüt eder.',
        'contact': 'İletişim',
        'contact_text': 'E-posta: fidar.fanavar.hermes@gmail.com | Telefon: +98 914 419 9484',
        'enter_system': 'Sisteme Giriş',
        'video_not_supported': 'Tarayıcınız video etiketini desteklemiyor.',
        'buyer_welcome': 'Maliyet Hesaplayıcınıza Hoş Geldiniz',
        'buyer_company_name': 'Azar Hydraulic Gharb (AHG)',
        'buyer_description': 'Azar Hydraulic Gharb (AHG), ülkenin kuzeybatısındaki en büyük hidrolik bağlantı parçaları üreticisidir ve 400\'den fazla hidrolik bağlantı parçası türü üretmektedir.',
        'buyer_intro_text': 'Değerli alıcımız olarak, bu araç ihtiyaçlarınıza göre özelleştirilmiştir. Parçalarınız için hassas maliyetleri hesaplamak için parametreleri seçin.',
        'start_calculating': 'Hesaplamaya Başla',
        'exclusive_image1_caption': 'Yüksek kaliteli hidrolik bağlantı parçaları üretim hattı',
        'exclusive_image2_caption': 'Gelişmiş üretim tesisi',
        'exclusive_image3_caption': 'Hidrolik ürünlerin çeşitli yelpazesi',
        'products_stat': 'Ürünler',
        'years_stat': 'İş Yılı',
        'buyer_contact_text': '| Telefon: +98 914 361 1140| Adres: İran, Tebriz, Otomotiv Teknolojisi Endüstri Parkı, Üçüncü Cadde'
    }
}

SUPPORTED_LOCALES = ['fa', 'en', 'tr']


def get_locale():
    return session.get('lang', 'fa')

def t(key):
    lang = get_locale()
    return translations.get(lang, translations['en']).get(key, key)

@app.context_processor
def inject_trans():
    return dict(t=t, get_lang=get_locale)

@app.route('/set_language', methods=['POST'])
def set_language():
    lang = request.form.get('lang')
    if lang:
        session['lang'] = lang
    return redirect(request.referrer or url_for('company_intro'))

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

USERS = {
    "AHG": {"password": "pass123"},
    "companyB": {"password": "pass456"}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

@app.route("/")
def company_intro():
    return render_template("company_intro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username]["password"] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for("buyer_intro"))
        else:
            flash(t('invalid_credentials'), "danger")
    return render_template("login.html")

@app.route("/buyer_intro")
@login_required
def buyer_intro():
    return render_template("buyer_intro.html")

@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    excel_path = os.path.join("data", "parts_data.xlsx")
    try:
        df_parts = pd.read_excel(excel_path, sheet_name="Parts")
        df_materials = pd.read_excel(excel_path, sheet_name="Materials")
        df_customers = pd.read_excel(excel_path, sheet_name="Customers")
        df_costs = pd.read_excel(excel_path, sheet_name="Costs")
    except FileNotFoundError:
        flash("Data file not found. Please check the 'data' directory.", "danger")
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Error loading data: {str(e)}", "danger")
        return redirect(url_for("index"))

    part_names = df_parts["PartName"].dropna().unique().tolist()
    materials = df_materials["MaterialName"].dropna().unique().tolist()
    customers = df_customers["CustomerName"].dropna().unique().tolist()

    if request.method == "POST":
        part_name = request.form.get("part_name")
        material = request.form.get("material")
        customer = request.form.get("customer")

        part_id = df_parts[df_parts["PartName"] == part_name]["PartID"].values
        material_id = df_materials[df_materials["MaterialName"] == material]["MaterialID"].values
        customer_id = df_customers[df_customers["CustomerName"] == customer]["CustomerID"].values

        if len(part_id) == 0 or len(material_id) == 0 or len(customer_id) == 0:
            flash(t('no_matching_data'), "danger")
            return redirect(url_for("index"))

        part_id = part_id[0]
        material_id = material_id[0]
        customer_id = customer_id[0]

        filtered = df_costs[
            (df_costs["PartID"] == part_id) &
            (df_costs["MaterialID"] == material_id) &
            (df_costs["CustomerID"] == customer_id)
        ]

        if filtered.empty:
            flash(t('no_matching_data'), "danger")
            return redirect(url_for("index"))

        total_cost = filtered["Cost"].values[0]

        table_df = pd.DataFrame({
            t('part_name'): [part_name],
            t('material'): [material],
            t('customer'): [customer],
            t('cost'): [total_cost]
        })

        return render_template("result.html",
                               part_name=part_name,
                               material=material,
                               customer=customer,
                               total_cost=total_cost,
                               table=table_df.to_html(classes="table table-bordered", index=False))

    return render_template("index.html", part_names=part_names, materials=materials, customers=customers)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)