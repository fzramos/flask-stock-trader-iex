from finance_app import app, routes
from makeSymbols import seedSymbols

if __name__ == '__main__':
    app.run(debug = True)
    # seedSymbols()
    # run this once when you want to populate your company table with real stock symbols
    # already completed so I'm commenting it out