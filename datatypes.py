from hashlib import sha256
from typing import TypedDict
from datetime import date
import requests
import yfinance as yf
import random

url = ('https://newsapi.org/v2/everything?' + 'q=Apple&' + 'from=2023-06-06&' + 'sortBy=popularity&' +    'apiKey=20178bc4c5624a8eb12652874011bc05')

response = requests.get(url)

# print(response.json())


msft = yf.Ticker("MSFT")
# print(msft.info['currentPrice'])

# for i in ['MSFT', "ACB", "NVDA", "META", "AAPL"]:
#   print(yf.Ticker(i).info['currentPrice'])

news_api_key = "20178bc4c5624a8eb12652874011bc05"

class Message(TypedDict):
  author: str
  content: str

class Conversation(TypedDict):
  subject: str
  conversation: list[Message]

class Flashcard(TypedDict):
  topic: str
  conversation: list[Message]

class Stock(TypedDict):
  ticker : str
  orig_price: float
  current_price: float
  price_difference: float
  day_high: float
  day_low: float

class Portfolio(TypedDict):
  name: str
  creation: str
  private: bool
  info: str
  stocks: list[Stock]

class ExchangePair(TypedDict):
  curr_one: str
  curr_two: str
  final_profit: float

class Forex(TypedDict):
  creation: date
  top_pairs: list[ExchangePair]
  

class User(TypedDict):
  username: str
  password: str
  private: bool
  name: str
  email: str
  location: str
  flashcards: list[Flashcard]
  messages: list[Conversation]
  portfolios: list[Portfolio]
  forexes: list[Forex]
  following: list[str]

def updated_stock_prices(orig: list[Stock]) -> list[Stock]:
  results: list[Stock] = orig
  for stock in results:
    info = yf.Ticker(stock['ticker']).info

    current_price = info['currentPrice']
    day_high = info['dayHigh']
    day_low = info['dayLow']
    price_change = (current_price - stock['orig_price']) / stock['orig_price'] * 100.00
    stock["current_price"] = current_price
    stock["price_difference"] = price_change
    stock["day_high"] = day_high
    stock["day_low"] = day_low
  return results

#print(yf.Ticker("NVDA").info)


def gen_stock(name:str) -> Stock:
  return {
    "ticker" : name,
    "orig_price" : 1,
    "current_price" : 1,
    "price_difference" : 1,
    "day_high" : 1,
    "day_low" : 1
  }

# print(updated_stock_prices([{
#   "ticker" : "AAPL",
#   "orig_price": 133.00
# }, {
#   "ticker": "NVDA",
#   "orig_price": 144.33
# } ]))

def get_usd_rates():
  url = 'https://api.exchangerate.host/latest'
  response =   requests.get(url)
  data = response.json()
  return data['rates']
#print(data['rates'])

test_data = get_usd_rates()
# print(test_data)
# print(test_data.items())

def get_conversion(rate1: str, rate2: str):
  url = f'https://api.exchangerate.host/convert?from={rate1}&to={rate2}'
  response = requests.get(url)
  data = response.json()
  return float(data['result'])


def calculate_forex(data, limit):
  limit: int = limit
  count: int = 0
  profits: list[ExchangePair] = []


  while count <= limit:
    currencies = random.sample(list(data.items()), 2)
    currency_one = currencies[0][0]
    currency_two = currencies[1][0]
          
    conversion_rate: float = get_conversion(currency_one, currency_two)
    final_profit = data[currency_one] * conversion_rate * ( 1 / data[currency_two])
    profits.append({
      "curr_one": currency_one,
      "curr_two": currency_two,
      "final_profit": final_profit
    })
    count += 1
  
  return profits

#print(sorted(calculate_forex(test_data), key= lambda pair: pair['final_profit']))
      

def password_check(input_pwd: str, hash: str) -> bool:
  input_pwd_hash = sha256(input_pwd.encode()).hexdigest()
  return input_pwd_hash == hash

