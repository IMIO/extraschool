# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Extraschool',
    'version': '9.1.0.10',
    'author': 'Town of La Bruyère and Imio',
    'depends': ['base',
                'report',
                'mail',
                'decimal_precision',
                'web',
                ],

    'css': [
        'static/src/css/test.css',
        'static/src/css/tpl_qrcodes_wizard_report.css',
    ],
    'demo': [],
    'test': [],
    'data': [
        'scripts/update_seq.xml',
        # 'scripts/update_one_report.sql',
        # 'scripts/update_activity_category.xml',
        'data/data_days.xml',
        'data/data_health_sheet.xml',
        'data/data_health_sheet_allergy.xml',
        'data/data_init.xml',
        'data/data_level.xml',
        'security/extraschool_security.xml',
        'data/data_tags_invoice.xml',
        'security/extraschool_security.xml',
        'security/ir.model.access.csv',
        'views/extraschool_age_group.xml',
        'views/extraschool_activitycategory.xml',
        'views/extraschool_organising_power.xml',
        'views/extraschool_activity.xml',
        'views/extraschool_activityoccurrence.xml',
        'views/extraschool_activity_occurrence_correction_wizard.xml',
        'views/extraschool_accrued.xml',
        'views/extraschool_biller.xml',
        'views/extraschool_childsimportfilter.xml',
        'views/extraschool_childsimport.xml',
        'views/extraschool_childsworkbook_wizard.xml',
        'report/child_qrcode.xml',
        'views/extraschool_coda.xml',
        'views/extraschool_discount.xml',
        'views/extraschool_guardianprestationtimes.xml',
        'views/extraschool_guardian.xml',
        'views/extraschool_initupdate_wizard.xml',
        'views/extraschool_invoice_wizard.xml',
        'views/extraschool_invoice.xml',
        'views/extraschool_mainsettings.xml',
        'views/extraschool_manuel_invoice_wizard.xml',
        'views/extraschool_negatif_payment_correction_wizard.xml',
        # 'views/extraschool_move_prepaiement.xml',
        'views/extraschool_parent.xml',
        'views/extraschool_parent_fusion_wizard.xml',
        'views/extraschool_payment.xml',
        'views/extraschool_payment_wizard.xml',
        'views/extraschool_place.xml',
        'views/extraschool_one_report.xml',
        'views/extraschool_subvention_report.xml',
        'views/extraschool_plain_report.xml',
        'views/extraschool_pda_prestation_times.xml',
        'views/extraschool_pdaprestationtimes_correction_wizard.xml',
        'views/extraschool_prestationscheck_wizard.xml',
        'views/extraschool_prestationtimes.xml',
        'views/extraschool_prestation_times_of_the_day.xml',
        'views/extraschool_prestation_times_encodage_manuel.xml',
        'views/extraschool_prestation_times_encodage_manuel_wizard.xml',
        'views/extraschool_presta_stat.xml',
        'views/extraschool_presta_activity.xml',
        'views/extraschool_price_list.xml',
        'views/extraschool_qrcodes_wizard.xml',
        'views/extraschool_report.xml',
        'views/extraschool_reminder.xml',
        'views/extraschool_remindersjournal.xml',
        'views/extraschool_smartphone.xml',
        'views/extraschool_taxcertificates.xml',
        'views/extraschool_timecorrection.xml',
        'views/extraschool_school.xml',
        'views/extraschool_schoolimplantation.xml',
        'views/extraschool_class.xml',
        'views/extraschool_level.xml',
        'views/extraschool_child.xml',
        'views/extraschool_child_fusion_wizard.xml',
        'views/extraschool_child_registration.xml',
        'views/extraschool_child_registration_wizard.xml',
        'views/extraschool_health_sheet.xml',
        'views/extraschool_settings.xml',
        'views/extraschool_annual_report.xml',
        'views/extraschool_refund_wizard.xml',
        'views/extraschool_res_users.xml',
        # 'views/widgets.xml',
        'views/extraschool_config_smartphone.xml',
        'views/extraschool_query_sql.xml',
        # 'views/extraschool_qrconfig.xml',
        'views/extraschool_prestation_times_history.xml',
        'wizard/views/extraschool_no_value_wizard.xml',
        'views/extraschool_view.xml',

        'report/biller/biller_summary_no_style.xml',
        'report/biller/biller_detail_no_style.xml',
        'report/child_registration.xml',
        'report/coda_report.xml',
        'report/tax_certificate_detail_report.xml',
        'report/parent.xml',
        'report/qrcode_report.xml',
        'report/horaire_guardian_report.xml',
        'report/layout/extraschool_layout.xml',
        'report/layout/biller_report_layout.xml',
        'report/layout/healthy_child_registration_report_layout.xml',
        'report/layout/invoice_report_layout.xml',
        'report/layout/payment_invitation_report_layout.xml',
        'report/layout/reminder_report_layout.xml',
        'report/layout/qrcode_report_layout.xml',
        'report/layout/healthy_report_layout.xml',
        'report/health/healthy.xml',
        'report/invoice/invoice_std_body.xml',
        'report/invoice/invoice_std_body_activity_without_date.xml',
        'report/invoice/invoice_regroup_by_activity.xml',
        'report/invoice/invoice_regroup_by_activity_by_child.xml',
        'report/invoice/invoice_regroup_by_activity_by_child_no_count_no_quantity.xml',
        'report/invoice/invoice_regroup_by_activity_by_child_by_day_enter_exit.xml',
        'report/invoice/invoice_regroup_by_activity_by_child_calendar_style.xml',
        'report/invoice/invoice_std_footer.xml',
        'report/invoice/invoice_ref_and_period_no_style.xml',
        'report/qrcode/qrcode_name_child.xml',
        'report/common/pre_print_virement.xml',
        'report/common/amount_no_style.xml',
        'report/common/comment_no_style.xml',
        'report/common/page_number_no_style.xml',
        'report/common/page_number_right.xml',
        'report/common/std_header.xml',
        'report/common/adresse_no_style.xml',
        'report/common/html_text.xml',
        'report/taxe_certificate_report.xml',
        'report/common/activity_categ_invoice_comment_no_style.xml',
        'report/common/payment_info_no_style.xml',
        'report/common/payment_info_with_frame.xml',
        'report/common/parent_credit.xml',
        'report/common/sign_no_style.xml',
        'report/common/sign_img_no_style.xml',
        'report/common/double_sign_no_style.xml',
        'report/common/spacer_2cm.xml',
        'report/common/invoice_summary.xml',
        'report/common/payment_info_amount_one_row.xml',
        'report/custo_client/assesse.xml',
        'report/custo_client/hannut.xml',
        'report/custo_client/theux.xml',
        'report/custo_client/lierneux.xml',
        'report/custo_client/neufchateau.xml',
        'report/custo_client/yvoir.xml',
        'report/custo_client/durbuy.xml',
        'report/custo_client/clavier.xml',
        'report/custo_client/jurbise.xml',
        'report/custo_client/engis.xml',
        'report/custo_client/ohey.xml',
        'report/custo_client/hastiere.xml',
        'report/custo_client/dinant.xml',
        'report/custo_client/ferrieres.xml',
        'report/custo_client/tournai.xml',
        'report/custo_client/burdinne.xml',
        'report/custo_client/ittre.xml',
        'report/custo_client/mettet.xml',
        'report/custo_client/fosses_la_ville.xml',
        'report/reminder/reminder_text.xml',
        'report/parent_invoices_summary.xml'
    ],
    'installable': True,
    'application': True,
    'description': "This module is to manage billing attendance for extra school activities",
}
