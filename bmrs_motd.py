#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import pandas as pd
import os 
import datetime
import dotenv
import io

def SP_to_hour(SP):
	m = '00' if SP%2 == 0 else '30'
	h = str(int(SP/2))
	hour = '{}:{}'.format(h,m)
	return hour


if __name__ == "__main__":

	dotenv.load_dotenv()
	API_KEY = os.getenv('BMRS_KEY')

	yesterday = datetime.date.today() - datetime.timedelta(1)
	yesterday, yesterday_normal = yesterday.strftime('%Y-%m-%d'), yesterday.strftime('%d-%m-%Y')
	date = yesterday

	print("Elexon data for yesterday ({})".format(yesterday_normal))
	print()

	# Aggregated imbalance volumes
	url = 'https://api.bmreports.com/BMRS/B1780/v1?APIKey={}&SettlementDate={}&Period=*&ServiceType=csv'.format(API_KEY, date)
	response = requests.get(url, allow_redirects=True)
	df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), header=4, error_bad_lines=False)
	max_imb = df[df['Imbalance Quantity (MAW)'] == df['Imbalance Quantity (MAW)'].max()].head(1)
	min_imb = df[df['Imbalance Quantity (MAW)'] == df['Imbalance Quantity (MAW)'].min()].head(1)

	print("Imbalance Quantity")
	print("------------------")
	print("Min: {:.2f} MW at {}".format(min_imb['Imbalance Quantity (MAW)'].item(), SP_to_hour(min_imb['Settlement Period'].item())))
	print("Max: {:.2f} MW at {}".format(max_imb['Imbalance Quantity (MAW)'].item(), SP_to_hour(max_imb['Settlement Period'].item())))
	print()

	# Imbalance prices
	url = 'https://api.bmreports.com/BMRS/B1770/v1?APIKey={}&SettlementDate={}&Period=*&ServiceType=csv'.format(API_KEY, date)
	response = requests.get(url, allow_redirects=True)
	df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), header=4, error_bad_lines=False)
	max_pr = df[df['ImbalancePriceAmount'] == df['ImbalancePriceAmount'].max()].head(1)
	min_pr = df[df['ImbalancePriceAmount'] == df['ImbalancePriceAmount'].min()].head(1)
	

	print("Imbalance Price")
	print("------------------")
	print("Min: £{:.2f} at SP {}".format(min_pr['ImbalancePriceAmount'].item(), SP_to_hour(min_pr['SettlementPeriod'].item())))
	print("Max: £{:.2f} at SP {}".format(max_pr['ImbalancePriceAmount'].item(), SP_to_hour(max_pr['SettlementPeriod'].item())))
	print()

	# Fuel mix 
	url = 'https://api.bmreports.com/BMRS/B1620/v1?APIKey={}&SettlementDate={}&Period=*&ServiceType=csv'.format(API_KEY, date)
	response = requests.get(url, allow_redirects=True)
	df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), header=4)

	summ = df.groupby('Power System Resource  Type').agg('sum')
	summ['pen'] = summ.Quantity / summ.Quantity.sum()
	wind_pen = summ.loc['Wind Onshore'].pen + summ.loc['Wind Offshore'].pen

	print("Wind penetration: {:.1f}%".format(wind_pen*100))

	# Peak demand
	url = 'https://api.bmreports.com/BMRS/PKDEMYESTTDYTOM/v1?APIKey={}&ServiceType=csv'.format(API_KEY)
	response = requests.get(url, allow_redirects=True)
	df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), header=0)
	peak_dem = df['PEAK DEMAND DATA_YESTERDAY'][0]
	print("Peak demand: {:.1f} GW".format(peak_dem/1000))
	print()

	print("Have a great day!")




	
