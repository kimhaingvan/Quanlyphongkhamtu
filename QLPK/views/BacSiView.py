from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from QLPK import dao
from QLPK.models import Bacsi

class BacSiView(ModelView):
    so_luong_danh_sach_bac_si = len(dao.LayTatCaBacSi())
    can_create = True if so_luong_danh_sach_bac_si <= 50 else False
    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(bac_si_id="Mã bác sĩ", ho_ten="Họ tên", nam_sinh="Năm sinh", mieu_ta="Miêu tả")

    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated


    def on_model_change(self, form, model, is_created=False):
        tat_ca_bac_si = dao.LayTatCaBacSi()

        if len(tat_ca_bac_si) > 50:
            self.can_create = False
        else:
            self.can_create = True


    def after_model_delete(self, model):
        tat_ca_bac_si = dao.LayTatCaBacSi()
        if len(tat_ca_bac_si) > 50:
            self.can_create = False
        else:
            self.can_create = True

