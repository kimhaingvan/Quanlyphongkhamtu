from flask import render_template, redirect, url_for, request
from livereload import Server

from QLPK import app, admin, dao, login, smtp
from QLPK.models import *
from QLPK.views.BacSiView import BacSiView
from QLPK.views.BenhNhanView import BenhNhanView
from QLPK.views.ChiDanView import ChiDanView
from QLPK.views.ChiTietHoaDonView import ChiTietHoaDonView
from QLPK.views.DonViView import DonViView
from QLPK.views.GopYView import GopYView
from QLPK.views.HoaDonView import HoaDonView
from QLPK.views.KhoaView import KhoaView
from QLPK.views.LoaiBenhView import LoaiBenhView
from QLPK.views.PhieuKhamBenhView import PhieuKhamBenhView
from QLPK.views.QuyDinhView import QuyDinhView
from QLPK.views.ThuocView import ThuocView
from QLPK.views.addViewLogout import LogoutView
from QLPK.views.addViewRegister import RegisterView
import smtplib
admin.add_view(PhieuKhamBenhView(Phieukhambenh, db.session, name="Phiếu khám bệnh"))
admin.add_view(BenhNhanView(Benhnhan, db.session, name="Bệnh nhân"))
admin.add_view(LoaiBenhView(Loaibenh, db.session, name="Loại bệnh"))
admin.add_view(ChiTietHoaDonView(Chitiethoadon, db.session, name="Chi tiết hóa đơn"))
admin.add_view(HoaDonView(Hoadon, db.session, name="Hóa đơn"))
admin.add_view(ThuocView(Thuoc, db.session, name="Thuốc"))
admin.add_view(DonViView(Donvi, db.session, name="Đơn vị"))
admin.add_view(ChiDanView(Chidan, db.session, name="Chỉ dẫn"))
admin.add_view(QuyDinhView(Quydinh, db.session, name="Quy định"))
admin.add_view(BacSiView(Bacsi, db.session, name="Bác sĩ"))
admin.add_view(KhoaView(Khoa, db.session, name="Khoa"))
admin.add_view(GopYView(GopY, db.session, name="Góp ý"))
admin.add_view(RegisterView(name="Đăng ký"))
admin.add_view(LogoutView(name="Đăng xuất"))

from email.message import EmailMessage

@app.route('/login-admin', methods=['post', 'get'])
def login_admin():
    user_login = dao.LoginUser()
    return user_login


@app.route('/register-admin', methods=['post', 'get'])
def DangKy():
    user_sign_up = dao.DangKy()
    return user_sign_up


@login.user_loader
def User_load(user_id):
    return Users.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def Index():
    return render_template('clients/base.html')


@app.route('/about', methods=['GET', 'POST'])
def About():
    return render_template('clients/about.html')

@app.route('/appointment', methods=['GET', 'POST'])
def Appointment():
    return render_template('clients/appointment.html')

@app.route('/blog', methods=['GET', 'POST'])
def Blog():
    return render_template('clients/blog.html')

@app.route('/blog-single', methods=['GET', 'POST'])
def BlogSingle():
    return render_template('clients/blog-single.html')

@app.route('/contact', methods=['GET', 'POST'])
def Contact():
    return render_template('clients/contact.html')

@app.route('/department', methods=['GET', 'POST'])
def Department():
    return render_template('clients/department.html')

@app.route('/pricing', methods=['GET', 'POST'])
def Pricing():
    return render_template('clients/pricing.html')

@app.route('/tim-kiem-bac-si', methods=['GET', 'POST'])
def TimKiemBacSi():
    ho_ten = request.form['ho_ten']
    ma_khoa = request.form['ten_khoa']
    danh_sach_bac_si_tim_kiem = dao.LayCacBacSiTheoKeyword(ho_ten, ma_khoa)
    ds_khoa =  dao.LayTatCaKhoa()
    return render_template('clients/doctor.html', tat_ca_bac_si = danh_sach_bac_si_tim_kiem, tat_ca_khoa= ds_khoa)

@app.route('/gui-thu-gop-y', methods=['GET', 'POST'])
def GuiThuGopY():
    ten_nguoi_gui = request.form['ten_nguoi_gui']
    email_nguoi_gui = request.form['email_nguoi_gui']
    tieu_de = request.form['tieu_de']
    noi_dung = request.form['noi_dung']
    dao.TaoThuGopY(ten_nguoi_gui, email_nguoi_gui, tieu_de, noi_dung)
    smtp.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    msg = EmailMessage()
    msg['Subject'] = 'Thông báo'
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = email_nguoi_gui
    msg.set_content(
        f'''    Gửi {email_nguoi_gui},
        Thư góp ý của bạn đã được gửi thành công.
        Xin chân thành cảm ơn bạn đã góp ý.
    ''')
    smtp.send_message(msg)
    return redirect(url_for('Pricing'))

@app.route('/doctor', methods=['GET', 'POST'])
def Doctor():
    ds_bac_si = dao.LayTatCaBacSi()
    ds_khoa =  dao.LayTatCaKhoa()
    return render_template('clients/doctor.html', tat_ca_bac_si = ds_bac_si, tat_ca_khoa= ds_khoa)

@app.route('/detail-doctor/<int:id>', methods=['GET', 'POST'])
def XemChiTietBS(id):
    chi_tiet_bac_si = dao.LayChiTietBacSiTheoId(id)
    return render_template('clients/detail-doctor.html', chi_tiet_bac_si=chi_tiet_bac_si)

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve()
    app.run(debug=True)
