from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ChiTietHoaDonView(ModelView):
    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(hoa_don="Mã hóa đơn", thuoc ="Mã thuốc", don_vi="Mã đơn vị", chi_dan="Mã chỉ dẫn", so_luong="Số lượng",)
    column_list = ()
    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated
