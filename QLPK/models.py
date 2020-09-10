from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

from QLPK import db, util


class Phieukhambenh(db.Model):
    phieu_kham_benh_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ngay_kham = db.Column(db.DateTime, nullable=False)
    trieu_chung = db.Column(db.String(1500))
    benh_nhan_id = db.Column(db.Integer, db.ForeignKey('benhnhan.benh_nhan_id'))
    loai_benh_id = db.Column(db.Integer, db.ForeignKey('loaibenh.loai_benh_id'))
    loai_benh_du_doan_id = db.Column(db.String(1500))
    hoa_don = db.relationship('Hoadon', backref='phieu_kham_benh', lazy=True)

    def __str__(self):
        return str(self.phieu_kham_benh_id)

    def serialize(self):
        return {
            'phieu_kham_benh_id': self.phieu_kham_benh_id,
            'ngay_kham': self.ngay_kham,
            'trieu_chung': self.trieu_chung,
            'benh_nhan_id': self.benh_nhan_id,
            'loai_benh_id': self.loai_benh_id,
            'loai_benh_du_doan_id': self.loai_benh_du_doan_id
        }


class Chitiethoadon(db.Model):
    hoa_don_id = db.Column(db.Integer, db.ForeignKey('hoadon.hoa_don_id'), primary_key=True)
    thuoc_id = db.Column(db.Integer, db.ForeignKey('thuoc.thuoc_id'), primary_key=True)
    don_vi_id = db.Column(db.Integer, db.ForeignKey('donvi.don_vi_id'), primary_key=True)
    chi_dan_id = db.Column(db.Integer, db.ForeignKey('chidan.chi_dan_id'), primary_key=True)
    so_luong = db.Column(db.Integer)

    def __str__(self):
        return str(self.hoa_don_id) + '-' + str(self.so_luong)

    def serialize(self):
        return {
            'hoa_don_id': self.hoa_don_id,
            'thuoc_id': self.thuoc_id,
            'don_vi_id': self.don_vi_id,
            'chi_dan_id': self.chi_dan_id,
            'so_luong': self.so_luong,
        }


class Benhnhan(db.Model):
    benh_nhan_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ho_ten = db.Column(db.String(200))
    gioi_tinh = db.Column(db.Boolean)
    nam_sinh = db.Column(db.DateTime)
    dia_chi = db.Column(db.String(500))
    ds_phieu_kham_benh = db.relationship('Phieukhambenh', backref='benh_nhan', lazy=True)

    def __str__(self):
        return str(self.benh_nhan_id) + '-' + self.ho_ten + '-' + self.dia_chi

    def serialize(self):
        return {
            'benh_nhan_id': self.benh_nhan_id,
            'ho_ten': self.ho_ten,
            'gioi_tinh': self.gioi_tinh,
            'nam_sinh': self.nam_sinh,
            'dia_chi': self.dia_chi,
        }


class Hoadon(db.Model):
    hoa_don_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    phieu_kham_benh_id = db.Column(db.Integer, db.ForeignKey('phieukhambenh.phieu_kham_benh_id'))
    tien_kham = db.Column(db.Float, nullable=True)
    ngay_thanh_toan = db.Column(db.DateTime)
    tong_tien = db.Column(db.Float)
    ds_chi_tiet_hoa_don = db.relationship('Chitiethoadon', backref='hoa_don', lazy=True)

    def __str__(self):
        return str(self.hoa_don_id)

    def serialize(self):
        return {
            'hoa_don_id': self.hoa_don_id,
            'phieu_kham_benh_id': self.phieu_kham_benh_id,
            'tien_kham': self.tien_kham,
            'ngay_thanh_toan': self.ngay_thanh_toan,
            'tong_tien': self.tong_tien,
        }


class Thuoc(db.Model):
    thuoc_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ten_thuoc = db.Column(db.String(300))
    don_gia = db.Column(db.Float)
    ds_chi_tiet_hoa_don = db.relationship('Chitiethoadon', backref='thuoc', lazy=True)

    def __str__(self):
        return str(self.thuoc_id) + '-' + self.ten_thuoc + '-' + str(self.don_gia)

    def serialize(self):
        return {
            'thuoc_id': self.hoa_don_id,
            'ten_thuoc': self.phieu_kham_benh_id,
            'don_gia': self.tien_kham
        }


class Donvi(db.Model):
    don_vi_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ten_don_vi = db.Column(db.String(300))
    ds_chi_tiet_hoa_don = db.relationship('Chitiethoadon', backref='don_vi', lazy=True)

    def __str__(self):
        return str(self.don_vi_id) + '-' + self.ten_don_vi

    def serialize(self):
        return {
            'thuoc_id': self.thuoc_id,
            'ten_thuoc': self.ten_thuoc,
            'don_gia': self.don_gia
        }

