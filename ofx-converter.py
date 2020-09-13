#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from jinja2 import Template
from pathlib import Path


class OFXConverter:

    def __init__(self, excel):
        self.template = 'template-neon-contabilizei.xml'
        self.excel = excel
        self.output = '/'.join(map(str, [Path(excel).parent, Path(excel).stem])) + '.ofx'

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
        with open(self.output, 'wb') as file:
            file.write(template.render(entries=entries)
                       .replace('\n', '\r\n')
                       .replace('ã', 'a')
                       .replace('ç', 'c')
                       .encode('us-ascii', 'ignore') + b'\n')


if __name__ == '__main__':
    ofx = OFXConverter('/home/christian/Downloads/lebrandt/extrato_periodo_neon_2020-08.xlsx')
    ofx.create()
