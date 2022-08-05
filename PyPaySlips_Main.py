# Python program to read
# file word by word
# opening the text file
from importlib.util import module_for_loader
import fitz
import os
import glob
import PyPDF2
import re
import time
from PyPDF2 import PdfFileReader, PdfFileWriter
from jdatetime import date

today=date.today()
t=time.localtime()

current_time = str(time.strftime("%H-%M-%S", t))
dd=str(today.day)
mm=str(today.month)
yy=str(today.year)

def fish_mounth():
    if mm=='1':
        mounth='Farvardin'
    elif mm=='2':
        mounth='Ordibehesht'
    elif mm=='3':
        mounth='Khordad'
    elif mm=='4':
        mounth='Tir'
    elif mm=='5':
        mounth='Mordad'
    elif mm=='6':
        mounth='Shahrivar'
    elif mm=='7':
        mounth='Mehr'
    elif mm=='8':
        mounth='Aban'
    elif mm=='9':
        mounth='Azar'
    elif mm=='10':
        mounth='Dey'
    elif mm=='11':
        mounth='Bahman'
    elif mm=='12':
        mounth='Esfand'
    return(mounth)

#access All pdf files in directory
for all_pdf_files in glob.glob('Input\\*.pdf'):
    #fish_file_name='sample.pdf'
    fishdoc=PyPDF2.PdfFileReader(all_pdf_files)
    fish_file_pages=fishdoc.getNumPages()
    fishdocument = fitz.open(all_pdf_files)
    #---------------------------------------------------------------
    keywords_list=[]
    with open('Input\\input_keywords.txt','r') as file:
        for i in range(1000):
            # reading each line	
            for txt_line in file:    
                # reading each word		
                for txt_keyword_list in txt_line.split(','):
                    #remove front and back white spaces and save in list
                    keywords_list.append(txt_keyword_list.lstrip())
                    # displaying the words		
                #print(keywords_list)
    #----------------------------------------------------------------
    for j in range(len(keywords_list)):
        search_prs_no=keywords_list[j]
        list_pages=[]
        for i in range(fish_file_pages):
            current_page=fishdoc.getPage(i)
            prs_fish=current_page.extract_text()
            if re.findall(search_prs_no,prs_fish):
                prs_fish_page_no=len(re.findall(search_prs_no,prs_fish))
                list_pages.append((prs_fish_page_no,i))
        #print(list_pages)
        prs_fish_page_no=[tup[1] for tup in list_pages ]
        print('Personel Page Number is:',prs_fish_page_no)
        #-----------------------------------------------------------------
        pdfWriter=PdfFileWriter()
        today=date.today()
        for page_number in prs_fish_page_no:
            pdfWriter.addPage(fishdoc.getPage(page_number))
            try:
               os.makedirs('Output\\'+yy+'\\'+keywords_list[j])
            except:
                continue

        with open('Output\\'+yy+'\\'+keywords_list[j]+'\\'+keywords_list[j]+' (D-'+yy+'-'+mm+' '+fish_mounth()+'-'+dd+') (T-'+current_time+').pdf','wb') as f:
            pdfWriter.write(f)
            f.close()
print(yy,mm,dd,current_time)
print('done',fish_mounth())
