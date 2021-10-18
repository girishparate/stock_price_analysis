from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from django.urls import reverse
import dash
import dash_core_components as dcc
import dash_html_components as html


# Dashboard for 1st user
class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard.html')

''' 1) data will be pulled from html form and then, it will be processed by below class.
    2) this class will the check, whethe we are taking input from period or date selection,
    3) after that, the yf (Yahoo finance) module will filter and give data,
    4) based on that data , the graph will be created as go.Figure().
    5) after graph created, the trace, layout and x-axes will be updated.
    5) we will again pass the data to frontend to set data of the graph.html form.
'''
class GraphStock(View):
    def post(self, request):
        tickers = request.POST['tickers']
        tad = yf.Ticker(tickers)

        data_response = {}
        #  step 2
        if 'period' in request.POST and 'interval' in request.POST:
            period = str(request.POST['period'])+'d'
            interval = str(request.POST['interval'])+'m'
            # step 3
            data = yf.download(tickers=tickers, period = period, interval = interval)
            # step 4
            graph = go.Figure()
            # step 5
            graph.add_trace(go.Candlestick(x=data.index, open=data['Open'],high=data['High'],low=data['Low'],close=data['Close'],name='Market data'))
            graph.update_layout(title=tad.info['shortName']+' live share price evolution',yaxis_title='Stock price (USD per shares)')
            graph.update_xaxes(rangeslider_visible=True, rangeselector=dict())
            # step 6
            data_response['tickers'] = tickers
            data_response['short_name'] = tad.info['shortName']
            data_response['business_info'] = tad.info['longBusinessSummary']
            data_response['graph'] = graph
            data_response['period'] = request.POST['period']
            data_response['interval'] = request.POST['interval']
        else:
            # step 3
            data = yf.download(tickers = tickers, start = request.POST['start_date'], end = request.POST['end_date'])
            # step 4
            graph = go.Figure()
            # step 5
            graph.add_trace(go.Candlestick(x=data.index, open=data['Open'],high=data['High'],low=data['Low'],close=data['Close'],name='Market data'))
            graph.update_layout(title=tad.info['shortName']+' live share price evolution',yaxis_title='Stock price (USD per shares)')
            graph.update_xaxes(rangeslider_visible=True, rangeselector=dict())
            # step 6
            data_response['tickers'] = tickers
            data_response['short_name'] = tad.info['shortName']
            data_response['business_info'] = tad.info['longBusinessSummary']
            data_response['graph'] = graph
            data_response['start_date'] = request.POST['start_date']
            data_response['end_date'] = request.POST['end_date']
        
        return render(request, 'graph.html',data_response)        
   