import hashlib
import hmac
import json
import urllib
import uuid
from calendar import monthrange
from datetime import datetime

from flask import request, redirect, flash, url_for, jsonify, session
from flask_login import login_user
from sqlalchemy import or_, func

from QLPK import db
from QLPK.models import Users, Code, Quydinh, Bacsi, Khoa, GopY, Phieukhambenh, Loaibenh, Thuoc, Donvi, Chidan, Hoadon, \
    Chitiethoadon, Chucvu

import smtplib

def LoginUser():
    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = Users.query.filter(Users.user_name == user_name.strip(), Users.password == password).first()
        if user:
            login_user(user=user)
        else:
            flash('Đăng nhập không thành công')
    return redirect("/admin")

def DangKy():
    if request.method == "POST":
        user_name = request.form.get("username")
        name = request.form.get("name")
        usercode = request.form.get("code")
        password = request.form.get("password", "")
        confirmpassword = request.form.get("confirmpassword", "")
        email = request.form.get("email")
        chuc_vu_id = request.form.get("chuc_vu_id")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        confirmpassword = str(hashlib.md5(confirmpassword.strip().encode("utf-8")).hexdigest())
        if password != confirmpassword:
            flash('Password not same.')
            return redirect(url_for('registerview.index'))
        user_code = Code.query.filter(Code.code_id == usercode, Code.is_active == 1).first()
        if not user_code:
            flash('Your code is wrong.')
            return redirect(url_for('registerview.index'))
        user = Users.query.filter(Users.email == email).first()
        if user:
            flash('Email address already exist.')
            return redirect(url_for('registerview.index'))
        new_user = Users(name=name, user_name=user_name, email=email, password=password, is_active=1, code_id=usercode, chuc_vu_id=chuc_vu_id)
        update_code = Code.query.get(usercode)
        update_code.is_active = 0
        db.session.add(new_user, update_code)
        db.session.commit()
    return redirect(url_for('login_admin'))


def LayCacQuyDinh():
    return Quydinh.query.first()

def SoLuongQuyDinh():
    return len(Quydinh.query.all())

def SoLuongPhieuKhamBenhTrongNgay():
    return len(Phieukhambenh.query.filter(Phieukhambenh.phieu_kham_benh_id, func.DATE(Phieukhambenh.ngay_kham) == datetime.utcnow().date()).all())

def SoLuongLoaiBenh():
    return len(Loaibenh.query.all())

def SoLuongLoaiThuoc():
    return len(Thuoc.query.all())

def SoLuongDonVi():
    return len(Donvi.query.all())

def SoLuongCachDung():
    return len(Chidan.query.all())

def LayTatCaBacSi():
    return Bacsi.query.all()

def LayTatCaKhoa():
    return Khoa.query.all()

def LayChiTietBacSiTheoId(bac_si_id):
    return Bacsi.query.get(bac_si_id)

def LayCacPhieuKhamBenh():
    return Phieukhambenh.query.all()

def LayCacLoaiThuoc():
    return Thuoc.query.all()

def LayCacChiDan():
    return Chidan.query.all()

def LayCacDonVi():
    return Donvi.query.all()

def LayCacPhieuKhamBenh():
    return Phieukhambenh.query.all()

def LaySoNgayTrongMotThang(nam, thang):
    return monthrange(nam, thang)[1]

def TinhTongSoBenhNhanTrongNgay(datetime):
    return len(Phieukhambenh.query.filter(Phieukhambenh.phieu_kham_benh_id, func.DATE(Phieukhambenh.ngay_kham) == datetime).all())

def TinhDoanhThuTrongNgay(datetime)-> float:
    cac_hoa_don = Hoadon.query.filter(Hoadon.hoa_don_id, func.DATE(Hoadon.ngay_thanh_toan) == datetime).all()
    doanh_thu_trong_ngay = 0
    for hoa_don in cac_hoa_don:
        doanh_thu_trong_ngay += hoa_don.tong_tien
    return doanh_thu_trong_ngay

def TinhTongTienTheoThang(thang, nam) -> float:
    tong_doanh_thu = 0.0
    for ngay in range(1, LaySoNgayTrongMotThang(nam, thang) + 1):
        date = datetime(nam, thang, ngay)
        print(TinhDoanhThuTrongNgay(date))
        doanh_thu_trong_ngay = TinhDoanhThuTrongNgay(date)
        tong_doanh_thu = tong_doanh_thu + doanh_thu_trong_ngay

    return tong_doanh_thu