def input_verification(usr:str, pwd: str) -> str:
  if usr == "":
    return "Username field cannot be empty"
  if pwd == "":
    return "Passwod field cannot be empty"
  if len(usr) < 6:
    return "Username must be at least 6 characters"
  if len(pwd) < 6:
    return "Password must be at least 6 characters"
  return "OK"

def gen_new_user(usr:str, pwd_hash:str) -> User:
  return {
    "username": usr,
    "password": pwd_hash,
    "name": "",
    "email": "",
    "location": "",
    "following": [],
    "flashcards": [{"topic": "What Are Different Ways Of Trading", "conversation": [
      {
        "author": "assistant",
        "content": "Some common ways of trading include day trading, swing trading, positional trading, and algorithmic trading."
      }
    ]}, {"topic": "Why Do People Short", "conversation": [
      {
        "author": "assistant",
        "content": "To profit from a decline in the price of an asset, or to hedge against potential losses in a portfolio."
      }
    ]} , {"topic": "What Is Citadel", "conversation": [
      {
        "author": "assistant",
        "content": "Citadel is a global investment firm that manages hedge funds, operates market-making initiatives, and provides other financial services."
      }
    ]}, {"topic": "Can You Explain Equity", "conversation": [
      {
        "author": "assistant",
        "content": "Equity represents ownership in a company, typically in the form of stocks. Higher equity means higher ownership and potential profits."
      }
    ]}, {"topic": "What Is Forex", "conversation": [
      {
        "author": "assistant",
        "content": "Forex refers to the market for trading currencies from around the world. It is short for 'foreign exchange'"
      }
    ]} , {"topic": "What Are Bollinger Bands", "conversation": [
      {
        "author": "assistant",
        "content": "Bollinger Bands are a technical analysis tool used to measure volatility. They consist of a moving average and upper and lower bands."
      }
    ]}
    ],
    "messages": [],
    "forexes": [],
    "portfolios": [{"name": "AAPL", "creation": "04-01-2023", 
                    "private": True, "info": "", "stocks":[{"ticker": "AAPL", 
                                                            "orig_price": 100,"current_price": 23001, 
                                                            "price_difference": 100, "day_high": 123212, "day_low": 1234}]}]
  }



example_user:User = {
  "username": "Bob",
  "password": "w5en424nf",
  "name": "Bobert",
  "email": "bob@bobert.org",
  "location": "New York",
  "following": [
    "ann", "lucia"
  ],
  "flashcards": [
    {
      "topic": "Forex",
      "conversation": [
        {
          "author": "user",
          "content": "What exactly is forex?"
        }, {
          "author": "assistant",
          "content": "Of course! forex is... "
        }
      ] 
    }
  ],
  "messages": [
    {
      "subject" : "lucia",
      "conversation": [
        {
          "author": "bob",
          "content": "hi, I noticed something"
        }, {
          "author": "lucia",
          "content": "kinda weird bro"
        } 
      ]
    },
    {
      "subject": "ann",
      "conversation": [
        {
          "author": "ann",
          "content": "hi bob how are you?"
        },{
          "author": "bob",
          "content": "going strong, thank you"
        }
      ]
    }
  ],
  "portfolios": [
    {
      "name": "test portfolio",
      "creation": date(2023,4,1),
      "private": False,
      "info": "sdf4624",
      "stocks": [
        {
          "ticker": "AAPL",
          "orig_price": 131.03,
          "current_price": 144.01,
          "price_difference": 0.03
        }, {
          "ticker": "NVDA",
          "orig_price": 185.31,
          "current_price": 184.33,
          "price_differece": -0.02
        }
      ]
    }
  ],
  "forexes" : [ 
    {
      "creation": date(2023,2,15),
      "top_pairs": [
        {
          "curr_one": "KRW",
          "curr_two": "JYN",
          "final_profit": 1.000034
        }, {
          "curr_one": "KRW",
          "curr_two": "MPS",
          "final_profit": 1.000023
        }, {
          "curr_one": "KRW",
          "curr_two": "LYN",
          "final_profit": 1.000011
        }
      ]
    } 
  ]
}
  

def gen_new_flashcard(): 
  return "lol"