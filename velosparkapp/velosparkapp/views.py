import json
import os

# from django.conf import settings
# from django.http import Http404
# from django.shortcuts import render
# from django.template import Template, Context
# from django.template.loader_tags import BlockNode
# from django.utils._os import safe_join
from django.views.generic.base import TemplateView
from django.views import generic
# from django.utils import timezone
# from django.views import View
#
from allaccess.views import OAuthCallback
#
from api.models import Athlete

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            try:
                access = self.request.user.accountaccess_set.all()[0]
            except IndexError:
                access = None
            else:
                client = access.api_client

                profile_info = client.get_profile_info(raw_token=access.access_token)
                # strava_user_id = getattr(self.request.user, 'id')
                # strava_user = StravaUser.objects.get(pk=strava_user_id)

        return context
class ContactView(TemplateView):
    template_name = "contact.html"

class ProfileView(generic.DetailView):
    model = Athlete
    template_name = "profile.html"

class NewActivityDataCallback(OAuthCallback):

    def get_login_redirect(self, provider, user, access, new=False):
        "Send a tweet for new Twitter users."
        if new and provider.name == 'strava':
            api = access.api_client
            params = {'page': 0}
            url = 'https://www.strava.com/api/v3/athlete/activities'
            response = api.request('get', url, params=params)
            # Check for errors in the response?
        return super(NewActivityDataCallback, self).get_login_redirect(provider, user, access, new)

# def get_page_or_404(name):
#     """Return page content as a Django template or raise 404 error."""
#     try:
#         file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
#     except ValueError:
#         raise Http404('Page Not Found')
#     else:
#         if not os.path.exists(file_path):
#             raise Http404('Page Not Found')
#
#     with open(file_path, 'r') as f:
#         page = Template(f.read())
#     meta = None
#     for i, node in enumerate(list(page.nodelist)):
#         if isinstance(node, BlockNode) and node.name == 'context':
#             meta = page.nodelist.pop(i)
#             break
#     page._meta = meta
#     return page
#
# class MyTemplateView(View):
    # def page(self, request, slug):
    #     """Render the requested page if found."""
    #     file_name = '{}.html'.format(slug)
    #     page = get_page_or_404(file_name)
    #     context = {
    #         'slug': slug,
    #         'page': page,
    #     }
    #     if page._meta is not None:
    #     	meta = page._meta.render(Context())
    #     	extra_context = json.loads(meta)
    #     	context.update(extra_context)
    #
    #     if request.user.is_authenticated():
    #         try:
    #             access = request.user.accountaccess_set.all()[0]
    #         except IndexError:
    #             access = None
    #         else:
    #             client = access.api_client
    #
    #             context['info'] = client.get_profile_info(raw_token=access.access_token)
    #     return context
    #
    # def get(self, request, *args, **kwargs):
    #     try:
    #         slug = self.kwargs['slug']
    #     except KeyError:
    #         slug='index'
    #     context = self.page(request, slug=slug)
    #     return render(request, 'page.html', context)




# class MapView(TemplateView):
#     template_name = "map.html"
#
# class ActivityView(DetailView):
#     model = Activity
#     template_name = 'activity.html'
#
# class RecResultsView(ListView):
#     model = Athlete
#     template_name = 'results.html'
#
#
#
#
def page(request, slug='index'):
    """Render the requested page if found."""
    file_name = '{}.html'.format(slug)
    page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'page': page,
    }
    if page._meta is not None:
    	meta = page._meta.render(Context())
    	extra_context = json.loads(meta)
    	context.update(extra_context)

    if request.user.is_authenticated():
        try:
            access = request.user.accountaccess_set.all()[0]
        except IndexError:
            access = None
        else:
            client = access.api_client

            context['info'] = client.get_profile_info(raw_token=access.access_token)
            # context['username'] = context['info']['username']
            # athlete = Athlete()
            profile_info = client.get_profile_info(raw_token=access.access_token)
            strava_user_id = getattr(request.user, 'id')
            strava_user = StravaUser.objects.get(pk=strava_user_id)
            # athlete = model(**strava_user.cleaned_data)

            athlete = None
            try:
                athlete = Athlete.objects.get(id=profile_info['id'])
            except Athlete.DoesNotExist:
                athlete = Athlete(id=profile_info['id'])
                athlete.user = StravaUser.objects.get(pk=strava_user_id)

            athlete.deserialize(profile_info)

            athlete.save()

            # athlete.user = strava_user
            # athlete.firstname = profile_info['firstname']
            # athlete.lastname = profile_info['lastname']
            # athlete.resource_state = profile_info['resource_state']



            # context['firstname'] = profile_info['firstname']
            # strava_user.firstname = profile_info['firstname']
            # strava_user.save()
            # athlete = Athlete.objects.get(pk=getattr(request.user, 'id'))
            # athlete.firstname =
            # athlete.save()

        # TODO: need to step get list of activities and put them in to database if they are not already there the following shows how to get one page of data from strava api:

        # if slug == 'test':
        #     params = {'page': 0}
        #     url = 'https://www.strava.com/api/v3/athlete/activities'
            # context['test'] = client.request('get', url, params=params)

    return render(request, 'page.html', context)
