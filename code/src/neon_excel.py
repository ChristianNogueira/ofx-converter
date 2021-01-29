#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd


class NeonExcel:

    def __init__(self, file_path):
        self.file_path = file_path
        self.columns = {
            "Data": "date",
            "Descrição": "desc",
            "Valor": 'value'
        }

    def read_data(self):
        df = pd.read_excel(self.file_path, usecols=self.columns.keys())
        df.rename(columns=self.columns, inplace=True)

        df = df.loc[df['value'] != 0]
        df['type'] = df.apply(lambda row: 'CREDIT' if row['value'] > 0 else 'DEBIT', axis=1)
        df['date'] = df['date'].dt.strftime('%Y%m%d000000')
        return df.to_dict(orient='records')
