from odoo import models


class PatientCardXLSX(models.AbstractModel):
    _name = 'report.hospital.report_patient_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, line):
        c = 0
        for lines in line:
            c += 1
            format1 = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': True})
            format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
            sheet = workbook.add_worksheet('Patient Card %s' % (c))
            sheet.set_column(9, 2, 20)
            sheet.set_column(1, 1, 15)
            sheet.write(1, 1, 'Patient ID', format1)
            sheet.write(1, 2, lines.patient_inscription_id, format2)
            sheet.write(2, 1, 'Name', format1)
            sheet.write(2, 2, lines.patient_name, format2)
            sheet.write(3, 1, 'Gender', format1)
            sheet.write(3, 2, lines.patient_gender, format2)
            sheet.write(4, 1, 'Birth Date', format1)
            sheet.write(4, 2, lines.patient_birth_date, format2)
            sheet.write(5, 1, 'Age', format1)
            sheet.write(5, 2, lines.patient_age, format2)
            sheet.write(6, 1, 'Age Group', format1)
            sheet.write(6, 2, lines.patient_age_group, format2)
            sheet.write(7, 1, 'Email', format1)
            sheet.write(7, 2, lines.patient_email, format2)
            sheet.write(8, 1, 'Contact', format1)
            sheet.write(8, 2, lines.patient_contact, format2)
            sheet.write(9, 1, 'Progress', format1)
            sheet.write(9, 2, lines.patient_progress, format2)
            sheet.write(10, 1, 'Doctor', format1)
            sheet.write(10, 2, lines.doctor_inscription_id.doctor_name, format2)
            sheet.write(11, 1, 'Doctor Gender', format1)
            sheet.write(11, 2, lines.doctor_gender, format2)
