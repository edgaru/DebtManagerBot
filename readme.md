# DebtManagerBot

DebtManagerBot is a simple yet effective Telegram bot designed to help you manage debts. It allows you to track debts and payments, and monitor outstanding balances. With DebtManagerBot, managing debts becomes a seamless experience.

## Features

- Add debtors to the system
- Record debts for each debtor, including the loan date and amount
- Add payments toward debts, specifying the date, amount, and an optional note
- View a summary of all debtors and their total outstanding balances
- View detailed information about each debtor, including their debts, payments, and remaining balances

## Requirements

- Python 3.7 or later
- MongoDB
- python-telegram-bot library (version 13.6)

## Installation

1. Clone this repository or download the source files.
2. Install the required packages with the following command:

pip install -r requirements.txt

3. Set up a MongoDB instance and configure the connection details in `database.py`.
4. Create a new bot on Telegram and obtain your API key from the BotFather. Replace `YOUR_API_KEY` in `bot.py` with your actual API key.

## Usage

Run the bot with the following command:

python bot.py

Now, you can start using DebtManagerBot through your Telegram client. Here are the available commands:

- `/start` - Welcome message and introduction to DebtManagerBot
- `/add_debtor [name]` - Add a new debtor with the provided name
- `/add_debt [name] [amount] [concept] (date)` - Add a debt for the specified debtor. The date is optional, and if not provided, the current date will be used
- `/add_payment [name] [amount] (note) (date)` - Add a payment for the specified debtor. Both the note and the date are optional
- `/show_debtors_summary` - Display a summary of all debtors and their total outstanding balances
- `/show_debtor_details [name]` - Show detailed information about the specified debtor, including their debts, payments, and remaining balance

## Contributing

If you would like to contribute to the project, feel free to submit a pull request or open an issue to discuss potential improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