def BaoCaoDoanhThuTheoThang(thang:int, nam:int):
    bao_cao_theo_thang = []
    tong_doanh_thu_theo_thang = TinhTongTienTheoThang(thang, nam)
    for ngay in range(1, LaySoNgayTrongMotThang(nam, thang) + 1):
        date = datetime(nam, thang, ngay)
        doanh_thu_theo_ngay = TinhDoanhThuTrongNgay(date)
        so_benh_nhan_trong_ngay = TinhTongSoBenhNhanTrongNgay(date)
        if doanh_thu_theo_ngay > 0:
            ti_le_doanh_thu = (doanh_thu_theo_ngay / tong_doanh_thu_theo_thang) * 100.0
        else:
            ti_le_doanh_thu = 0.0
        bao_cao_theo_ngay = {
            'ngay': str(ngay) + '/' + str(thang) + '/' + str(nam),
            'so_benh_nhan': so_benh_nhan_trong_ngay,
            'doanh_thu': doanh_thu_theo_ngay,
            'ti_le': ti_le_doanh_thu
        }
        bao_cao_theo_thang.append(bao_cao_theo_ngay)
    return jsonify(bao_cao_theo_thang)

def BaoCaoSuDungThuoc(thang, nam):
    pass

def LayCacBacSiTheoKeyword(ho_ten, ma_khoa):
    danh_sach_bac_si_tim_kiem = Bacsi.query.filter(or_(Bacsi.ho_ten.contains(ho_ten), Bacsi.khoa_id==ma_khoa
                                                      )).all()
    return danh_sach_bac_si_tim_kiem

def TaoThuGopY(ten_nguoi_gui, email_nguoi_gui, tieu_de, noi_dung):
    thu_gop_y = GopY(ten_nguoi_gui= ten_nguoi_gui,email_nguoi_gui=email_nguoi_gui,tieu_de=tieu_de,noi_dung=noi_dung)
    db.session.add(thu_gop_y)
    db.session.commit()

def ThanhToan(ma_phieu_kham_benh, tien_kham, tong_tien, cac_chi_tiet_hoa_don, nguoi_dung_id):
    hoa_don = Hoadon(phieu_kham_benh_id = ma_phieu_kham_benh,tien_kham=tien_kham, tong_tien= tong_tien, nguoi_dung_id= nguoi_dung_id, ngay_thanh_toan=datetime.now())
    db.session.add(hoa_don)
    db.session.flush()

    for chi_tiet_hoa_don in cac_chi_tiet_hoa_don:
        chi_tiet_hoa_don_model= Chitiethoadon(hoa_don_id=int(hoa_don.hoa_don_id), thuoc_id=chi_tiet_hoa_don['thuoc_id'], chi_dan_id=chi_tiet_hoa_don['chi_dan_id'], don_vi_id=chi_tiet_hoa_don['don_vi_id'], so_luong= chi_tiet_hoa_don['so_luong'])
        # hoa_don.ds_chi_tiet_hoa_don.append(chi_tiet_hoa_don_model)
        db.session.add(chi_tiet_hoa_don_model)
        db.session.commit()
    db.session.commit()
    return jsonify({'thanh_cong': True})

def thanh_toan_momo(tong_tien):
    endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOY1ZA20200907" #busssiness momo
    accessKey = "rVuWIV2U6YHmb803"#busssiness momo
    serectkey = "EQeEkD4sirbclirmqPv5qXDrcLu2h5EZ"#busssiness momo
    orderInfo = "pay with MoMo" #hieenj lên thông tin info
    returnUrl = "http://127.0.0.1:5500/admin/hoadon" # redicrect sau đi hoàn tất thanh toán
    notifyurl = "http://127.0.0.1:5500/contact"
    amount = tong_tien #Số tiền của hóa đơn
    orderId = str(uuid.uuid4()) # order id của momo chứ ko phải của chúng ta
    requestId = str(uuid.uuid4()) # như trên
    requestType = "captureMoMoWallet" 
    extraData = "merchantName=;merchantId="

    rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + str(amount) + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData


    h = hmac.new(serectkey.encode('utf-8'), rawSignature.encode('utf-8'), hashlib.sha256)
    signature = h.hexdigest()


    data = {
        'partnerCode': partnerCode,
        'accessKey': accessKey,
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'returnUrl': returnUrl,
        'notifyUrl': notifyurl,
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }

    data = json.dumps(data)

    clen = len(data)
    req = urllib.request.Request(endpoint,data.encode('utf-8'),
        {'Content-Type': 'application/json', 'Content-Length': clen}
    )
    f = urllib.request.urlopen(req)

    response = f.read()
    f.close()

    return json.loads(response)

def LayTatCaChucVu():
    return Chucvu.query.all()
