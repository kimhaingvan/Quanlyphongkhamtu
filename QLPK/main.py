from flask import render_template

from QLPK import app, admin, dao, login
from QLPK.models import *
from QLPK.views.BenhNhanView import BenhNhanView
from QLPK.views.ChiDanView import ChiDanView
from QLPK.views.ChiTietHoaDonView import ChiTietHoaDonView
from QLPK.views.DonViView import DonViView
from QLPK.views.HoaDonView import HoaDonView
from QLPK.views.LoaiBenhView import LoaiBenhView
from QLPK.views.PhieuKhamBenhView import PhieuKhamBenhView
from QLPK.views.QuyDinhView import QuyDinhView
from QLPK.views.ThuocView import ThuocView
from QLPK.views.addViewLogout import LogoutView
from QLPK.views.addViewRegister import RegisterView

admin.add_view(PhieuKhamBenhView(Phieukhambenh, db.session, name="Phiếu khám bệnh"))
admin.add_view(BenhNhanView(Benhnhan, db.session, name="Bệnh nhân"))
admin.add_view(LoaiBenhView(Loaibenh, db.session, name="Loại bệnh"))
admin.add_view(ChiTietHoaDonView(Chitiethoadon, db.session, name="Chi tiết hóa đơn"))
admin.add_view(HoaDonView(Hoadon, db.session, name="Hóa đơn"))
admin.add_view(ThuocView(Thuoc, db.session, name="Thuốc"))
admin.add_view(DonViView(Donvi, db.session, name="Đơn vị"))
admin.add_view(ChiDanView(Chidan, db.session, name="Chỉ dẫn"))
admin.add_view(QuyDinhView(Quydinh, db.session, name="Quy định"))
admin.add_view(RegisterView(name="Đăng ký"))
admin.add_view(LogoutView(name="Đăng xuất"))


@app.route('/login-admin', methods=['post', 'get'])
def login_admin():
    user_login = dao.LoginUser()
    return user_login


@app.route('/register-admin', methods=['post', 'get'])
def sign_up():
    user_sign_up = dao.SignUpUser()
    return user_sign_up


@login.user_loader
def User_load(user_id):
    return Users.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def Index():
    return render_template('clients/base.html')


@app.route('/pricing', methods=['GET', 'POST'])
def Pricing():
    return render_template('clients/pricing.html')


@app.route('/doctor', methods=['GET', 'POST'])
def Doctor():
    return render_template('clients/doctor.html')


if __name__ == "__main__":
    app.run(debug=True)
