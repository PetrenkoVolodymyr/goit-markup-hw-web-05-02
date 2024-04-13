import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys

dates_list =[]
currency_list = ['USD', 'EUR']


class Request:
    async def handler (self, days, curr_list):
        # print(third_curr)
        dates_list = await self.dates_generator(days)
        reply=[]
        for date in dates_list:
            
            data_per_day = await self.data_generator(date, curr_list)
            required_data_per_day = await self.adapter(date, data_per_day)
            reply.append(required_data_per_day)
        return reply


    async def dates_generator(self, number):
        for i in range(number):
            date = (datetime.now()-timedelta(days = i)).strftime("%d.%m.%Y")
            dates_list.append(date)
        return dates_list
        

    async def adapter(self, date, info):
        dict_per_day ={}
        for item in info:
           
            info_one_currency = {item['currency']: {
            'sale': item['saleRate'],
            'purchase': item['purchaseRate']}}
            dict_per_day.update(info_one_currency)
        return {date: dict_per_day}

    async def data_generator(self, date, curr_list):
        currecny_data_dor_date=[]
        params = {'date': date}

        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.privatbank.ua/p24api/exchange_rates', params = params) as response:

                data = await response.json()
                all_rates = data['exchangeRate']
                for currency in curr_list:
                    one_curr_dict = list(filter(lambda x: x['currency'] == currency, all_rates))[0]  
                    currecny_data_dor_date.append(one_curr_dict)           
                return currecny_data_dor_date


async def main_(days):   
    qty_days = int(days)
    port = Request()
    return await port.handler(qty_days, currency_list)
  

if __name__ == "__main__":

    asyncio.run(main_())



