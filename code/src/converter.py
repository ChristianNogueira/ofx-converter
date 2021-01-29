#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Template
from pathlib import Path
from src.neon_excel import NeonExcel


class OFXConverter:

    def __init__(self, excel, template):
        self.template = template
        self.excel = excel
        self.output_file_name = str(Path(excel).stem) + '.ofx'
        self.output_file_path = '/'.join([str(Path(excel).parent), self.output_file_name])

    def create(self):
        entries = NeonExcel(self.excel).read_data()
        with open(self.template, 'r') as file:
            template = Template(file.read())
        with open(self.output_file_path, 'wb') as file:
            file.write(template.render(entries=entries)
                       .replace('\n', '\r\n')
                       .replace('ã', 'a')
                       .replace('ç', 'c')
                       .encode('us-ascii', 'ignore') + b'\n')
