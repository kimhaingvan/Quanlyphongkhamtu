from flask import render_template
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from QLPK import dao


class HoaDonView(ModelView):
    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        cac_phieu_kham_benh = dao.LayCacPhieuKhamBenh()
        cac_loai_thuoc = dao.LayCacLoaiThuoc()
        cac_don_vi = dao.LayCacDonVi()
        cac_chi_dan = dao.LayCacChiDan()

        return render_template('clients/payment.html', cac_don_vi=cac_don_vi, cac_chi_dan=cac_chi_dan, cac_phieu_kham_benh = cac_phieu_kham_benh, cac_loai_thuoc=cac_loai_thuoc )

    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(hoa_don_id="Mã hóa đơn", benh_nhan="Mã bệnh nhân", phieu_kham_benh="Phiếu khám bênh",user="Người tạo", tien_kham="Tiền khám", ngay_thanh_toan="Ngày thanh toán", tong_tien="Tổng tiền", ds_chi_tiet_hoa_don="Các chi tiết hóa đơn")

    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated
