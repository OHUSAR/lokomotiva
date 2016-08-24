#!/usr/bin/python
# -*- coding: utf-8 -*-
from io import BytesIO
import xlsxwriter

from user_profiles.models import ChildProfile


def write_to_excel(event, children, parents, trainers):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)

    worksheet_s = workbook.add_worksheet('{}.xls'.format(
        event.name, event.start_date, event.end_date
    ))
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    title_text = "{} {}: {} až {}".format(
        "Dochádzka pre udalosť", event.name, event.start_date, event.end_date
    )
    worksheet_s.merge_range('B2:H2', title_text, title)

    worksheet_s.write(4, 2, "Deti", header)
    worksheet_s.write(4, 4, "Rodičia", header)
    worksheet_s.write(4, 6, "Tréneri", header)

    for i, child in enumerate(children):
        try:
            worksheet_s.write(5 + i, 2, child.childprofile)
        except ChildProfile.DoesNotExist:
            worksheet_s.write(5 + i, 2, child.username)

    for i, parent in enumerate(parents):
        worksheet_s.write(5 + i, 4, parent.username)

    for i, trainer in enumerate(trainers):
        worksheet_s.write(5 + i, 6, trainer.username)

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data
