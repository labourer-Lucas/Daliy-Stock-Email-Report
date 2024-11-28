# **[Daliy-Stock-Email-with-quant](https://github.com/labourer-Lucas/Daliy-Stock-Email-with-quant)**

This project is an automated system that sends daily emails summarizing the stock market data of your holdings and watchlist and **rank them with my trading algorithm**. It utilizes the yfinance for fetching stock prices, and SMTP for email delivery. The email contains details on your current holdings and watchlist, providing useful metrics like earnings, P/E ratios, and target price earnings potential.

## Features

- **Daily Automated Stock Emails**: Sends a detailed summary of your stock holdings and watchlist on trading days.

**Holdings Data**

|      | Ticker | CurrentPrice | AveragePrice | Shares | TargetMedianPrice | ForwardPE | EarningCoefficient | Earning | EarningRate | TargetEarningRate | EarningCoefficientRank |
| ---- | ------ | ------------ | ------------ | ------ | ----------------- | --------- | ------------------ | ------- | ----------- | ----------------- | ---------------------- |
| 1    | AMD    | 136.24       | 147.73       | 12     | 184.500           | 26.509449 | 1.718232           | -137.88 | -8.43%      | 35.42%            | 1.0                    |
| 2    | QCOM   | 156.40       | 153.57       | 5      | 200.000           | 12.630024 | 1.581188           | 14.15   | 1.81%       | 27.88%            | 2.0                    |
| 0    | ASML   | 670.48       | 699.95       | 1      | 886.287           | 28.834303 | 1.394849           | -29.47  | -4.40%      | 32.19%            | 3.0                    |
| 4    | NVDA   | 135.34       | 135.00       | 1      | 175.000           | 30.627184 | 1.367748           | 0.34    | 0.25%       | 29.30%            | 4.0                    |
| 5    | MSFT   | 422.99       | 416.61       | 3      | 500.000           | 28.131836 | 1.340007           | 19.14   | 1.51%       | 18.21%            | 5.0                    |
| 3    | PYPL   | 86.57        | 79.45        | 15     | 90.000            | 17.712496 | 1.076854           | 106.80  | 8.22%       | 3.96%             | 6.0                    |

**Watchings Data**

|      | Ticker | CurrentPrice | TargetMedianPrice | ForwardPE | EarningCoefficient | TargetHigh | TargetLow | TargetEarningRate | EarningCoefficientRank |
| ---- | ------ | ------------ | ----------------- | --------- | ------------------ | ---------- | --------- | ----------------- | ---------------------- |
| 5    | LRCX   | 71.57        | 95.0              | 16.994268 | 1.534127           | 114.0      | 75.0      | 32.74%            | 1.0                    |
| 2    | TSM    | 181.19       | 240.0             | 20.391123 | 1.371089           | 265.0      | 180.0     | 32.46%            | 2.0                    |
| 0    | NVDA   | 135.34       | 175.0             | 30.627184 | 1.367748           | 220.0      | 125.0     | 29.30%            | 3.0                    |
| 1    | GOOG   | 170.82       | 207.0             | 19.090216 | 1.252738           | 225.0      | 167.8     | 21.18%            | 4.0                    |
| 6    | AMZN   | 205.74       | 235.0             | 33.432080 | 1.148664           | 285.0      | 180.0     | 14.22%            | 5.0                    |
| 3    | LLY    | 788.19       | 1005.0            | 34.877857 | 1.013006           | 1250.0     | 580.0     | 27.51%            | 6.0                    |
| 4    | ARM    | 133.37       | 159.5             | 65.021420 | 0.416678           | 200.0      | 66.0      | 19.59%            | 7.0                    |

- **Performance Metrics**: Calculates metrics such as earnings rate, target earnings rate, and earnings coefficient rank, with self-designed algorithm.
- **Scheduling**: Automates email sending at three specific times throughout the day.

## Requirements

- Python 3.x

Install the dependencies via pip:

```bash
pip install requirements.txt
```

## Setup

1. **Email Configuration**: Add a `config.json` file under the `config/` directory with the following structure:

   ```json
   {
     "sender_email": "your_email@gmail.com",
     "sender_password": "your_password",
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 587,
     "receiver_email": "receiver_email@gmail.com",
     "holding_path": "config/Holdings.xlsx",
     "watching_path": "config/Watching_list.xlsx"
   }
   ```

2. **Adapt Holdings and Watchlist Excel Files**: Ensure your holdings and watchlist are saved in separate Excel files with the required columns:

   - Holdings file should contain columns: `Ticker`, `AveragePrice`, `Shares`
   - Watchlist file should contain column: `Ticker`

## Quick Start

Start by running  `dailyReport.py`

```bash
python src/dailyReport.py
```

## Earning Coefficient

$$
EarningCoefficient=ln(e\times \frac{Target\ High\ Price}{Current\ Price})\times ln(e\times \frac{Target\ Low\ Price}{Current\ Price})
$$



## IMPORTANT LEGAL DISCLAIMER

This repo is based on [yfinance](https://github.com/ranaroussi/yfinance):

> yfinance is **not** affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes.

