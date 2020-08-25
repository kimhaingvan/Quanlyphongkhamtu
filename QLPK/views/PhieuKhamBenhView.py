from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class PhieuKhamBenhView(ModelView):
    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(benh_nhan="Bệnh nhân", ngay_kham="Ngày khám", trieu_chung="Triệu chứng",
                        loai_benh="Loại bệnh", loai_benh_du_doan_id="Loại bệnh dự đoán")
    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated
