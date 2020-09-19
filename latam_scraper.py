#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import datetime


def get_prices(flight, driver):
    ''' Get Economy and Premium Prices '''
    prices = []
    try:
        flight.click()

        # ### Economy #####
        tarifas_basicas = flight.find_elements_by_xpath('.//div[@class="fares-table-container"]//tfoot//td[contains(@class, "fare-")]')
        print('Economy cabin')
        for tarifa in tarifas_basicas:
            label = tarifa.find_element_by_xpath('.//label').get_attribute('for')
            price = tarifa.find_element_by_xpath('.//span[@class="price"]/span[@class="value"]/span')
            currency = tarifa.find_element_by_xpath('.//span[@class="price"]/span[@class="currency-symbol"]')
            print('{}: {}{}'.format(label, currency.text, price.text))
            data_economy = {
                'Category': label,
                'Price': price.text,
                'Currency': currency.text,
            }
            prices.append(data_economy)
        print('-' * 40)

        #### Premium #####
        button_premium = flight.find_element_by_xpath('.//li[@id="J"]')
        button_premium.click()
        tarifas_premium = flight.find_elements_by_xpath('.//div[@class="fares-table-container"]//tfoot//td[contains(@class, "fare-")]')
        print('Premium Bussines Cabin')
        for tarifa in tarifas_premium:
            label = tarifa.find_element_by_xpath('.//label').get_attribute('for')
            price = tarifa.find_element_by_xpath('.//span[@class="price"]/span[@class="value"]/span')
            currency = tarifa.find_element_by_xpath('.//span[@class="price"]/span[@class="currency-symbol"]')
            print('{}: {}{}'.format(label, currency.text, price.text))
            data_premium = {
                'Category': label,
                'Price': price.text.replace('.', ''),
                'Currency': currency.text,
                }
            prices.append(data_premium)
        print('-' * 40)
        return prices
    except Exception as e:
        print(e)
        driver.close()


def flight_connections(flight, driver):
    ''' Get the flight connections '''
    flight_connections = []
    try:
        button = flight.find_element_by_xpath('.//div[@class="flight-summary-stops-description"]/button')
        button.click()
        segments = flight.find_elements_by_xpath('//div[@class="sc-hZSUBg gfeULV"]/div[@class="sc-cLQEGU hyoued"]')
        for idx, escala in enumerate(segments):
            print('Flight connection N°: {}'.format(idx + 1))
            escala = segments[idx].find_elements_by_xpath('.//span[@class="sc-bsbRJL bMMExG"]//abbr')
            escala_time = segments[idx].find_elements_by_xpath('.//span[@class="sc-bsbRJL bMMExG"]//time')
            # Origin
            print('Origin: {} Departure: {}'.format(escala[0].text, escala_time[0].text))
            # Destiny
            print('Destiny: {} Departure: {}'.format(escala[1].text, escala_time[1].text))
            # duration
            duration = segments[idx].find_element_by_xpath('.//span[@class="sc-cmthru ipcOEH"]//time').get_attribute('datetime')
            print('Duration: {}h'.format(duration))
            # Numero de vuelo y Avion
            numero = segments[idx].find_element_by_xpath('.//div[@class="airline-flight-details"]//b')
            avion = segments[idx].find_element_by_xpath('.//span[@class="sc-gzOgki uTyOl"]')
            print('N° Flight: {} Airplane: {}'.format(numero.text, avion.text))
            # Avion
            print('-' * 40)

            data = {
                'Origin': escala[0].text,
                'Origin-Departure': escala_time[0].text,
                'Destiny': escala[1].text,
                'Destiny-Departure': escala_time[0].text,
                'Duration': duration,
                'Flight N°': numero.text,
                'Airplane N°': avion.text,
            }

            flight_connections.append(data)
        driver.find_element_by_xpath('//div[@class="modal-content sc-iwsKbI eHVGAN"]//button[@class="close"]').click()
        return flight_connections
    except Exception as e:
        print(e)
        driver.close()


def departure_func(flight, driver):
    ''' Get the general flight informatio '''
    flight_general = []
    try:
        # ############## FLIGHT ###################
        departure = flight.find_element_by_xpath('.//div[@class="departure"]/time').get_attribute('datetime')
        arrival = flight.find_element_by_xpath('.//div[@class="arrival"]/time').get_attribute('datetime')
        duration = flight.find_element_by_xpath('.//span[@class="duration"]/time').get_attribute('datetime')
        duration = duration.replace('PT', '')
        print('Departure: {} Arrival: {} Duration: {}'.format(departure, arrival, duration))
        print('-' * 40)
        data = {
            'Departure': departure,
            'Arrival': arrival,
            'Duration': duration,
        }
        flight_general.append(data)
        return data

    except Exception as e:
        print(e)
        driver.close()


if __name__ == "__main__":
    url = input('Input Flight URL: ')
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(executable_path='./geckodriver.exe')
    delay = 15
    driver.get(url)
    # time.sleep(15)
    general = []
    connection = []
    prices = []
    try:
        flights = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//li[@class="flight"]')))
        flights = driver.find_elements_by_xpath('//li[@class="flight"]')
        print('OK')
    except TimeoutException:
        print('La pagina no cargo correctamente')
        driver.close()
    if len(flights) != 0:
        print(f'Found {len(flights)} Flights')
        for idx, flight in enumerate(flights):
            print(f'<<<<<<<<<<< FLIGHT: {idx + 1} >>>>>>>>>>>')
            general.append(departure_func(flight, driver))
            connection.append(flight_connections(flight, driver))
            prices.append(get_prices(flight, driver))
    driver.close()
