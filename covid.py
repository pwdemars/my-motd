#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import pandas as pd
import io

def get_vaccination_data():
	url = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newPeopleVaccinatedFirstDoseByPublishDate%22:%22newPeopleVaccinatedFirstDoseByPublishDate%22,%22newPeopleVaccinatedSecondDoseByPublishDate%22:%22newPeopleVaccinatedSecondDoseByPublishDate%22,%22cumPeopleVaccinatedFirstDoseByPublishDate%22:%22cumPeopleVaccinatedFirstDoseByPublishDate%22,%22cumPeopleVaccinatedSecondDoseByPublishDate%22:%22cumPeopleVaccinatedSecondDoseByPublishDate%22%7D&format=csv'
	response = requests.get(url)
	df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), error_bad_lines=False)
	return df

if __name__ == "__main__":
	df = get_vaccination_data()
	df = df.sort_values('date')

	UK_pop = 66650000

	date = df.date.values[-1]
	new_vaccs = df.newPeopleVaccinatedFirstDoseByPublishDate.values[-1]
	week_vaccs = df.newPeopleVaccinatedFirstDoseByPublishDate.values[-7:]
	cum_vaccs = df.cumPeopleVaccinatedFirstDoseByPublishDate.values[-1]
	perc_vaccs = 100*cum_vaccs/UK_pop

	print("UK Covid Vaccinations: {}".format(date))
	print("---------------------------------")
	print("New vaccinations: {}".format(int(new_vaccs)))
	print("7-day average vaccinations: {}".format(int(week_vaccs.mean())))
	print("Cumulative vaccinations: {} ({:.1f}%)".format(int(cum_vaccs), perc_vaccs))
	print()
