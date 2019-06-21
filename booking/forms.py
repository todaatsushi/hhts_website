from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout as cf

from .models import Booking


class BookTourForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = cf.Layout(

            cf.Fieldset(
                _('基本情報'),
                cf.Div(
                    cf.Div(
                        cf.Field('scheduled_at', css_class='mr-3', placeholder=_('予定時間')),
                        cf.Field('duration', css_class='mr-3', placeholder=_('期間')),
                        cf.HTML(
                            _("""
                            <select name="transportation" class="mr-3 form-control" required="" id="id_transportation">
                              <option value="使う交通手段" selected disabled>使う交通手段</option>
                              <option value="電車">電車</option>
                              <option value="コーチ">コーチ</option>
                              <option value="自動車・バン">自動車・バン</option>
                              <option value="タクシ">タクシ</option>
                              <option value="その他">他の交通手段（”他に伝えたい情報”で伝えてください。）</option>
                            </select>
                            """)
                        ),
                        css_class='col-md-6'
                    ),
                    cf.Div(
                        cf.Field('places_to_visit', placeholder=_('訪問したい酒蔵'), rows='5'),
                        css_class='col-md-6'
                    ),
                    css_class='row form-group'
                )
            ),
            cf.Fieldset(
                _('個人情報'),
                cf.Div(
                    cf.Div(
                        cf.Field('contact_name', css_class='mr-3', placeholder=_('名前')),
                        cf.Field('contact_number', css_class='mr-3', placeholder=_('電話番号')),
                        cf.Field('contact_email', css_class='mr-3', placeholder=_('メールアドレス')),
                        css_class='col-md-6'
                    ),
                    cf.Div(
                        cf.Field('contact_address', placeholder=_('住所'), rows='5'),
                        css_class='col-md-6'
                    ),
                    css_class='row form-group'
                )
            ),
            cf.Fieldset(
                _('グループの情報'),
                cf.Div(
                    cf.HTML(
                        _("""
                        <input type="checkbox" name="is_group" class="mr-3 checkboxinput" placeholder="グループ予約" id="id_is_group" checked="">
                        <label for="is_group" class='mr-3'>グループ予約</label>
                        """)
                    ),
                    cf.Field('group_name', placeholder=_('グループ名前'), css_class='mr-3'),
                    cf.Field('group_number', placeholder=_('グループの数'), css_class='mr-3'),
                    cf.HTML(
                        _("""
                        <select name="age_group" class="mr-3 select form-control" required="" id="id_age_group">
                            <option value="NA" selected disabled>年齢層</option>
                            <option value="家族">家族</option>
                            <option value="大人">大人</option>
                            <option value="高齢者">高齢者</option>
                            <option value="子供・思春期">子供・思春期</option>
                            <option value="ミックス">ミックス</option>
                        </select>
                        """)
                    ),
                    css_class='form-inline'
                )
            ),
            cf.Fieldset(
                _('確認'),
                cf.Div(
                    cf.Div(
                        cf.Field('extra_details', placeholder=_('他に伝えたい情報'), rows='5'),
                        css_class='col-md-6'
                    ),
                    cf.Div(
                        cf.HTML(
                            _("""
                            <a href="{% url 'home' %}" class='btn btn-sm btn-block btn-custom-1 my-3'>戻る</a>
                            """)
                        ),
                        cf.ButtonHolder(
                            cf.Submit('submit', _('送る'), css_class='btn btn-sm btn-block btn-success my-3')
                        ),
                        css_class='col-md-4 offset-1'
                    ),
                    css_class='row'
                )
            )

        )

        super(BookTourForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = [
            'scheduled_at', 'duration', 'places_to_visit', 'transportation',
            'contact_name', 'contact_address', 'contact_email', 'contact_number',
            'is_group', 'group_name', 'group_number', 'age_group',
            'extra_details',
        ]
        widgets = {
            'scheduled_at': forms.DateTimeInput(format=['%d/%m/%y %H:%M']),
            'contact_email': forms.EmailInput(),
            'group_number': forms.NumberInput()
        }
