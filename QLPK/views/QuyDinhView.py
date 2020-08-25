from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from QLPK import models, dao


class QuyDinhView(ModelView):
    print(dao.GetAmountOfRules())
    can_edit = True
    can_create = True if dao.GetAmountOfRules() == 0 else False
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(qui_dinh_id="Mã quy định", so_luong_benh_nhan_kham_trong_ngay="Số lượng bệnh nhân khám trong ngày", so_luong_loai_benh_toi_da="Số lượng loại bệnh tối đa",
                         so_luong_thuoc_toi_da="Số lượng thuốc tối đa", so_luong_don_vi_tinh_toi_da="Số lượng đơn vị tính tối đa", so_luong_cach_dung_toi_da="Số lượng cách dùng tối đa")
    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated

