from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from QLPK import dao


class DonViView(ModelView):
    cac_quy_dinh = dao.LayCacQuyDinh()
    so_luong_don_vi_tinh_toi_da = dao.SoLuongDonVi()
    can_create = True if so_luong_don_vi_tinh_toi_da <= cac_quy_dinh.so_luong_don_vi_tinh_toi_da else False

    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(don_vi_id = "Mã đơn vị", ten_don_vi="Tên đơn vị",)

    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated

    def on_model_change(self, form, model, is_created=False):
        cac_quy_dinh = dao.LayCacQuyDinh()
        so_luong_don_vi_tinh_toi_da = dao.SoLuongDonVi()
        if so_luong_don_vi_tinh_toi_da > cac_quy_dinh.so_luong_don_vi_tinh_toi_da:
            self.can_create = False
        else:
            self.can_create = True


    def after_model_delete(self, model):
        cac_quy_dinh = dao.LayCacQuyDinh()
        so_luong_don_vi_tinh_toi_da = dao.SoLuongDonVi()
        if so_luong_don_vi_tinh_toi_da > cac_quy_dinh.so_luong_don_vi_tinh_toi_da:
            self.can_create = False
        else:
            self.can_create = True
