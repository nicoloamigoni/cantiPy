from datetime import datetime
from weasyprint import HTML
import os

def create_pdf(songs):
    check = True
    for song in songs:
        if(song.translation and not(len(song.translation)==0 or song.translation[0]=="") and len(song.text) != len(song.translation)):
            print("[ERROR] Text and translation have different number of paragraphs for song ", song.title)
            check = False
        print("[INFO] Adding ", song.title)

    if not check:
        return False
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    filename = "output/SdC_" + date
    create_vert(songs, filename)
    create_proiez(songs, filename)

    print("[INFO] PDF created")
    return True

def create_vert(songs, filename):
    html_content = '''
        <html><head><style>
            @page { size: A4; }
            body { font-family: Arial, sans-serif; font-size: 11px;}
            h1 { font-size: 12px; }
            div { column-count: 2; }
            table td, table td * {
                vertical-align: top;
            }
            p { page-break-inside: avoid}
            
        </style></head><body>
    '''
    html_content += create_content(songs)
    html_content += "</body></html>"
    HTML(string=html_content).write_pdf(filename)

def create_proiez(songs, filename):
    html_content = '''
        <html><head><style>
            @page { size: A4 landscape; }
            body { font-family: Arial, sans-serif; font-size: 24px;}
            h1 { font-size: 24px; }
            div { column-count: 2; }
            table td, table td * {
                vertical-align: top;
            }
            p { page-break-inside: avoid}
            
        </style></head><body>
    '''
    html_content += create_content(songs, pagebreak=True)
    html_content += "</body></html>"
    HTML(string=html_content).write_pdf(filename+"_proiez")

def create_content(songs, pagebreak = False):
    html_content =""

    for song in songs:
        song.text = [line.replace("\n", "<br>") for line in song.text]

        

        html_content += f"<h1><b>{song.title}</b>"
        if song.author:
            html_content += f" (<i>{song.author}</i>)"
        html_content += "</h1>"
        
        if song.translation:
            song.translation = [line.replace("\n", "<br>") for line in song.translation]
            print("in")
            html_content += "<table>"
            for original, translation in zip(song.text, song.translation):
                html_content += f"<tr><td>{original}<br><br></td><td style='width:10px'></td><td><i>{translation}<br><br></i></td></tr>"
            html_content += "</table>"
        else:
            html_content += "<div>"
            for line in song.text:
                html_content += f"<p>{line}</p>"
            html_content += "</div>"
        if pagebreak:
            html_content += "<p style='page-break-before: always;'></p>"
    return html_content
