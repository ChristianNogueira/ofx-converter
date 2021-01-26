#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pandas as pd
from jinja2 import Template
from pathlib import Path


class OFXConverter:

    def __init__(self, excel, template):
        self.template = template
        self.excel = excel
        self.output_file_name = str(Path(excel).stem) + '.ofx'
        self.output_file_path = '/'.join([str(Path(excel).parent), self.output_file_name])

    def read_data(self):
        df = pd.read_excel(self.excel, usecols=['Descrição', 'Data', 'Valor'])
        df.rename(columns={"Data": "date", "Descrição": "desc", "Valor": 'value'}, inplace=True)

        df = df.loc[df['value'] != 0]
        df['type'] = df.apply(lambda row: 'CREDIT' if row['value'] > 0 else 'DEBIT', axis=1)
        df['date'] = df['date'].dt.strftime('%Y%m%d000000')
        return df.to_dict(orient='records')

    def create(self):
        entries = self.read_data()
        with open(self.template, 'r') as file:
            template = Template(file.read())
        with open(self.output_file_path, 'wb') as file:
            file.write(template.render(entries=entries)
                       .replace('\n', '\r\n')
                       .replace('ã', 'a')
                       .replace('ç', 'c')
                       .encode('us-ascii', 'ignore') + b'\n')
