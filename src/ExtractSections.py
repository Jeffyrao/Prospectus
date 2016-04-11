'''
Created on Mar 28, 2016

@author: jeffy
'''
import sys
import os
import re

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__": 
    reload(sys)
    sys.setdefaultencoding('ascii') 
    num_files, num_empty_files = 0, 0
    html_flag = True
    for filename in os.listdir("../html_files/"):
        file = open('../html_files/'+filename, 'r')
        num_files += 1
        if filename.endswith('.txt'):
            table_line, line_counter = -1, 0
            page_flag, table_flag, section_flag = False, False, False
            sec_list = []
            regexp = re.compile(r'\.\.+')
            empty_line = 0
            for line in file.readlines():
                line_counter += 1
	        # read table contents
                if 'TABLE OF CONTENTS' == line.strip().upper() and table_flag == False:
                    table_line = line_counter
                    table_flag = True
                    empty_line = 0
                    continue
                if line_counter - empty_line - table_line < 20 and table_line != -1:
                    # original .txt files
                    if html_flag == False and regexp.search(line) is not None:
                        sec = re.search('[a-zA-Z\s]+',line).group().upper()
                        if sec != None and len(sec) != 0:
                            sec_list.append(sec)
                    if html_flag == True: # .html files
                        # section name is at least longer than 8.
                        if len(line.strip()) >= 5 and 'TABLE OF CONTENTS' not in line.upper(): 
                            # parse section name from line
                            sec = re.search('[a-zA-Z\s]+',line.strip())
                            if sec != None:
                                sec_list.append(sec.group().upper().strip())
                        else:
                            empty_line += 1
                # verify whether table of contents is correct 
                if table_flag and line_counter - empty_line - table_line > 20 \
                    and 'PROSPECTUS SUMMARY' not in sec_list and 'RISK FACTORS' not in sec_list \
                    and 'USE OF PROCEEDS' not in sec_list:
                    sec_list = []
                    table_flag = False
            
            file = open('../html_files/'+filename, 'r')
            profile = open('../sec_files/pro_' + filename, 'w')
            riskfile = open('../sec_files/risk_' + filename, 'w')
            usefile = open('../sec_files/use_' + filename, 'w')
            manfile = open('../sec_files/man_' + filename, 'w')
            totalfile = open('../sec_files/total_' + filename, 'w')
            pro_flag, risk_flag, use_flag, man_flag = False, False, False, False
            empty_flag = True
            line_counter = 0
            table_line = -1
            manage_regexp = re.compile(r'MANAGEMENT.S\sDISCUSSION')
            for line in file.readlines(): 
                line_counter += 1
                line = line.strip()
                
                # judge the end of section                
                if section_flag:
                    if line == None or len(line) == 0:
                        continue
                    for sec in sec_list:
                        if sec == line.upper(): # end of section
                            pro_flag, risk_flag, use_flag, man_flag, section_flag = False, False, False, False, False
                            break
                
                # for documents that have page numbers                
                if page_flag and len(line) < 80:
                    if line == None or line.isspace():
                        continue
                    for sec in sec_list:
                        if sec in line.upper():
                            pro_flag, risk_flag, use_flag, man_flag, section_flag = False, False, False, False, False
                    if manage_regexp.search(line.upper()) is not None:
                        man_flag = True
                        empty_flag = False
                        section_flag = True
                # for documents that dont have page numbers
                if len(line) < 50 and line_counter - table_line > 30: 
                    if 'PROSPECTUS SUMMARY' == line.upper() or 'SUMMARY' == line.upper():
                        pro_flag = True
                    if 'RISK FACTORS' == line.upper():
                        risk_flag = True
                    if 'USE OF PROCEEDS' == line.upper():
                        use_flag = True
                    if 'PROSPECTUS SUMMARY' == line.upper() \
                       or 'SUMMARY' == line.upper() \
                       or 'RISK FACTORS' == line.upper() \
                       or 'USE OF PROCEEDS' == line.upper():
                        empty_flag = False
                        section_flag = True
                # start of management discussion section
                if manage_regexp.search(line.upper()) is not None and len(line) < 150:
                    man_flag = True
                    empty_flag = False
                    section_flag = True
                    
                if section_flag:
                    totalfile.write(line+'\n')
                if pro_flag:
                    profile.write(line+'\n')
                if risk_flag:
                    riskfile.write(line+'\n')
                if use_flag:
                    usefile.write(line+'\n')
                if man_flag:
                    manfile.write(line+'\n')
                if '<PAGE>' in line: # page flag
                    page_flag = True
                elif is_int(line.strip()) and int(line.strip()) < 40 and int(line.strip()) > 0:
                    page_flag = True # page number 
                else:
                    page_flag = False
            if empty_flag:
                num_empty_files += 1
                print('empty file:' + filename)
            profile.close()
            riskfile.close()
            usefile.close()
            manfile.close()
            totalfile.close()
    print('number of files: ' + str(num_files) + ', empty files:' + str(num_empty_files))
                
                        
