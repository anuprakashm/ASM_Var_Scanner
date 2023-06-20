import os
import sys
import json
from os.path import isfile, join
import functions.asm_extractor as asm_extractor

## Get files in the input folder
if (os.path.exists(sys.argv[1])):
    path = sys.argv[1]
    files = os.listdir(path)
else:
    print("*** ERROR ***", sys.argv[1], " - Directory does not exist!!!")
    exit()

output_json = "./output.json"
output_csv = "./output.csv"

if (os.path.isfile(output_json)):
    os.remove(output_json)
if (os.path.isfile(output_csv)):
    os.remove(output_csv)

file_json = open(output_json,'a')
file_csv = open(output_csv,'a')
file_json.write('[ \n')

## Load Assembler data definitions reference
data_def_path = "./config/DataDef.json"
first_line = 1

data_def_file = open(data_def_path, 'r')
data_def = json.loads(data_def_file.read())
data_def_file.close()

## Process Assembler file one by one
for file in files:
    fileName = join(path, file)
    if (not isfile(fileName)):
        continue

    ## Read lines in the Assembler file
    asm_lines = open(path + '/' + file, "r").readlines()
    ## Process Assembler program statements one by one
    processNextLine = 0
    value = ''

    for asm_line in asm_lines:
        if (processNextLine == 0):
            asm_line_details = {}
        asm_line = asm_line[0:72].replace('\n',' ')
        asm_line_split_arr = asm_line.split()
        
        if (((' DS ' in asm_line) and ((asm_line_split_arr[1] == 'DS') or (asm_line_split_arr[0] == 'DS'))) or 
            ((' DC ' in asm_line) and ((asm_line_split_arr[1] == 'DC') or (asm_line_split_arr[0] == 'DC'))) or 
            processNextLine):
            if (processNextLine == 0):
                asm_line_details['filepath'] = path
                asm_line_details['filename'] = file
                asm_line_details['line'] = asm_line
                asm_line_ext = asm_extractor.extract_asm_line_data(asm_line)
                asm_data_def_ext = asm_extractor.extract_data_declaration(asm_line_ext['data_type'],data_def)
                processNextLine = (asm_data_def_ext['valueContinuation'])
            else:
                if ("'" in asm_line):
                     value = asm_line[:asm_line.index("'")] 
                     processNextLine = 0
                else:
                     val_len = len(asm_data_def_ext['value'])
                    
                     if (val_len > 71):
                        value = asm_data_def_ext['value'][:71] 
                        if (asm_line[71] == ' '):
                            processNextLine = 0
                        else:
                            processNextLine = 1
                     else:
                         value = asm_data_def_ext['value'][:asm_data_def_ext['value'].find("'")] 
                         processNextLine = 0
                asm_data_def_ext['value'] = asm_data_def_ext['value'][:-1]  + value   

            if (processNextLine == 0):
                 value = ''
                 asm_line_details.update(asm_line_ext)
                 asm_line_details.update(asm_data_def_ext)
                 
                 if (first_line == 1):
                     file_json.write(json.dumps(asm_line_details))
                     file_csv.write(','.join(asm_line_details.keys()))
                     file_csv.write('\n')
                     file_csv.write(','.join(str(x) for x in asm_line_details.values()))
                     file_csv.write('\n')
                     first_line = 0
                 else:
                     file_json.write(',\n' + json.dumps(asm_line_details))
                     file_csv.write(','.join(str(x) for x in asm_line_details.values()))
                     file_csv.write('\n')

file_json.write('\n]')
file_json.close()   
file_csv.close()                