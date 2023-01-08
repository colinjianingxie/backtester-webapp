from django.views.generic import TemplateView


class DisplayDailyPriceView(TemplateView):
    template_name = "display_price.html"
