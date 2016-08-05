from telegrambotsican.views import StartView
from telegrambot.handlers import command

urlpatterns = [
    command('start', StartView.as_command_view()),
]