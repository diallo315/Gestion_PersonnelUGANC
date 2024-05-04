from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from .models import *
# =================================================== FONCTION DE GENERE DE PDF =================================




def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

# ================================================ IMPRIMER PERSONNEL ===========================================

class DownloadPDF_Personnel(View):
    def get(self, request):
        personnel = Personnel.objects.all()
        administrationGeneral = AdministrationGeneral.objects.all()
        categorie = Categorie.objects.all()

        context = {
            'personnels' : personnel, 
            'administrationGenerals' : administrationGeneral,
            'categories': categorie,
        }

        pdf = render_to_pdf('src/pdf/personnel.html.twig', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Document_%s.pdf" % ("12341231")
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Failed to generate PDF", status=404)

class ViewPDF_Personnel(View):
    def get(self, request):
        personnel = Personnel.objects.all()
        administrationGeneral = AdministrationGeneral.objects.all()
        categorie = Categorie.objects.all()

        context = {
            'personnels': personnel, 
            'administrationGenerals': administrationGeneral,
            'categories': categorie,
        }

        pdf = render_to_pdf('src/pdf/personnel.html.twig', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        return HttpResponse("Failed to generate PDF", status=404)
    
# ================================================ IMPRIMER Un Personnel  ===========================================

class DownloadPDF_detailPersonnel(View):
    def get(self, request, id):
        personnel = get_object_or_404(Personnel, id=id)

        context = {
            'personnel' : personnel,
        }

        pdf = render_to_pdf('src/pdf/detailPersonnel.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "DetailPersonne_%s.pdf" % ("12341231")
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Failed to generate PDF", status=404)

class ViewPDF_detailPersonnel(View):
    def get(self, request, id):
        personnel = get_object_or_404(Personnel, id=id)

        context = {
            'personnel' : personnel,
        }

        pdf = render_to_pdf('src/pdf/detailPersonnel.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        return HttpResponse("Failed to generate PDF", status=404)
    
# ================================================ IMPRIMER LETTRE DE RELEVE BANCAIRE ===========================================

class DownloadPDF_docBancaire(View):
    def get(self, request, id):
        lBancaire = get_object_or_404(LettreBanque, id=id)

        context = {
            'lBancaire' : lBancaire,
        }

        pdf = render_to_pdf('src/pdf/genereDocB.html.twig', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Bancaire_%s.pdf" % ("12341231")
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Failed to generate PDF", status=404)

class ViewPDF_docBancaire(View):
    def get(self, request, id):
        lBancaire = get_object_or_404(LettreBanque, id=id)

        context = {
            'lBancaire' : lBancaire,
        }

        pdf = render_to_pdf('src/pdf/genereDocB.html.twig', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        return HttpResponse("Failed to generate PDF", status=404)
    
# ================================================ IMPRIMER LETTRE DE RELEVE BANCAIRE ===========================================

class DownloadPDF_docLettre(View):
    def get(self, request, id):
        lLettre = get_object_or_404(Lettre, id= id)

        context = {
            'lLettre' : lLettre,
        }

        pdf = render_to_pdf('src/pdf/genereDocL.html.twig', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Lettre_%s.pdf" % ("12341231")
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Failed to generate PDF", status=404)

class ViewPDF_docLettre(View):
    def get(self, request, id):
        lLettre = get_object_or_404(Lettre, id=id)

        context = {
            'lLettre' : lLettre,
        }

        pdf = render_to_pdf('src/pdf/genereDocB.html.twig', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        return HttpResponse("Failed to generate PDF", status=404)
    
