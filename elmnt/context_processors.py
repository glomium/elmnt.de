from django.utils.safestring import mark_safe
import random

def page_header(request):
    data = [
        ('img/turkei.jpg', 'Aus der Luft &uuml;ber &Ouml;l&uuml;deniz'),
        ('img/tolmin.jpg', 'Das slowenische Tolmin aus dem Gleitschirm fotografiert'),
        ('img/zweilaender.jpg', 'Zweil&auml;nder-Kletterseig an der Kanzelwand bei Obersdorf'),
        ('img/annecy.jpg', '&Uuml;ber dem Lac d\'Annecy'),
        ('img/bassano.jpg', 'Ein sp&auml;ter Nachmittag am Panettone in Bassano'),
        ('img/schirm.jpg', 'Mein Schirm der Arcus 6 compact von Swing'),
    ]
    image, title = random.choice(data)
    return {
        'page_header': {
            'title': mark_safe(title),
            'image': image,
        }
    }
