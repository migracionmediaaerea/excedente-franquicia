# Django things
from django.template.loader import get_template
from django.conf import settings
from django.template.loader import render_to_string

# Third party things
import pdfkit
import pytz
from datetime import datetime
# Python things
import platform
import os
import tempfile
import pytz

meses = {
    '1': "enero",
    '2': "febrero",
    '3': "marzo",
    '4': "abril",
    '5': "mayo",
    '6': "junio",
    '7': "julio",
    '8': "agosto",
    '9': "septiembre",
    '10': "octubre",
    '11': "noviembre",
    '12': "diciembre"
}

def generate_pdf(template_name:str, context_data, tipo_cambio):
    try:
        options = None

        # update context_data with static url
        tz = pytz.timezone('America/Mexico_City')
        fecha_tz = datetime.now().astimezone(tz)
        fecha_str = fecha_tz.strftime('%d de <mes> del %Y a las %H:%M %p')
        fecha = fecha_str.replace('<mes>', meses[str(fecha_tz.month)])

        context_data.update({
            'static': f'{settings.STATICFILES_DIRS[0]}',
            'dia': fecha_tz.day,
            'mes': meses[str(fecha_tz.month)],
            'year': fecha_tz.year,
            'fecha': fecha,
            'tipo_cambio': tipo_cambio,
        })

        # Get the template
        template = get_template(template_name)
        # Render the data in the template
        html = template.render(context_data)
        # options to config pdfkit
        options = {
            "page-size": 'Letter', # Page size 
            'title': "PDF title", # File title
            #'margin-top': '200px', # Margin top
            #'margin-right': '0px', # Margin right
            #'margin-left': '0px', # Margin left
            #'margin-bottom': '10px', # Margin botton
            'encoding': "ISO-8859-3", # File enconding, it can be UTF-8 but sometimes it does not work
            #'footer-html': f'{TEMPLATE_DIR}/acuses/footer.html', # Footer
            #'--header-html': f'{TEMPLATE_DIR}/acuses/header.html', # Header
            #'--header-spacing': '-223', # Header spacing from the content
            #'--footer-spacing': '-14', # Footer spacing from the content
            '--enable-local-file-access': "", # The pdf can access file from the local machine
            'viewport-size': '1280x1024', # Viewport size
            'javascript-delay': '2000', # Delay to load the js
        }

        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header_html:
            options['header-html'] = header_html.name
            header_html.write(render_to_string('acuses/header.html', context_data).encode('utf-8'))

        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header_html:
            options['footer-html'] = header_html.name
            header_html.write(render_to_string('acuses/footer.html', context_data).encode('utf-8'))
        
        # Config of wkhtmltopdf
        # Default is linux config else windows config
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf') \
            if platform.system() != 'Windows' \
            else pdfkit.configuration(
                # Windows config
                wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        )
        # This is the path to the css
        # STATICFILES_DIRS[0] are the dirs to access the static files like js, css and images, css mus be load here or using cdn in html
        css = [
            f'{settings.STATICFILES_DIRS[0]}/assets/css/styles.min.css', 
            f'{settings.STATICFILES_DIRS[0]}/assets/pdfbootstrap/css/bootstrap.min.css',
            # etc
        ]
        
        # Generate the pdf from string using the rendered html, the options and the config, we can add the css, and write the path to save it, 
        # in this case is not saved, it is just rendered miau
        # to add css just write css=css and the save path is output_path='miau.pdf'
        pdf_file = pdfkit.from_string(html, options=options, configuration=config, css=css)
        
        return pdf_file
    
    finally:
        if options:
            if options.get('header-html', None):
                os.remove(options['header-html'])

            if options.get('footer-html', None):
                os.remove(options['footer-html'])