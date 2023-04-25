#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import openpyxl
import yaml

def read_excel_file(file_path, row_headers=None):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = {}

    if row_headers:
        header_row = {}
        normalized_headers = [header.lower() for header in row_headers]
        for idx, cell in enumerate(sheet[1]):
            if cell.value.lower() in normalized_headers:
                header_row[cell.value] = idx + 1
    else:
        header_row = {cell.value: idx + 1 for idx, cell in enumerate(sheet[1])}

    for row in sheet.iter_rows(min_row=2):
        row_data = {}
        for header, col in header_row.items():
            row_data[header] = row[col - 1].value
        data[row[0].value] = row_data

    return data

def main():
    module = AnsibleModule(
        argument_spec=dict(
            file_path=dict(type='str', required=True),
            row_headers=dict(type='list', elements='str', required=False, default=None),
        ),
        supports_check_mode=True
    )

    file_path = module.params['file_path']
    row_headers = module.params['row_headers']

    try:
        data = read_excel_file(file_path, row_headers)
        yaml_output = yaml.dump(data)
        module.exit_json(changed=False, yaml_output=yaml_output)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