class Bacsi(db.Model):
    bac_si_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ho_ten = db.Column(db.String(200))
    gioi_tinh = db.Column(db.Boolean)
    nam_sinh = db.Column(db.DateTime)
    mieu_ta = db.Column(db.String(200))
    khoa_id =  db.Column(db.Integer, db.ForeignKey('khoa.khoa_id'))


    def save(self, *args, **kwargs):
        print('whatever I want to do myself is here')
        return super(Bacsi, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.bac_si_id) + '-' + self.ho_ten

    def serialize(self):
        return {
            'bac_si_id': self.bac_si_id,
            'ho_ten': self.ho_ten,
            'nam_sinh': self.nam_sinh,
            'mieu_ta': self.mieu_ta,
            'khoa': self.khoa.serialize(),
        }

class Khoa(db.Model):
    khoa_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ten_khoa = db.Column(db.String(200))
    mieu_ta = db.Column(db.String(2000))
    ds_bac_si = db.relationship('Bacsi', backref='khoa', lazy=True)

    def __str__(self):
        return str(self.khoa_id) + '-' + self.ten_khoa

    def serialize(self):
        return {
            'ten_khoa': self.ten_khoa,
            'mieu_ta': self.mieu_ta,
            'ds_bac_si': util.ConvertModelListToDictList(self.ds_bac_si),
        }

class Chidan(db.Model):
    chi_dan_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    noi_dung = db.Column(db.String(1500))
    ds_chi_tiet_hoa_don = db.relationship('Chitiethoadon', backref='chi_dan', lazy=True)

    def __str__(self):
        return str(self.chi_dan_id) + '-' + self.noi_dung

    def serialize(self):
        return {
            'chi_dan_id': self.chi_dan_id,
            'noi_dung': self.noi_dung
        }


class Loaibenh(db.Model):
    loai_benh_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ten_loai_benh = db.Column(db.String(300))
    trieu_chung = db.Column(db.String(300))
    ds_phieu_kham_benh = db.relationship('Phieukhambenh', backref='loai_benh', lazy=True)

    def __str__(self):
        return str(self.loai_benh_id) + '-' + self.ten_loai_benh

    def serialize(self):
        return {
            'loai_benh_id': self.loai_benh_id,
            'ten_loai_benh': self.ten_loai_benh,
            'trieu_chung': self.trieu_chung
        }


class Code(db.Model):
    code_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_active = db.Column(db.Boolean)
    users = db.relationship('Users', backref='code', lazy=True)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_id = db.Column(db.Integer, db.ForeignKey(Code.code_id), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'code_id': self.code_id,
            'name': self.name,
            'is_active': self.is_active,
            'user_name': self.user_name,
            'password': self.password,
            'email': self.email
        }


class Quydinh(db.Model):
    qui_dinh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    so_luong_benh_nhan_kham_trong_ngay = db.Column(db.Integer)
    so_luong_loai_benh_toi_da = db.Column(db.Integer)
    so_luong_thuoc_toi_da = db.Column(db.Integer)
    so_luong_don_vi_tinh_toi_da = db.Column(db.Integer)
    so_luong_cach_dung_toi_da = db.Column(db.Integer)

    def __str__(self):
        return str(
            self.so_luong_benh_nhan_kham_trong_ngay) + '-' + self.so_luong_loai_benh_toi_da + '-' + self.so_luong_thuoc_toi_da + '-' + self.so_luong_don_vi_tinh_toi_da + '-' + self.so_luong_cach_dung_toi_da

    def serialize(self):
        return {
            'qui_dinh_id': self.qui_dinh_id,
            'so_luong_benh_nhan_kham_trong_ngay': self.so_luong_benh_nhan_kham_trong_ngay,
            'so_luong_loai_benh_toi_da': self.so_luong_loai_benh_toi_da,
            'so_luong_thuoc_toi_da': self.so_luong_thuoc_toi_da,
            'so_luong_don_vi_tinh_toi_da': self.so_luong_don_vi_tinh_toi_da,
            'so_luong_cach_dung_toi_da': self.so_luong_cach_dung_toi_da,
        }


class GopY(db.Model):
    gop_y_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_nguoi_gui =  db.Column(db.String(50), nullable=False)
    email_nguoi_gui = db.Column(db.String(50), nullable=False)
    tieu_de = db.Column(db.String(100), nullable=False)
    noi_dung = db.Column(db.String(5000), nullable=False)

db.create_all()


