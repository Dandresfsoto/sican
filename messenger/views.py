from django.views.generic import TemplateView
import os
from django.shortcuts import HttpResponse
import json
import requests
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL


class WebHookView(TemplateView):
    template_name = 'rh/administrativos/lista.html'
    permission_required = "permisos_sican.rh.cargos.ver"


    def get(self, request, *args, **kwargs):
        url_base = self.request.META['HTTP_ORIGIN']
        send_mail_templated.delay('email/change_password.tpl', {'url_base':url_base,'first_name':request.GET.get('hub.mode'),'last_name':request.GET.get('hub.verify_token'),'email':os.getenv('VALIDATION_TOKEN'),'password':''}, DEFAULT_FROM_EMAIL, ['dandresfsoto@gmail.com'])
        if request.GET.get('hub.mode') == 'subscribe' and request.GET.get('hub.verify_token') == os.getenv('VALIDATION_TOKEN'):
            return HttpResponse(request.GET.get('hub.challenge'),status=200)
        else:
            return HttpResponse(status=404)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if data['object'] == 'page':
            for entry in data['entry']:
                id = entry['id']
                time = entry['time']
                for message_object in entry['messaging']:
                    if 'message' in message_object.keys():
                        sender_id = message_object['sender']['id']
                        recipient_id = message_object['recipient']['id']
                        message = message_object['message']
                        if 'text' in message.keys():
                            response = {
                                'recipient': {
                                    'id': sender_id
                                },
                                'message': {
                                    'text': message['text']
                                }
                            }
                            self.call_send_api(response,os.getenv('VALIDATION_TOKEN'))

                    else:
                        pass
        return HttpResponse(status=200)

    def call_send_api(self,json,token):
        rqs = requests.post('https://graph.facebook.com/v2.7/me/messages',params={'access_token':token},json=json)
        return rqs.status_code