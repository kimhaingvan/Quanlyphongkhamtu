from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from QLPK import dao


class PhieuKhamBenhView(ModelView):
    cac_quy_dinh = dao.LayCacQuyDinh()
    so_luong_phieu_kham_benh_trong_ngay = dao.SoLuongPhieuKhamBenhTrongNgay()
    # can_create = True if so_luong_phieu_kham_benh_trong_ngay <= cac_quy_dinh.so_luong_benh_nhan_kham_trong_ngay else False
    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(benh_nhan="Bệnh nhân", ngay_kham="Ngày khám", trieu_chung="Triệu chứng",
                        loai_benh="Loại bệnh", loai_benh_du_doan_id="Loại bệnh dự đoán")
    column_exclude_list = ['detele_at', 'create_at', ]
    column_filters = ['benh_nhan']

    def is_accessible(self):
            return current_user.is_authenticated

    def on_model_change(self, form, model, is_created=False):
        cac_quy_dinh = dao.LayCacQuyDinh()
        so_luong_phieu_kham_benh_trong_ngay = dao.SoLuongPhieuKhamBenhTrongNgay()
        if so_luong_phieu_kham_benh_trong_ngay > cac_quy_dinh.so_luong_benh_nhan_kham_trong_ngay:
            self.can_create = False
        else:
            self.can_create = True


    def after_model_delete(self, model):
        cac_quy_dinh = dao.LayCacQuyDinh()
        so_luong_phieu_kham_benh_trong_ngay = dao.SoLuongPhieuKhamBenhTrongNgay()

        if so_luong_phieu_kham_benh_trong_ngay > cac_quy_dinh.so_luong_benh_nhan_kham_trong_ngay:
            self.can_create = False
        else:
            self.can_create = True
