from telegrambot.bot_views.generic import TemplateCommandView

class StartView(TemplateCommandView):
    template_text = "bot/messages/start.txt"