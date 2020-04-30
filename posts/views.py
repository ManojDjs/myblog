import requests
from operator import itemgetter
from django.http import HttpResponse
from datetime import date
from django.shortcuts import render
from qr_code.qrcode.utils import ContactDetail, WifiConfig, Coordinates, QRCodeOptions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here
from .models import Post
from plotly.offline import plot
import plotly.graph_objects as go
from .forms import MyForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic import CreateView

from .forms import MyModelForm
from .models import Location
def mymodel(request):
    context = {
        'posts': Location.objects.all().order_by('-date_posted')
    }
    return render(request, 'examplemodel_form.html', context)

class MyCreateView(CreateView):
    form_class = MyModelForm
    model = Location


def posts(request):
    context = {
        'posts': Post.objects.all().order_by('-date_posted')
    }
    return render(request, 'posts.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/posts/posts'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def scan(request):
    form=MyForm()
    return render(request,'scan.html',{'form':form})


def statistics(request):
    api = requests.get("https://api.thevirustracker.com/free-api?global=stats")
    result = api.json()['results']
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "db5da9c3bcmsh732ce95c62ebea7p19777ejsn61d83d88dea6"
    }
    response = requests.request("GET", url, headers=headers)

    country = response.json()['countries_stat']
    new = sorted(country, key=lambda i: int(i['cases'].replace(',', '')), reverse=True)
    context2 = new[0:15]
    context3 = context2
    for j in context3:
        j.pop('region')
    labels = []
    data = []
    total = []
    # print(context3)
    for entry in context2:
        labels.append(entry['country_name'])
        data.append(int(entry['deaths'].replace(',', '')))
        total.append(int(entry['cases'].replace(',', '')))
    pielabel = []
    pievalues = []
    for x, y in result[0].items():
        pielabel.append(x)
        pievalues.append(y)

    def scatter():
        years = labels

        fig = go.Figure()
        fig.add_trace(go.Bar(x=years,
                             y=data,
                             name='deaths',
                             marker_color='rgb(55, 83, 109)'
                             ))
        fig.add_trace(go.Bar(x=years,
                             y=total,
                             name='total cases',
                             marker_color='rgb(26, 118, 255)'
                             ))

        fig.update_layout(
            title='Cases and deaths by corona in world',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='population',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=1.0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.15,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1  # gap between bars of the same location coordinate.
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def pie():
        labels = pielabel
        values = pievalues

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                     insidetextorientation='radial',
                                     hole=.3)])
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    def world():
        import pandas as pd

        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

        fig = go.Figure(data=go.Choropleth(
            locations=df['CODE'],
            z=df['GDP (BILLIONS)'],
            text=df['COUNTRY'],
            colorscale='Blues',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix='',
            colorbar_title='DEARTHS BT CORONA',
        ))

        fig.update_layout(
            title_text='World Corona virus Analytics ',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            width=1000, height=600,
            annotations=[dict(
                x=0.55,
                y=0.1,
                xref='paper',
                yref='paper',
                text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                    CORONA VIRUS</a>',
                showarrow=False
            )]
        )

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {'result': {'total': result[0]}, 'country': context2, 'data': data, 'labels': labels, 'plot1': scatter(),'piechart':pie(),'world':world()}

    return render(request, 'statistics.html', context)


def newplotly(request):
    # Create your views here.
    def scatter():
        years = [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=years,
                             y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                350, 430, 474, 526, 488, 537, 500, 439],
                             name='Rest of world',
                             marker_color='rgb(55, 83, 109)'
                             ))
        fig.add_trace(go.Bar(x=years,
                             y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                                299, 340, 403, 549, 499],
                             name='China',
                             marker_color='rgb(26, 118, 255)'
                             ))

        fig.update_layout(
            title='US Export of Plastic Scrap',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='USD (millions)',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.15,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1  # gap between bars of the same location coordinate.
        )
        # fig.show()
        # x1 = [1,2,3,4]
        # y1 = [30, 35, 25, 45]
        #
        # trace = go.Scatter(
        #     x=x1,
        #     y = y1
        # )
        # layout = dict(
        #     title='Simple Graph',
        #     xaxis=dict(range=[min(x1), max(x1)]),
        #     yaxis = dict(range=[min(y1), max(y1)])
        # )
        #
        # fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {
        'plot1': scatter()
    }

    return render(request, 'new.html', context)
def code(request):
    # Use a ContactDetail instance to encapsulate the detail of the contact.
    contact_detail = ContactDetail(
        first_name='John',
        last_name='Doe',
        first_name_reading='jAAn',
        last_name_reading='dOH',
        tel='+41769998877',
        email='j.doe@company.com',
        url='http://www.company.com',
        birthday=date(year=1985, month=10, day=2),
        address='Cras des Fourches 987, 2800 Delémont, Jura, Switzerland',
        memo='Development Manager',
        org='Company Ltd',
    )

    # Use a WifiConfig instance to encapsulate the configuration of the connexion.
    wifi_config = WifiConfig(
        ssid='my-wifi',
        authentication=WifiConfig.AUTHENTICATION.WPA,
        password='wifi-password'
    )

    # Build coordinates instances.
    google_maps_coordinates = Coordinates(latitude=586000.32, longitude=250954.19)
    geolocation_coordinates = Coordinates(latitude=586000.32, longitude=250954.19, altitude=500)

    # Build context for rendering QR codes.
    context = dict(
        contact_detail=contact_detail,
        wifi_config=wifi_config,
        video_id='J9go2nj6b3M',
        google_maps_coordinates=google_maps_coordinates,
        geolocation_coordinates=geolocation_coordinates,
        options_example=QRCodeOptions(size='t', border=6, error_correction='L'),
    )

    # Render the index page.
    return render(request, 'qrcode.html', context=context)