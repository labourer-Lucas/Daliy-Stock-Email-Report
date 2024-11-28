import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
from datetime import datetime
import yfinance as yf
import pandas as pd
import json
import sys
import numpy as np
import pandas_market_calendars as mcal
import pytz
import time
def is_trading_day():
    date=datetime.now().strftime("%Y-%m-%d")
    result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
    return result.empty == False

#function to read holdings
def read_holdings_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, usecols=["Ticker", "AveragePrice", "Shares"])
        return df
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        sys.exit(1)

#function to read watching list
def read_watchings_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, usecols=["Ticker"])
        return df
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        sys.exit(1)

#read email config
def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except Exception as e:
        print(f"Failed to read config file: {e}")
        sys.exit(1)

def write_watching_data(watchings):
    watching_symbols = watchings['Ticker'].tolist()
    watching_data = []

    for symbol in watching_symbols:
        stock = yf.Ticker(symbol)
        current_price = stock.info.get("currentPrice", "N/A")
        forward_pe = stock.info.get("forwardPE", "N/A")
        target_high_price = stock.info.get("targetHighPrice", "N/A")
        target_low_price = stock.info.get("targetLowPrice", "N/A")
        target_median_price = stock.info.get("targetMedianPrice", "N/A")


        earning_coefficient = (
            np.log(np.exp(1) * target_high_price / current_price) * np.log(np.exp(1) * target_low_price / current_price)
            if target_high_price != "N/A" and target_low_price != "N/A" and current_price != "N/A"
            else "N/A"
        )

        watching_data.append({
            "Ticker": symbol,
            "CurrentPrice": current_price,
            "TargetMedianPrice": target_median_price,
            "ForwardPE": forward_pe,
            "EarningCoefficient": earning_coefficient,
            "TargetHigh": target_high_price,
            "TargetLow": target_low_price
        })

    # Create the DataFrame
    watching_data_df = pd.DataFrame(watching_data)

    # Calculate the 'Earning' column
    watching_data_df["TargetEarningRate"]= (
        watching_data_df["TargetMedianPrice"] - watching_data_df["CurrentPrice"]
    ) / watching_data_df["CurrentPrice"]* 100
    watching_data_df["TargetEarningRate"] = watching_data_df["TargetEarningRate"].apply(lambda x: f"{x:.2f}%" if not pd.isnull(x) else "N/A")
    # Rank the 'EarningCoefficient' column
    watching_data_df["EarningCoefficientRank"] = watching_data_df["EarningCoefficient"].rank(
        ascending=False, na_option='bottom'
    )
    watching_data_df=watching_data_df.sort_values("EarningCoefficientRank")
    return watching_data_df

def write_holding_data(holdings):
    holding_symbols = holdings['Ticker'].tolist()
    holding_data = []

    for symbol in holding_symbols:
        stock = yf.Ticker(symbol)
        current_price = stock.info.get("currentPrice", "N/A")
        forward_pe = stock.info.get("forwardPE", "N/A")
        average_price = holdings.loc[holdings['Ticker'] == symbol, 'AveragePrice'].values[0]
        shares = holdings.loc[holdings['Ticker'] == symbol, 'Shares'].values[0]
        target_high_price = stock.info.get("targetHighPrice", "N/A")
        target_low_price = stock.info.get("targetLowPrice", "N/A")
        target_median_price = stock.info.get("targetMedianPrice", "N/A")

        earning_coefficient = (
            np.log(np.exp(1) * target_high_price / current_price) * np.log(np.exp(1) * target_low_price / current_price)
            if target_high_price != "N/A" and target_low_price != "N/A" and current_price != "N/A"
            else "N/A"
        )

        holding_data.append({
            "Ticker": symbol,
            "CurrentPrice": current_price,
            "AveragePrice": average_price,
            "Shares": shares,
            "TargetMedianPrice": target_median_price,
            "ForwardPE": forward_pe,
            "EarningCoefficient": earning_coefficient
        })

    # Create the DataFrame
    holding_data_df = pd.DataFrame(holding_data)

    # Calculate the 'Earning' column
    holding_data_df["Earning"] = (
        holding_data_df["CurrentPrice"] - holding_data_df["AveragePrice"]
    ) *holding_data_df["Shares"]
    holding_data_df["EarningRate"] = (
        holding_data_df["CurrentPrice"] - holding_data_df["AveragePrice"]
    ) / holding_data_df["CurrentPrice"]* 100
    holding_data_df["EarningRate"] = holding_data_df["EarningRate"].apply(lambda x: f"{x:.2f}%" if not pd.isnull(x) else "N/A")
    holding_data_df["TargetEarningRate"]= (
        holding_data_df["TargetMedianPrice"] - holding_data_df["CurrentPrice"]
    ) / holding_data_df["CurrentPrice"]* 100
    holding_data_df["TargetEarningRate"] = holding_data_df["TargetEarningRate"].apply(lambda x: f"{x:.2f}%" if not pd.isnull(x) else "N/A")
    # Rank the 'EarningCoefficient' column
    holding_data_df["EarningCoefficientRank"] = holding_data_df["EarningCoefficient"].rank(
        ascending=False, na_option='bottom'
    )
    holding_data_df=holding_data_df.sort_values("EarningCoefficientRank")
    return holding_data_df

def send_stock_email():
    if is_trading_day():
        config = read_config("config/config.json")
        send_email = config.get("sender_email")
        sender_password = config.get("sender_password")
        smtp_server = config.get("smtp_server")
        smtp_port = config.get("smtp_port")
        receiver_email = config.get("receiver_email")
        holding_path=config.get("holding_path")
        watching_path=config.get("watching_path")
        timeStamp = datetime.now().strftime('%Y%m%d_%H%M')
        #read holdings and watchings
        holdings=read_holdings_from_excel(holding_path)
        holdings_result=write_holding_data(holdings)
        holdings_html=holdings_result.to_html()
        watchings=read_watchings_from_excel(watching_path)
        watching_result=write_watching_data(watchings)
        watchings_html=watching_result.to_html()
        #store the result 
        holding_outpath="result/"+"holding_"+timeStamp+".xlsx"
        watching_outpath="result/"+"watching_"+timeStamp+".xlsx"
        watching_result.to_excel(watching_outpath)
        holdings_result.to_excel(holding_outpath)
        # email body
        message = MIMEMultipart()
        message["From"] = send_email
        message["To"] = receiver_email
        message["Subject"] = "Daily Stock Notification " + timeStamp

        email_content = f"""
            <html>
            <body>
                <h2>Holdings Data</h2>
                {holdings_html}
                <br><br>
                <h2>Watchings Data</h2>
                {watchings_html}
            </body>
            </html>
            """
        message.attach(MIMEText(email_content, "html"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(send_email, sender_password)
            server.sendmail(send_email, receiver_email, message.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        print("Not trading day today.")


def read_holdings_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, usecols=["Ticker", "AveragePrice", "Shares"])
        return df
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return None

def schedule_tasks():
    schedule.every().day.at("15:31").do(send_stock_email)
    schedule.every().day.at("19:00").do(send_stock_email)
    schedule.every().day.at("22:00").do(send_stock_email)
    while True:
        schedule.run_pending()
        time.sleep(35)
    
if __name__ == "__main__":
    # send_stock_email()
    schedule_tasks()