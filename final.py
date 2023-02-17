import pdfplumber

def extract_pdf_to_html(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        html = "<html><body>"
        current_tables = []
        in_table = False
        table_texts = []
        tab=""
        list_texts= []
        list_index=['1.','2.','3.','4.','5.','6.','7.','8.','9.','a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','i.','ii.','iii.','iv.','v.','vi.','vii.','viii.','ix.','x.','(i)','(ii)','(iii)','(iv)','(v)','(vi','(x','•','','(a','(b','(c','(d','(e)','(f','(g','(h)','(i)','(j)','(k)']
        in_list=False
        para=""

        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if current_tables:
                for table in tables:
                    current_tables[-1].extend(table)
            else:
                current_tables.extend(tables)

            if current_tables:
                in_table = True
                tab += "<table border=1>"
                for row in current_tables[0]:
                    tab += "<tr>"
                    for cell in row:
                        if cell != None:
                            table_texts.extend(cell.split("\n"))
                            tab += "<td>" + cell + "</td>"
                    #for row in current_tables[current_tables.index(row)+1]:
                       # if row[0]==' ':
                        #    for cell in row:
                         #       if cell != None:
                          #          table_texts.extend(cell.split("\n"))
                           #         tab += "<td>" + cell + "</td>"

                    tab += "</tr>"
                tab += "</table>"
                current_tables.pop(0)
            else:
                in_table = False
                paragraphs = page.extract_text().split("\n")
                for paragraph in paragraphs:
                    if paragraph not in table_texts:
                        if paragraph.startswith(tuple(list_index)):
                            if not in_list:
                                html += "<ul>"
                                in_list = True
                            
                            html += "<li>" + paragraph
                            list_texts.append(paragraph)
                            for para in paragraphs[paragraphs.index(paragraph)+1:]:
                                if para.startswith(" "):
                                    html+="</li>"
                                    break
                                
                                elif para.startswith(tuple(list_index)):
                                    html+="</li>"
                                    break
                                else:
                                    html +=  para
                                    list_texts.append(para)

                        else:
                            if in_list:
                                html += "</ul>"
                                in_list = False
                            
                            if paragraph not in list_texts:
                                
                                if paragraph.startswith(" "):
                                    html += "<p>" + para + "</p>"
                                    #print(para)
                                    para=""
                                else:
                                    para+=paragraph



            in_table = False
        if in_list:
            html += "</ul>"
        html+="<h2>"+"ALL Tables" +"</h2>"
        html += tab
        html += "</body></html>"
        return html

pdf_file = "/Users/arjunmalik/Downloads/TED.pdf"
html = extract_pdf_to_html(pdf_file)
with open("example1.html", "w") as file:
    file.write(html)


