def extract_asm_line_data(asm_line):
    output = {}
    
    asm_line_split_arr = asm_line.split()
   
    if (' DS ' in asm_line):
        decl_idx = asm_line.index(' DS ') + 4
            
    if (' DC ' in asm_line):
        decl_idx = asm_line.index(' DC ') + 4

    if ((asm_line_split_arr[1] == 'DS') or (asm_line_split_arr[1] == 'DC')):
        output["var_name"] = asm_line_split_arr[0]
        output["dec_type"] = asm_line_split_arr[1]
        output["data_type"] = (asm_line[decl_idx:]).lstrip()
    else:
        output["var_name"] = ''
        output["dec_type"] = asm_line_split_arr[0]
        output["data_type"] = (asm_line[decl_idx:]).lstrip()
    return(output)

#################################################################

def extract_data_declaration(data_dec,char_types):
    output = {}
  
    if (data_dec[0] == "0"):
        output['group_var'] = 1
    else:
        output['group_var'] = 0
    
    output['valueContinuation'] = 0
    output['value'] = ''
   
    if (data_dec.find('(') == 0):
        type_idx = data_dec.index(')') 
    else:
        type_idx = 0
        
    data_dec_list = list(data_dec[type_idx:])
    for i in data_dec_list:
        if (i.isalpha()):
            data_type = i
            break

    for char_type in char_types:
        if (char_type['type'] == data_type):
            output['datatype'] = char_type['type']
            if (type_idx == 0):
                data_dec_multiplier = data_dec[0:data_dec.index(char_type['type'])]
            else:
                data_dec_multiplier = data_dec[1:type_idx]
            
            len_chk = type_idx + len(char_type['type'])
            if (len(data_dec) <= len_chk):
                output['varsize'] = 1
            else:
                if (data_dec[len_chk] == 'L'):
                    if ("'" in data_dec):                        
                        if ((" " in data_dec) and (data_dec.index(" ") < data_dec.index("'"))):
                            if ((data_dec[len_chk+1 : data_dec.index(" ")]).isnumeric()):
                                output['varsize'] = int((data_dec[len_chk+1 : data_dec.index(" ")]))
                            else:
                                output['varsize'] = data_dec[len_chk+1 : data_dec.index(" ")]
                        else:
                            if ((data_dec[len_chk+1 : data_dec.index("'")]).isnumeric()):
                                output['varsize'] = int((data_dec[len_chk+1 : data_dec.index("'")]))
                            else:
                                output['varsize'] = data_dec[len_chk+1 : data_dec.index("'")]
                            
                            output['value'] = data_dec[data_dec.index("'")+1:]
                            if ("'" in output['value']):
                                output['value'] = output['value'][:output['value'].index("'")]                                
                            else:
                                output['valueContinuation'] = 1
                    elif (" " in data_dec):
                        if ((data_dec[len_chk+1 : data_dec.index(" ")]).isnumeric()):
                            output['varsize'] = int((data_dec[len_chk+1 : data_dec.index(" ")])) 
                        else:
                            output['varsize'] = data_dec[len_chk+1 : data_dec.index(" ")]
                    else:
                        if ((data_dec[len_chk+1:]).isnumeric()):
                            output['varsize'] = int((data_dec[len_chk+1:]))
                        else:
                            output['varsize'] = data_dec[len_chk+1:]
                else:
                    output['varsize'] = 1
                    if ("'" in data_dec): 
                        output['value'] = data_dec[data_dec.index("'"):]
                        if ("'" in output['value']):
                            output['value'] = output['value'][:output['value'].index("'")]                                
                        else:
                            output['valueContinuation'] = 1
            output['isArray'] = 0
            if (data_dec_multiplier.isnumeric()):
                output['multiplier'] = int(data_dec_multiplier)
                if (output['multiplier'] > 1):
                    output['isArray'] = 1
                    output['varlen'] = output['varsize'] * char_type['length'] * output['multiplier'] 
                else:
                    output['varlen'] = output['varsize'] * char_type['length']
            else:
                if (data_dec_multiplier == ''):
                    output['multiplier'] = 1
                    output['varlen'] = output['varsize'] * char_type['length']
                else:
                    output['multiplier'] = data_dec_multiplier
                    
            output['varlenInBits'] = char_type['bintype']
            return(output)